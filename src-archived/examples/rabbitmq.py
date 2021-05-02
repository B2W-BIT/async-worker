from datetime import datetime
from typing import List

from asyncworker import App
from asyncworker.connections import AMQPConnection
from asyncworker.rabbitmq import RabbitMQMessage, AMQPRouteOptions

amqp_conn = AMQPConnection(
    hostname="127.0.0.1", username="guest", password="guest", prefetch=1024
)

app = App(connections=[amqp_conn])


@app.amqp.consume(
    ["queue"],
    options=AMQPRouteOptions(bulk_size=1024 * 8, bulk_flush_interval=10),
)
async def _handler(msgs: List[RabbitMQMessage]):
    print(f"Recv {len(msgs)} {datetime.now().isoformat()}")


@app.run_every(1)
async def produce(app: App):
    await amqp_conn.put(data={"msg": "ok"}, routing_key="queue")


app.run()
