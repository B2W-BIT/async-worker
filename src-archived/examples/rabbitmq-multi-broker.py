from datetime import datetime
from typing import List

from asyncworker import App
from asyncworker.connections import AMQPConnection
from asyncworker.http.methods import HTTPMethods
from asyncworker.options import Actions, Events, Options
from asyncworker.rabbitmq import RabbitMQMessage, AMQPRouteOptions

"""
Para rodar esse exemplo precisamos de dois RabbitMQ rodando, ambos na porta default.
Basta ajustar os endereços abaixo apontando cada conexão para o RabbitMQ correspondente.

Em ambos os Rabbits deve existe uma fila com nome "queue" no vhost "/".
"""


amqp_conn = AMQPConnection(
    hostname="127.0.0.1", username="guest", password="guest"
)

amqp_conn_2 = AMQPConnection(
    hostname="172.17.0.2", username="guest", password="guest"
)

app = App(connections=[amqp_conn, amqp_conn_2])


@app.amqp.consume(
    ["queue"], connection=amqp_conn, options=AMQPRouteOptions(bulk_size=64)
)
async def _handler_broker_1(msgs: List[RabbitMQMessage]):
    print(f"Broker 1 ({amqp_conn.hostname}): Recv: {len(msgs)}")
    for m in msgs:
        await amqp_conn_2["/"].put(
            serialized_data=m.serialized_data, routing_key="queue"
        )


@app.amqp.consume(
    ["queue"], connection=amqp_conn_2, options=AMQPRouteOptions(bulk_size=128)
)
async def _handler_roker_2(msgs: List[RabbitMQMessage]):
    print(f"Broker 2 ({amqp_conn_2.hostname}): Recv: {len(msgs)}")


@app.run_every(1)
async def produce(app: App):
    for _ in range(32):
        await amqp_conn.put(data={"msg": "Broker 1"}, routing_key="queue")
        await amqp_conn_2.put(data={"msg": "broker 2"}, routing_key="queue")


app.run()
