
[![Build Status](https://travis-ci.org/b2wdigital/async-worker.svg?branch=master)](https://travis-ci.org/b2wdigital/async-worker)
[![codecov](https://codecov.io/gh/b2wdigital/async-worker/branch/master/graph/badge.svg?flag=unittest)](https://codecov.io/gh/b2wdigital/async-worker)
[![codecov](https://codecov.io/gh/b2wdigital/async-worker/branch/master/graph/badge.svg?flag=typehint)](https://codecov.io/gh/b2wdigital/async-worker)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![PyPI version](https://badge.fury.io/py/async-worker.svg)](https://badge.fury.io/py/async-worker)

# Async Worker

## Propósito

Ser um microframework (inspirado no flask) para facilitar a escrita de workers assíncronos.
Atualmente o projeto suporta as seguintes backends:

* [RabbitMQ](https://www.rabbitmq.com/): Consumo e produção de mensagens AMQP;
* [Server Side Events](https://en.wikipedia.org/wiki/Server-sent_events): Possibilidade de eventos de um endpoint que implementa Server Side Events.
* [HTTP](https://pt.wikipedia.org/wiki/Hypertext_Transfer_Protocol): Possibilidade de receber dados via requisições HTTP


# Incompatibilidades

Atualmente, pelo fato o asyncworker usar o [aiologger](https://github.com/b2wdigital/aiologger), ele é incompatível com apps que usam **múltiplos** loops de evento. Ou seja, se sua app cria um novo loop e substitui o loop anterior isso causará um problema com os logs gerados pelo asyncworker (via aiologger).

No geral, as aplicações assíncronas usam apenas um loop de evento durante todo o seu ciclo de vida. Isso significa que a não se que você esteja escrevendo um código com um comportamento muito específico (que dependa da renovação do loop de eventos) você não terá maiores problemas em usar o asyncworker.

Essa incompatibilidade do aiologger está sendo tratada na issue [#35](https://github.com/b2wdigital/aiologger/issues/35).

## Escrevendo testes

Por causa dessa incompatibilidade com múltiplos loops para escrever testes você precisa ter certeza que seu test runner não está criando novos loops para cada um dos casos de teste sendo rodados. Por padrão o [asynctest](https://github.com/Martiusweb/asynctest) faz isso. No caso do asyntest, basta adicionar um atributo `use_default_loop = True` (doc [aqui](https://asynctest.readthedocs.io/en/latest/asynctest.case.html#asynctest.TestCase.use_default_loop)) em sua classe de teste.

## Exemplos

### Worker lendo dados de um RabbitMQ

```python

from asyncworker import App, RouteTypes
from asyncworker.connections import AMQPConnection


amqp_conn = AMQPConnection(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)
app = App(connections=[amqp_conn])

@app.route(["asgard/counts", "asgard/counts/errors"],
           type=RouteTypes.AMQP_RABBITMQ,
           vhost="fluentd")
async def drain_handler(message):
    print(message)

```

Nesse exemplo, o handler `drain_handler()` recebe mensagens de ambas as filas: `asgard/counts` e `asgard/counts/errors`.

Se o handler lançar alguma exception, a mensagem é automaticamente devolvida para a fila (reject com requeue=True);
Se o handler rodar sem erros, a mensagem é automaticamente confirmada (ack).

### Worker lendo dados de um endpoint Server Side Events

```python
from asyncworker import App, RouteTypes, Options
from asyncworker.connections import SSEConnection


sse_conn = SSEConnection(url="http://172.18.0.31:8080/")
app = App(connections=[sse_conn])

@app.route(["/v2/events"], type=RouteTypes.SSE, options={Options.BULK_SIZE: 2})
async def _on_event(events):
    import json
    event_names = [e.name for e in events]
    print(f"Events received: {len(events)} {event_names}")
    for event in events:
        data = ""
        if event.name == 'deployment_info':
            data = event.body['plan']['id']
        if event.name == 'deployment_success':
            data = event.body['id']
        if event.name == 'status_update_event':
            data = f"app={event.body['appId']}, task={event.body['taskId']} ({event.body['taskStatus']})"

        print(f"Event Received: {event.name} {data}")
```

Nesse exemplo, o handler `_on_event()` recebe os eventos enviados pelo servidor. O objeto `events` é sempre uma lista, mesmo quando estamos usando `BULK_SIZE=1` (Falaremos sobre isso mais a frente)

### Worker lendo dados de requisições HTTP
```python
from aiohttp import web
from asyncworker import App, RouteTypes

# ...

@app.route(routes=['/', '/hello'], methods=['GET'], type=RouteTypes.HTTP)
async def index(request: web.Request) -> web.Response:
    return web.Response(body="Hello world")
```

Nesse exemplo, declaramos um handler `index`, que receberá uma instância de
`aiohttp.web.Request` para cada acesso as rotas `GET /` e `GET /hello`.

### Rodando esses códigos

Ambos os exemplos precisam de um `main()` para poderem rodar. Um exemplo de `main` seria o seguinte, assumindo que o objeto `app` está no módulo `myworker`:

```python

from myworker import app

app.run()

```

Nesse ponto sua app já estará rodando e caso você seja desconectado, um loop ficará tentanto reconectar. A cada erro de conexão um log de exception é gerado.

A seguir temos documentações específicas sobre cada backend implementado


# RabbitMQ

## Rejeitando uma mensagem e não colocando-a de volta na fila

Opcionalmente, caso seja necessário rejeitar uma mensagem e ao mesmo tempo **não** devolver essa mensagem pra fila,
podemos chamar `message.reject(requeue=False)`. O valor default do `requeue` é `True`.

## Configurações de ação padrão em caso de sucesso e exception

É possível escolher o que o asynworker fará com as mensagens em caso de sucesso (handler executa sem lançar exceção)
ou em caso de falha (handler lança uma exception não tratada).

As opções são: Events.ON_SUCCESS e Events.ON_EXCEPTION. Ambas são passadas a cada rota de consumo registrada, ex:

```python
from asyncworker.options import Events, Actions, RouteTypes

@app.route(["queue1", "queue2"],
            type=RouteTypes.AMQP_RABBITMQ,
            options={
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

### Publicando uma mensagem em outra fila

Não é incomum termos a necessidade de criar `consumers` que também são `producers`.
Pra isso, o asyncworker expõe o objeto `AMQPConnection`. Por exemplo, em um
cenário onde consumimos da fila `queue1`  e queremos publicar na fila `queue2`,
que tem bindings com a routing key `queue2_routing_key` e o
exchange `queue2_exchange`:

```python

from asyncworker.options import RouteTypes

@app.route(["queue1", "queue2"], type=RouteTypes.AMQP_RABBITMQ)
async def handler(messages):
    await app[RouteTypes.AMQP_RABBITMQ]['connection'].put(
        body={"dog": "Xablau"},
        routing_key="queue2_routing_key",
        exchange="queue2_exchange",
    )

```

Caso o nosso producer precise publicar em uma fila em outro [virtual host](https://www.rabbitmq.com/vhosts.html),
basta expecificar o nome do virtual host:

```python

from asyncworker.options import RouteTypes

@app.route(["queue1", "queue2"], type=RouteTypes.AMQP_RABBITMQ)
async def handler(messages):
    await app['rabbitmq_connection'].put(
        body={"dog": "Xablau"},
        routing_key="queue2_routing_key",
        exchange="queue2_exchange",
        vhost="b"
    )

```

Se necessário, o asyncworker vai se encarregar de abrir uma nova conexão com
esse virtual host utilizando as credenciais já passadas na inicialização da `App`.

# Server Side Events


## Recebendo dados em lote

o async-worker permite que você receba seus dados em lotes de tamanho definido por você. A forma de escolher esse lote é atrávez da opção `Options.BULK_SIZE`.
Essa opção é passada para cada um dos handlers, individualmente. O default é `BULK_SIZE=1`.

## Escolhendo o tamanho do BULK que será usado

Assumindo que nossa `app` já está criada. Independente de qual tipo de app é, o decorator `@app.route()` recebe um kwarg chamado `options` onde podemos passar o BULK_SIZE, assim:

```python
from asyncworker.options import Options

@app.route(..., options={Options.BULK_SIZE: 1000})
async def _handler(dat):
    for m in messages:
      logger.info(message.body)

```

Nesse exemplo, o `_handler` só será chamado quando o async-worker tiver, **já nas mãos**, 1000 itens. Os 1000 itens serão passados de uma única vez para o handler, em uma lista.

#### Flush timeout

Com o flush timeout a `app` não necessita ficar presa esperando o bucket encher para conseguir processar as mensagens.
Após o tempo do `FLUSH_TIMEOUT`, que são 60 segundos por default, a `app` irá enviar todas as mensagens que já possui para o `_handler`.
Por exemplo, se tivermos um `handler` que possui
 - Um `BULK_SIZE` de 1.000
 - As mensagens para esse handles são publicadas diariamente
 - E o bucket desse handler ficou com 500 mensagens

Nesse caso a `app` irá esperar o timeout do flush para liberar essas mensagens para o `handler`.

Caso queria alterar o tempo default do timeout do flush basta definir env `ASYNCWORKER_FLUSH_TIMEOUT` com um número que representara os segundos em que a app irá esperar para realizar o flush

# HTTP (0.6.0+)

Atualmente, uma das formas mais comuns comunicação entre aplicações é HTTP,
e com o async-worker você também consegue utilizar esse protocolo nos seus handlers.

## Declarando uma rota

```python
from aiohttp import web
from asyncworker import App, RouteTypes
from asyncworker.connections import AMQPConnection


amqp_conn = AMQPConnection(host="localhost", user="guest", password="guest", prefetch_count=1024)
app = App(connections=[amqp_conn])


@app.route(routes=['/', '/hello'], methods=['GET'], type=RouteTypes.HTTP)
async def index(request: web.Request) -> web.Response:
    return web.Response(body="Hello world")


@app.route(routes=["words_to_index"], type=RouteTypes.AMQP_RABBITMQ)
async def drain_handler(messages):
    print(messages)


app.run()
```

Os parâmetros `routes` e `methods` são listas, ou seja, um mesmo handler
pode atender múltiplos métodos e múltiplas rotas.

Por padrão, fazemos o binding em `127.0.0.1:8080`, mas isso pode ser alterado
com as envvars `ASYNCWORKER_HTTP_HOST` e `ASYNCWORKER_HTTP_PORT`.

# Compartilhamento de dados e inicializações assíncronas

Recomendamos que com o `asyncworker` você não utilize variáveis globais e que
utilize o estado do `asyncworker.App` para manter os seus
"[singletons](https://pt.wikipedia.org/wiki/Singleton)". Para isso, o `asyncworker.App`
disponibiliza _hooks_ para que códigos sejam injetados ao longo ciclo de vida
da aplicação, tornando possível a manutenção, manipulação e compartilhamento de
estado pelos handlers.

## Armazenando na App

Para armazenar estados globais da aplicação, podemos utilizar a instância de
`asyncworker.App`, que age como um dicionário.

```python
app['processed_messages'] = 0
```
Então você poderá utilizá-los nos seus handlers

 ```python
@app.route(routes=["words_to_index"], type=RouteTypes.AMQP_RABBITMQ)
async def drain_handler(messages):
    app['processed_messages'] += 1
```
**Obs.:** Vale lembrar que esse dicionário é compartilhado ao longo de toda app
e utilizado inclusive pelo próprio asyncworker, então uma boa prática é escolher
nomes únicos para evitar conflitos.

## @app.run_on_startup

Um cenário bem comum em workers é, por exemplo, a necessidade de se manter e
compartilhar uma conexão persistente com um banco de dados. Em clientes
assíncronos, é comum a necessidade da inicialização de conexões que necessitam
de um loop de eventos rodando. Para esses cenários, usamos o evento de
`on_startup` da aplicação:

```python
import aioredis
from asyncworker import App

# ...

@app.run_on_startup
async def init_redis(app):
    app['redis'] = await aioredis.create_pool('redis://localhost')


app.run()
```

## @app.run_on_shutdown

Assim como o evento de `on_startup` sinaliza a inicialização do ciclo de vida
da app, o evento `on_shutdown` representa o fim. Um caso de uso comum, é fazer
o processo de finalização de conexões abertas. Como no exemplo anterior
abrimos uma conexão com o [Redis](https://redis.io), utilizando a biblioteca
[aioredis](https://github.com/aio-libs/aioredis), precisamos fechar as conexões
criadas:

```python
@app.run_on_shutdown
async def init_redis(app):
    app['redis'].close()
    await app['redis'].wait_closed()
```

# Observações adicionais

### BULK_SIZE e o backend RabbitMQ

O valor do BULK_SIZE sempre é escolhido com a fórmula: `min(BULK_SIZE, PREFRETCH)`. Isso para evitar que o código fique em um deadlock, onde ao mesmo tempo que ele aguarda o bulk encher para poder pegar mais mensagens da fila, ele está aguardando o bulk esvaziar para pegar mais mensagens da fila.

# Atualizando o async-worker no seu projeto

# 0.5.x -> 0.6.0

Nessa versão, tornamos obrigatório o uso do  qenumerator `RouteTypes` e a
assinatura de `app.route` mudou. Ex.:

```python
from asyncworker.models import RouteTypes

@app.route(['/sse'], type=RouteTypes.SSE)
async def event_handler(events):
    pass
```


## 0.1.x -> 0.2.0

Na versão `0.2.0` criamos a possibilidade de receber mensagens em lote. E a partir dessa versão
a assinatura do handler mudo para:

```python
from asyncworker.rabbitmq.message import RabbitMQMessage

async def handler(messages: List[RabbitMQMessage]):
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

# Utils
## Timeit (0.3.0+)

### Gerenciador de contexto

Um gerenciador de contexto para marcar o tempo de execução de código e chamar
um callback `Callable[..., Coroutine]`
assíncrono ao final, com o tempo total de execução.

```python
import asyncio
from asyncworker.utils import Timeit


async def log_callback(**kwargs):
    print(kwargs)
    # >>> {'transactions': {'xablau': 1.0028090476989746}, 'exc_type': None, 'exc_val': None, 'exc_tb': None}


async def main():
    async with Timeit(name="xablau", callback=log_callback):
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Caso uma exceção seja levantada dentro do contexto, `log_callback` será chamado
com os dados da exceção explicitamente.


```python
import asyncio
from asyncworker.utils import Timeit


async def log_callback(**kwargs):
    print(kwargs)
    # >>> {'transactions': {'xablau': 3.0994415283203125e-06}, 'exc_type': <class 'KeyError'>, 'exc_val': KeyError('error',), 'exc_tb': <traceback object at 0x10c10c7c8>}


async def main():
    async with Timeit(name="xablau", callback=log_callback):
        raise KeyError("error")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

### Decorator

Também é possível utilizar `Timeit` como um decorator:

```python
# ...

@app.route(["xablau-queue"], type=RouteTypes.AMQP_RABBITMQ, vhost="/")
@Timeit(name="xablau-access-time", callback=log_callback)
async def drain_handler(message):
    await access_some_remote_content()
```

### Múltiplas transações (0.4.0+)

Muitas vezes queremos ter várias métricas ao mesmo tempo para contar o tempo
dentro de um mesmo contexto de execução. Para isso, uma mesma instância pode
receber múltiplas chamadas.

```python
async def printit(**kwargs):
    print(kwargs)
    # >>> {'transactions': {'c': 0.10274815559387207, 'b': 0.20585179328918457, 'a': 0.3061490058898926}, 'exc_type': None, 'exc_val': None, 'exc_tb': None}


async def foo():
    async with Timeit(name='a', callback=printit) as timeit:
        await asyncio.sleep(.1)
        async with timeit(name='b'):
            await asyncio.sleep(.1)
            async with timeit(name='c'):
                await asyncio.sleep(.1)
```
