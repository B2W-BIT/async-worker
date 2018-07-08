
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


## Utils
### Timeit

Um gerenciador de contexto para marcar o tempo de execução de código e chamar
um callback `(str, float, Optional[Type[Exception]], Optional[Exception], Optional[traceback]) -> Coroutine` 
assíncrono ao final, com o tempo total de execução.

```python
import traceback
from typing import Type

from asyncworker.utils import Timeit


# App initialization stuff...

async def log_callback(name: str,
                       time_delta: float, 
                       exc_type: Type[Exception]=None, 
                       exc_val: Exception=None, 
                       exc_tb: traceback=None):
    log = {'name': name, 'time_delta': time_delta}
    if exc_type:
        await logger.error(log, exc_info=(exc_type, exc_val, exc_tb))
    else:
        await logger.info(log)


@app.route(["xablau-queue"], vhost="/")
async def drain_handler(message):
    async with Timeit(name="xablau-access-time", callback=log_callback):
        await access_some_remote_content()
```

Caso uma exceção seja levantada dentro do contexto, `log_callback` será chamado
com os dados da exceção.

## Atualizando o async-worker no seu projeto

### 0.1.0 para 0.2.0

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
