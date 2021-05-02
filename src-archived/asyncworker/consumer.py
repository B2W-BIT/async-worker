import asyncio
import traceback
from typing import Dict, List, Type, Union

from aioamqp.exceptions import AioamqpException

from asyncworker import conf
from asyncworker.easyqueue.message import AMQPMessage
from asyncworker.easyqueue.queue import JsonQueue, QueueConsumerDelegate
from asyncworker.options import DefaultValues, Events, Options
from asyncworker.routes import AMQPRoute
from asyncworker.time import ClockTicker

from .bucket import Bucket
from .rabbitmq import RabbitMQMessage


class Consumer(QueueConsumerDelegate):
    def __init__(
        self,
        route_info: Union[Dict, AMQPRoute],
        host: str,
        username: str,
        password: str,
        prefetch_count: int = 128,
        bucket_class: Type[Bucket] = Bucket[RabbitMQMessage],
    ) -> None:
        self.route = route_info
        self._handler = route_info["handler"]
        self._queue_name = route_info["routes"]
        self._route_options = route_info["options"]
        self.host = host
        self.vhost = route_info.get("vhost", "/")
        self.bucket = bucket_class(
            size=min(self._route_options["bulk_size"], prefetch_count)
        )
        self.queue: JsonQueue = JsonQueue(
            host,
            username,
            password,
            virtual_host=self.vhost,
            delegate=self,
            prefetch_count=prefetch_count,
            logger=conf.logger,
            connection_fail_callback=self._route_options.get(
                Options.CONNECTION_FAIL_CALLBACK, None
            ),
        )
        self.clock = ClockTicker(
            seconds=self._route_options.get(
                Options.BULK_FLUSH_INTERVAL, conf.settings.FLUSH_TIMEOUT
            )
        )
        self.clock_task = None

    @property
    def queue_name(self) -> str:
        return self._queue_name

    async def on_before_start_consumption(
        self, queue_name: str, queue: "JsonQueue"
    ):
        """
        Coroutine called before queue consumption starts. May be overwritten to
        implement further custom initialization.

        :param queue_name: Queue name that will be consumed
        :type queue_name: str
        :param queue: AsynQueue instanced
        :type queue: JsonQueue
        """
        pass

    async def on_consumption_start(self, consumer_tag: str, queue: "JsonQueue"):
        """
        Coroutine called once consumption started.
        """
        pass

    async def on_queue_message(self, msg: AMQPMessage):
        """
        Callback called every time that a new, valid and deserialized message
        is ready to be handled.
        """
        if not self.bucket.is_full():
            message = RabbitMQMessage(
                delivery_tag=msg.delivery_tag,
                amqp_message=msg,
                on_success=self._route_options[Events.ON_SUCCESS],
                on_exception=self._route_options[Events.ON_EXCEPTION],
            )
            self.bucket.put(message)

        if self.bucket.is_full():
            return await self._flush_bucket_if_needed()

    async def _flush_clocked(self):
        async for _ in self.clock:
            try:
                await self._flush_bucket_if_needed()
            except Exception as e:
                await conf.logger.error(
                    {
                        "type": "flush-bucket-failed",
                        "dest": self.host,
                        "retry": True,
                        "exc_traceback": traceback.format_exc(),
                    }
                )

    async def _flush_bucket_if_needed(self):
        try:
            if not self.bucket.is_empty():
                all_messages = self.bucket.pop_all()
                await conf.logger.debug(
                    {
                        "event": "bucket-flush",
                        "bucket-size": len(all_messages),
                        "handler": self._handler.__name__,
                    }
                )
                rv = await self._handler(all_messages)
                await asyncio.gather(
                    *(m.process_success() for m in all_messages)
                )
                return rv
        except AioamqpException as aioamqpException:
            raise aioamqpException
        except Exception as e:
            await asyncio.gather(*(m.process_exception() for m in all_messages))
            raise e

    async def on_queue_error(self, body, delivery_tag, error, queue):
        """
        Callback called every time that an error occurred during the validation
        or deserialization stage.

        :param body: unparsed, raw message content
        :type body: Any
        :param delivery_tag: delivery_tag of the consumed message
        :type delivery_tag: int
        :param error: THe error that caused the callback to be called
        :type error: MessageError
        :type queue: JsonQueue
        """
        await conf.logger.error(
            {
                "parse-error": True,
                "exception": "Error: not a JSON",
                "original_msg": body,
            }
        )
        try:
            await queue.ack(delivery_tag=delivery_tag)
        except AioamqpException as e:
            await self._log_exception(e)

    async def on_message_handle_error(self, handler_error: Exception, **kwargs):
        """
        Callback called when an uncaught exception was raised during message
        handling stage.

        :param handler_error: The exception that triggered
        :param kwargs: arguments used to call the coroutine that handled
        the message
        """
        await self._log_exception(handler_error)

    async def on_connection_error(self, exception: Exception):
        """
        Called when the connection fails
        """
        await self._log_exception(exception)

    async def _log_exception(self, exception):
        current_exception = {
            "exc_message": str(exception),
            "exc_traceback": traceback.format_exc(),
        }
        await conf.logger.error(current_exception)

    async def consume_all_queues(self, queue: JsonQueue):
        for queue_name in self._queue_name:
            # Por enquanto não estamos guardando a consumer_tag retornada
            # se precisar, podemos passar a guardar.
            await conf.logger.debug(
                {"queue": queue_name, "event": "start-consume"}
            )
            await queue.consume(queue_name=queue_name, delegate=self)

    def keep_runnig(self):
        return True

    async def start(self):
        while self.keep_runnig():
            if not self.queue.connection.has_channel_ready():
                try:
                    await self.consume_all_queues(self.queue)

                    if not self.clock_task:
                        self.clock_task = self._flush_clocked()
                        asyncio.get_event_loop().create_task(self.clock_task)

                except Exception as e:
                    await conf.logger.error(
                        {
                            "type": "connection-failed",
                            "dest": self.host,
                            "retry": True,
                            "exc_traceback": traceback.format_exc(),
                        }
                    )
            await asyncio.sleep(1)
