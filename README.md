
[![Build Status](https://travis-ci.org/B2W-BIT/async-worker.svg?branch=master)](https://travis-ci.org/B2W-BIT/async-worker)
[![codecov](https://codecov.io/gh/B2W-BIT/async-worker/branch/master/graph/badge.svg)](https://codecov.io/gh/B2W-BIT/async-worker)

# Async Worker

## Propósito

Ser um microframework (inspirado no flask) para facilitar a escrita de workers de RabbitMQ.


## Exemplo

```python

from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def drain_handler(message):
    logger.info(message)

```

Nesse exemplo, o handler `drain_handler()` recebe mensagens de ambas as filas: `asgard/counts` e `asgard/counts/errors`.

Se o handler lançar alguma exception, a mensagem é automaticamente devolvida para a fila (reject com requeue=True);
Se o handler rodar sem erros, a mensagem é automaticamente confirmada (ack).


## Rejeitando uma mensagem e não colocando-a de volta na fila

Opcionalmente, caso seja necessário rejeitar uma mensagem e ao mesmo tempo **não** devolver essa mensagem pra fila,
podemos chamar `message.reject(requeue=False)`. O valor default do `requeue` é `True`.

## Configurações de ação padrão em caso de sucesso e exception

É possível escolher o que o asynworker fará com as mensagens em caso de sucesso (handler executa sel lançar exceção)
ou em caso de falha (handler lança uma exception não tratada).

As opções são: Events.ON_SUCCESS e Events.ON_EXCEPTION. Ambas são passadas a cada rota de consumo registrada, ex:

```python
from asynworker.options import Events, Actions

@app.route(["queue1", "queue2"], options={
                                  Events.ON_SUCCESS: Actions.ACK,
                                  Events.ON_EXCEPTION: Actions.REJECT,
                                  })
async def handler(messages):
    ...
```

Nesse caso, se o handler rodar com sucesso, todas as mensagem soferão `ACK`. Caso uma exceção não tratada seja capturada
pelo asyncworker todas as mensagens sofrerão `REJECT`.

### Opções possíveis

 - `Actions.ACK`: Confirma a mensagem para o RabbitMQ
 - `Actions.REJECT`: Rejeita a mensagem e **não devolve para a fila de origem**
 - `Actions.REQUEUE`: Rejeita a mensagem e **devolve** para a fila de origem.

### Sobrescrevendo a ação padrão apenas para algumas mensagens

É possível escolher uma ação diferente da padrão para qualquer mensagem do bulk que foi entregue ao handler. Para isso
basta chamar um dos métodos do objeto `RabbitMQMessage`. São eles:

 - `.accept()`: Marca a mensagem para ser confirmada para o RabbitMQ
 - `.reject(requeue=False)`: Marca a mensagem para ser rejeitada e **não devolvida** para a fila de origem
 - `.reject(requeue=True)`: Marca a mensagem para ser rejeitada e **devolvida** para a fila de origem

O valor default para o `.reject()` é `requeue=True`.

## Escolhendo o tamanho do BULK que será usado no consumo das fila

Para conseguir receber mais de uma mensagem de uma vez, para poderem ser processadas em lote, podemos fazer o seguinte:

```python
from asyncworker import App
from asyncworker.options import Options

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd", options={Options.BULK_SIZE: 1000})
async def drain_handler(messages):
    for m in messages:
      logger.info(message.body)

```

## Atualizando o async-worker no seu projeto

### 0.1.x 0.2.0

Na versão `0.2.0` criamos a possibilidade de receber mensagens em lote. E a partir dessa versão
a assinatura do handler mudo para:

```python
from asyncworker.rabbitmq.message import Message

async def handler(messages: List[Message]):
  pass
```

As instâncias do objeto `asyncworker.rabbitmq.RabbitMQMessage` já vêm por padrão configurado para receber `ack()` 
depois queo handler retornar (sem exception), mas o handler pode mudar isso
chamando o método `message.reject()` para cada mensagem que precisar ser devolvida para a fila.

O conteúdo da mensagem original está agora no atributo `message.body`. Então um handler antigo que era assim:

```python
from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def drain_handler(message):
    logger.info(message)

```

passa a ser assim:

```python
from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def drain_handler(messages):
    for m in messages:
      logger.info(message.body)

```
