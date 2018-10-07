
[![Build Status](https://travis-ci.org/B2W-BIT/async-worker.svg?branch=master)](https://travis-ci.org/B2W-BIT/async-worker)
[![codecov](https://codecov.io/gh/B2W-BIT/async-worker/branch/master/graph/badge.svg)](https://codecov.io/gh/B2W-BIT/async-worker)

# Async Worker  
  
## Purpose  
  
To be a microframework (inspired in flask) to facilitate the code of asynchronous workers.   
Nowadays, the project supports the following backends:  
  
* [RabbitMQ](https://www.rabbitmq.com/): Only to read messages. The implementation of publish messages will be done in #9;  
* [Server Side Events](https://en.wikipedia.org/wiki/Server-sent_events): Possibilities of endpoint events that implements Server Side Events.  
  
## Examples  
  
### Worker reading data from RabbitMQ  

```python

from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def drain_handler(message):
    logger.info(message)

```

In this example, the handler `drain_handler()` receives messages from both queues:   
`asgard/counts` and `asgard/counts/errors`  
  
If the handler throws an exception, the message is automatically putted back into the same queue (reject with requeue = True);  
  
If the handler run without erros, the message is automatically confirmed (ack).  
  
### Worker reading data from a Server Side Events endpoint  
  
```python

from asyncworker.sse.app import SSEApplication
import logging

app = SSEApplication(url="http://172.18.0.31:8080/", logger=logging.getLogger())

@app.route(["/v2/events"], options={Options.BULK_SIZE: 2})
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
  
In this example, the handler  `_on_event()` receives the events sent from server. The object `events` is always a list, even if we are using `BULK_SIZE=1` (We will talk about that further).  
  
### Running these codes  
  
Both examples need a `main()` to be able to run. Some example of `main` will be the following, assuming that the `app` object is inside `myworker` module:  
  
```python  
  
from myworker import app  
  
app.run()  
  
```  
At this point your app will be running. In case of being disconnected, a loop will be trying to reconnect. For every connection error, an exception log is generated.  
  
Next, we have specific documentations about every backend implemented.  
  
  
# RabbitMQ  
  
## Rejecting a message and not putting back in queue   
Optionally,  in case of being necessary to reject a message and in the same time **not** putting back in queue, we could call `message.reject(requeue=False)`. The default value of `requeue` is `True`.  
  
##  Default action configurations in case of success and exception  
  
It is possibible to chose what asyncwork will do with the messages in case of success (handler executes without throw an exception) or in case of failure (handler throws an untreated exception).   
  
The options are: `Events.ON_SUCCESS` and `Events.ON_EXCEPTION`. Both are passed in each registered consume route, example:  
  
```python
from asynworker.options import Events, Actions

@app.route(["queue1", "queue2"], options={
                                  Events.ON_SUCCESS: Actions.ACK,
                                  Events.ON_EXCEPTION: Actions.REJECT,
                                  })
async def handler(messages):
    ...
```
  
In this case, if the handler runs with success, all the messages will respond with `ACK`.  On the other hand, if an untreated exception was caught by asyncworker, it will respond with `REJECT`.   
  
### Possible options  
  
 - `Actions.ACK`: Confirms the message to RabbitMQ   
 - `Actions.REJECT`: Rejects the message and **does not put back** into the origin queue  
 - `Actions.REQUEUE`: Rejects the message and **puts back** into the origin queue  
   
### Overwriting the default action only for some messages   
It is possible to chose an action different from default to every message in the bulk that was delivered to the handler. For this, it's necessary to call one of the methods from the `RabbitMQMessage` object. They are:  
  
 - `.accept()`: Marks the message to be confirmed to the RabbitMQ   
 - `.reject(requeue=False)`: Marks the message to be reject and **does not put back** into the origin queue  
 - `.reject(requeue=True)`: Marks the message to be reject and **puts back** into the origin queue   
  
The default value to  `.reject()` is `requeue=True`.  
  
  
# Server Side Events   
  
# Receiving batch data   

The async-worker allows that you receive your batch data in sizes defined by you. You can define and chose this batch through the option `Options.BULK_SIZE`.  
This option is passed individually to each of handlers. The default is `BULK_SIZE=1`.  
  
## Choosing the BULK size that will be used  
  
Assuming that our `app` is already created, independent of what type the app is, the decorator `@app.route()` receives a *kward* called `options` where we can pass the BULK_SIZE as you can see in the example below:  
  
```python
from asyncworker.options import Options

@app.route(..., options={Options.BULK_SIZE: 1000})
async def _handler(dat):
    for m in messages:
      logger.info(message.body)

```  
In this example, the  `_handler` only will be called when the *async-worker* had, **in its hands**, 1000 items. The 10000 items will be passed once to the handler in a list.  
  
### BULK_SIZE and the backend RabbitMQ  
  
The value of BULK_SIZE is always chosen with the formula: `min(BULK_SIZE, PREFRETCH)`. This is necessary to avoid that the code stays in a deadlock, where in the same time that it waits the bulk flood, it is waiting the bulk stays empty to get more messages in the queue.  
   
## Updating the async-worker in your project  
  
### 0.1.x > 0.2.0  
  
In version `0.2.0`, we create the possibility to receive bulk messages. For this version and later,  the handler signature has changed to:  
  

```python
from asyncworker.rabbitmq.message import Message

async def handler(messages: List[Message]):
  pass
```
  
The instances of `asyncworker.rabbitmq.RabbitMQMessage` object are already configured by default to receive `ack()` after the handler returns (without exception). However, the handler can change it calling `message.reject()` method to each message that needs to be putted back in queue.  
  
The original content from message is now in `message.body` attribute. So, an old handler that was written in this way:  
  

```python
from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=256)

@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def drain_handler(message):
    logger.info(message)

```
  
transforms into:  
  
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
  
### Context Manager  
  
A context manager to measure execution time of the code and call an asynchronous callback `Callable[..., Coroutine]` in the end with the total execution time.  
  
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

If an exception is raised inside the context, `log_callback` will be called with the exception data explicitly.  

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
  
It is also possible to use `Timeit` as a decorator:  
  
```python
# ...

@app.route(["xablau-queue"], vhost="/")
@Timeit(name="xablau-access-time", callback=log_callback)
async def drain_handler(message):
    await access_some_remote_content()
```
  
### Multiple transactions (0.4.0+)  
  
Frequently we want to have many metrics, simultaneously, to count the time inside the same execution context. To do that, the same instance can receive multiples calls.  
  
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
