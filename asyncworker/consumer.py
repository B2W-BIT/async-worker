import asyncio
import traceback
from typing import Type

from easyqueue.async import AsyncQueueConsumerDelegate, AsyncQueue
from aioamqp.exceptions import AioamqpException

from asyncworker import conf
from asyncworker.options import Events
from .bucket import Bucket
from .rabbitmq import RabbitMQMessage


class Consumer(AsyncQueueConsumerDelegate):
    def __init__(self,
                 route_info,
                 host,
                 username,
                 password,
                 prefetch_count=128,
                 bucket_class: Type[Bucket]=Bucket):
        self.route = route_info
        self._handler = route_info['handler']
        self._queue_name = route_info['route']
        self._route_options = route_info['options']
        self.host = host
        self.vhost = self._route_options.get("vhost", "/")
        if self.vhost != "/":
            self.vhost = self.vhost.lstrip("/")
        self.bucket = bucket_class(size=min(self._route_options['bulk_size'],
                                            prefetch_count))
        self.queue = AsyncQueue(host,
                                username,
                                password,
                                virtual_host=self.vhost,
                                delegate=self,
                                prefetch_count=prefetch_count)

    @property
    def queue_name(self) -> str:
        return self._queue_name

    async def on_before_start_consumption(self,
                                          queue_name: str,
                                          queue: 'AsyncQueue'):
        """
        Coroutine called before queue consumption starts. May be overwritten to
        implement further custom initialization.

        :param queue_name: Queue name that will be consumed
        :type queue_name: str
        :param queue: AsynQueue instanced
        :type queue: AsyncQueue
        """
        pass

    async def on_consumption_start(self,
                                   consumer_tag: str,
                                   queue: 'AsyncQueue'):
        """
        Coroutine called once consumption started.
        """
        pass

    async def on_queue_message(self, content, delivery_tag, queue):
        """
        Callback called every time that a new, valid and deserialized message
        is ready to be handled.

        :param delivery_tag: delivery_tag of the consumed message
        :type delivery_tag: int
        :param content: parsed message body
        :type content: dict
        :type queue: AsyncQueue
        """
        rv = None
        all_messages = []
        try:

            if not self.bucket.is_full():
                message = RabbitMQMessage(
                    body=content,
                    delivery_tag=delivery_tag,
                    on_success=self._route_options[Events.ON_SUCCESS],
                    on_exception=self._route_options[Events.ON_EXCEPTION],
                )
                self.bucket.put(message)

            if self.bucket.is_full():
                all_messages = self.bucket.pop_all()
                rv = await self._handler(all_messages)
                await asyncio.gather(
                    *(m.process_success(queue) for m in all_messages)
                )
            return rv
        except AioamqpException as aioamqpException:
            raise aioamqpException
        except Exception as e:
            await asyncio.gather(
                *(m.process_exception(queue) for m in all_messages)
            )
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
        :type queue: AsyncQueue
        """
        conf.logger.error({
            "parse-error": True,
            "exception": "Error: not a JSON",
            "original_msg": body
        })
        try:
            await queue.ack(delivery_tag=delivery_tag)
        except AioamqpException as e:
            self._log_exception(e)

    async def on_message_handle_error(self, handler_error: Exception, **kwargs):
        """
        Callback called when an uncaught exception was raised during message
        handling stage.

        :param handler_error: The exception that triggered
        :param kwargs: arguments used to call the coroutine that handled
        the message
        :return:
        """
        self._log_exception(handler_error)

    async def on_connection_error(self, exception: Exception):
        """
        Called when the connection fails
        """
        self._log_exception(exception)

    def _log_exception(self, exception):
        current_exception = {
            "exc_message": str(exception),
            "exc_traceback": traceback.format_exc(),
        }
        conf.logger.error(current_exception)

    async def consume_all_queues(self, queue):
        for queue_name in self._queue_name:
            # Por enquanto não estamos guardando a consumer_tag retornada
            # se precisar, podemos passar a guardar.
            conf.logger.debug({"queue": queue_name, "action": "start-consume"})
            await queue.consume(queue_name=queue_name)

    def keep_runnig(self):
        return True

    async def start(self):
        while self.keep_runnig():
            if not self.queue.is_connected:
                try:
                    await self.queue.connect()
                    await self.consume_all_queues(self.queue)
                except Exception as e:
                    conf.logger.error({
                        "type": "connection-failed",
                        "dest": self.host, "retry": True,
                        "exc_traceback": traceback.format_exc()
                    })
            await asyncio.sleep(1)
