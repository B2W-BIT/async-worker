Search.setIndex({docnames:["changelog/index","changelog/v0.10.0","changelog/v0.10.1","changelog/v0.11.0","changelog/v0.11.1","changelog/v0.11.2","changelog/v0.11.3","changelog/v0.11.4","changelog/v0.11.5","changelog/v0.12.0","changelog/v0.12.1","devguide/custom-decorators","devguide/index","devguide/tests","incompat","index","intro","src/asyncworker/asyncworker","src/asyncworker/asyncworker.connections","src/asyncworker/asyncworker.easyqueue","src/asyncworker/asyncworker.exceptions","src/asyncworker/asyncworker.http","src/asyncworker/asyncworker.rabbitmq","src/asyncworker/asyncworker.signals","src/asyncworker/asyncworker.signals.handlers","src/asyncworker/asyncworker.sse","src/asyncworker/asyncworker.testing","src/asyncworker/asyncworker.types","src/asyncworker/modules","userguide/asyncworker-app/hooks","userguide/asyncworker-app/index","userguide/asyncworker-app/intro","userguide/asyncworker-app/storage","userguide/handlers/http/doc","userguide/handlers/http/index","userguide/handlers/index","userguide/handlers/rabbitmq","userguide/index","userguide/quickstart","userguide/updates/index","userguide/utils/index","userguide/utils/run_every","userguide/utils/timeit","versions"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["changelog/index.rst","changelog/v0.10.0.rst","changelog/v0.10.1.rst","changelog/v0.11.0.rst","changelog/v0.11.1.rst","changelog/v0.11.2.rst","changelog/v0.11.3.rst","changelog/v0.11.4.rst","changelog/v0.11.5.rst","changelog/v0.12.0.rst","changelog/v0.12.1.rst","devguide/custom-decorators.rst","devguide/index.rst","devguide/tests.rst","incompat.rst","index.rst","intro.rst","src/asyncworker/asyncworker.rst","src/asyncworker/asyncworker.connections.rst","src/asyncworker/asyncworker.easyqueue.rst","src/asyncworker/asyncworker.exceptions.rst","src/asyncworker/asyncworker.http.rst","src/asyncworker/asyncworker.rabbitmq.rst","src/asyncworker/asyncworker.signals.rst","src/asyncworker/asyncworker.signals.handlers.rst","src/asyncworker/asyncworker.sse.rst","src/asyncworker/asyncworker.testing.rst","src/asyncworker/asyncworker.types.rst","src/asyncworker/modules.rst","userguide/asyncworker-app/hooks.rst","userguide/asyncworker-app/index.rst","userguide/asyncworker-app/intro.rst","userguide/asyncworker-app/storage.rst","userguide/handlers/http/doc.rst","userguide/handlers/http/index.rst","userguide/handlers/index.rst","userguide/handlers/rabbitmq.rst","userguide/index.rst","userguide/quickstart.rst","userguide/updates/index.rst","userguide/utils/index.rst","userguide/utils/run_every.rst","userguide/utils/timeit.rst","versions.rst"],objects:{"":{asyncworker:[17,0,0,"-"]},"asyncworker.app":{App:[17,1,1,""]},"asyncworker.app.App":{freeze:[17,2,1,""],get_connection:[17,2,1,""],get_connection_for_route:[17,2,1,""],handlers:[17,3,1,""],route:[17,2,1,""],run:[17,2,1,""],run_every:[17,2,1,""],run_on_shutdown:[17,2,1,""],run_on_startup:[17,2,1,""],shutdown:[17,2,1,""],shutdown_os_signals:[17,3,1,""],startup:[17,2,1,""]},"asyncworker.bucket":{Bucket:[17,1,1,""],BucketFullException:[17,4,1,""]},"asyncworker.bucket.Bucket":{is_empty:[17,2,1,""],is_full:[17,2,1,""],pop_all:[17,2,1,""],put:[17,2,1,""],used:[17,2,1,""]},"asyncworker.conf":{Settings:[17,1,1,""]},"asyncworker.conf.Settings":{Config:[17,1,1,""]},"asyncworker.conf.Settings.Config":{allow_mutation:[17,3,1,""],env_prefix:[17,3,1,""]},"asyncworker.connections":{AMQPConnection:[18,1,1,""],Connection:[18,1,1,""],ConnectionsMapping:[18,1,1,""],SSEConnection:[18,1,1,""]},"asyncworker.connections.AMQPConnection":{Config:[18,1,1,""],items:[18,2,1,""],keys:[18,2,1,""],put:[18,2,1,""],register:[18,2,1,""],set_connections:[18,2,1,""],values:[18,2,1,""]},"asyncworker.connections.AMQPConnection.Config":{arbitrary_types_allowed:[18,3,1,""]},"asyncworker.connections.ConnectionsMapping":{add:[18,2,1,""],with_type:[18,2,1,""]},"asyncworker.consumer":{Consumer:[17,1,1,""]},"asyncworker.consumer.Consumer":{consume_all_queues:[17,2,1,""],keep_runnig:[17,2,1,""],on_before_start_consumption:[17,2,1,""],on_connection_error:[17,2,1,""],on_consumption_start:[17,2,1,""],on_message_handle_error:[17,2,1,""],on_queue_error:[17,2,1,""],on_queue_message:[17,2,1,""],queue_name:[17,2,1,""],start:[17,2,1,""]},"asyncworker.easyqueue":{connection:[19,0,0,"-"],exceptions:[19,0,0,"-"],message:[19,0,0,"-"],queue:[19,0,0,"-"]},"asyncworker.easyqueue.connection":{AMQPConnection:[19,1,1,""]},"asyncworker.easyqueue.connection.AMQPConnection":{close:[19,2,1,""],connection_parameters:[19,2,1,""],is_connected:[19,2,1,""]},"asyncworker.easyqueue.exceptions":{EmptyQueueException:[19,4,1,""],InvalidMessageSizeException:[19,4,1,""],MessageError:[19,4,1,""],UndecodableMessageException:[19,4,1,""]},"asyncworker.easyqueue.message":{AMQPMessage:[19,1,1,""]},"asyncworker.easyqueue.message.AMQPMessage":{ack:[19,2,1,""],channel:[19,3,1,""],connection:[19,3,1,""],delivery_tag:[19,3,1,""],deserialized_data:[19,2,1,""],queue_name:[19,3,1,""],reject:[19,2,1,""],serialized_data:[19,3,1,""]},"asyncworker.easyqueue.queue":{BaseJsonQueue:[19,1,1,""],BaseQueue:[19,1,1,""],DeliveryModes:[19,1,1,""],JsonQueue:[19,1,1,""],QueueConsumerDelegate:[19,1,1,""]},"asyncworker.easyqueue.queue.BaseJsonQueue":{content_type:[19,3,1,""],deserialize:[19,2,1,""],serialize:[19,2,1,""]},"asyncworker.easyqueue.queue.BaseQueue":{deserialize:[19,2,1,""],serialize:[19,2,1,""]},"asyncworker.easyqueue.queue.DeliveryModes":{NON_PERSISTENT:[19,3,1,""],PERSISTENT:[19,3,1,""]},"asyncworker.easyqueue.queue.JsonQueue":{consume:[19,2,1,""],deserialize:[19,2,1,""],put:[19,2,1,""],serialize:[19,2,1,""],stop_consumer:[19,2,1,""]},"asyncworker.easyqueue.queue.QueueConsumerDelegate":{on_before_start_consumption:[19,2,1,""],on_connection_error:[19,2,1,""],on_consumption_start:[19,2,1,""],on_message_handle_error:[19,2,1,""],on_queue_message:[19,2,1,""]},"asyncworker.exceptions":{InvalidConnection:[17,4,1,""],InvalidRoute:[17,4,1,""]},"asyncworker.http":{decorators:[21,0,0,"-"]},"asyncworker.http.decorators":{parse_path:[21,5,1,""]},"asyncworker.options":{Actions:[17,1,1,""],AutoNameEnum:[17,1,1,""],DefaultValues:[17,1,1,""],Events:[17,1,1,""],Options:[17,1,1,""],RouteTypes:[17,1,1,""]},"asyncworker.options.Actions":{ACK:[17,3,1,""],REJECT:[17,3,1,""],REQUEUE:[17,3,1,""]},"asyncworker.options.DefaultValues":{BULK_FLUSH_INTERVAL:[17,3,1,""],BULK_SIZE:[17,3,1,""],ON_EXCEPTION:[17,3,1,""],ON_SUCCESS:[17,3,1,""],RUN_EVERY_MAX_CONCURRENCY:[17,3,1,""]},"asyncworker.options.Events":{ON_EXCEPTION:[17,3,1,""],ON_SUCCESS:[17,3,1,""]},"asyncworker.options.Options":{BULK_FLUSH_INTERVAL:[17,3,1,""],BULK_SIZE:[17,3,1,""],CONNECTION_FAIL_CALLBACK:[17,3,1,""],MAX_CONCURRENCY:[17,3,1,""]},"asyncworker.options.RouteTypes":{AMQP_RABBITMQ:[17,3,1,""],HTTP:[17,3,1,""],SSE:[17,3,1,""]},"asyncworker.rabbitmq":{message:[22,0,0,"-"]},"asyncworker.rabbitmq.message":{RabbitMQMessage:[22,1,1,""]},"asyncworker.rabbitmq.message.RabbitMQMessage":{accept:[22,2,1,""],body:[22,2,1,""],process_exception:[22,2,1,""],process_success:[22,2,1,""],reject:[22,2,1,""],serialized_data:[22,2,1,""]},"asyncworker.routes":{AMQPRoute:[17,1,1,""],HTTPRoute:[17,1,1,""],Model:[17,1,1,""],Route:[17,1,1,""],RoutesRegistry:[17,1,1,""],SSERoute:[17,1,1,""],call_http_handler:[17,5,1,""],http_handler_wrapper:[17,5,1,""]},"asyncworker.routes.HTTPRoute":{aiohttp_routes:[17,2,1,""],validate_method:[17,2,1,""]},"asyncworker.routes.Model":{get:[17,2,1,""],keys:[17,2,1,""]},"asyncworker.routes.Route":{factory:[17,2,1,""]},"asyncworker.routes.RoutesRegistry":{add_route:[17,2,1,""],amqp_routes:[17,3,1,""],http_routes:[17,3,1,""],route_for:[17,2,1,""],sse_routes:[17,3,1,""]},"asyncworker.routes.SSERoute":{add_default_headers:[17,2,1,""]},"asyncworker.signals":{base:[23,0,0,"-"],handlers:[24,0,0,"-"]},"asyncworker.signals.base":{Freezable:[23,1,1,""],Signal:[23,1,1,""]},"asyncworker.signals.base.Freezable":{freeze:[23,2,1,""],frozen:[23,2,1,""]},"asyncworker.signals.base.Signal":{send:[23,2,1,""]},"asyncworker.signals.handlers":{base:[24,0,0,"-"],http:[24,0,0,"-"],rabbitmq:[24,0,0,"-"],sse:[24,0,0,"-"]},"asyncworker.signals.handlers.base":{SignalHandler:[24,1,1,""]},"asyncworker.signals.handlers.base.SignalHandler":{shutdown:[24,2,1,""],startup:[24,2,1,""]},"asyncworker.signals.handlers.http":{HTTPServer:[24,1,1,""]},"asyncworker.signals.handlers.http.HTTPServer":{shutdown:[24,2,1,""],startup:[24,2,1,""]},"asyncworker.signals.handlers.rabbitmq":{RabbitMQ:[24,1,1,""]},"asyncworker.signals.handlers.rabbitmq.RabbitMQ":{startup:[24,2,1,""]},"asyncworker.signals.handlers.sse":{SSE:[24,1,1,""]},"asyncworker.signals.handlers.sse.SSE":{startup:[24,2,1,""]},"asyncworker.sse":{consumer:[25,0,0,"-"],message:[25,0,0,"-"]},"asyncworker.sse.consumer":{SSEConsumer:[25,1,1,""],State:[25,1,1,""]},"asyncworker.sse.consumer.SSEConsumer":{interval:[25,3,1,""],keep_runnig:[25,2,1,""],on_connection:[25,2,1,""],on_connection_error:[25,2,1,""],on_event:[25,2,1,""],on_exception:[25,2,1,""],start:[25,2,1,""]},"asyncworker.sse.consumer.State":{EVENT_DATA_FOUND:[25,3,1,""],EVENT_NAME_FOUND:[25,3,1,""],WAIT_FOR_DATA:[25,3,1,""]},"asyncworker.sse.message":{SSEMessage:[25,1,1,""]},"asyncworker.task_runners":{ScheduledTaskRunner:[17,1,1,""]},"asyncworker.task_runners.ScheduledTaskRunner":{can_dispatch_task:[17,2,1,""],start:[17,2,1,""],stop:[17,2,1,""]},"asyncworker.testing":{HttpClientContext:[26,1,1,""],http_client:[26,5,1,""]},"asyncworker.time":{ClockTicker:[17,1,1,""]},"asyncworker.time.ClockTicker":{stop:[17,2,1,""]},"asyncworker.types":{registry:[27,0,0,"-"],resolver:[27,0,0,"-"]},"asyncworker.types.registry":{RegistryItem:[27,1,1,""],TypesRegistry:[27,1,1,""]},"asyncworker.types.registry.TypesRegistry":{get:[27,2,1,""],set:[27,2,1,""]},"asyncworker.types.resolver":{ArgResolver:[27,1,1,""],MissingTypeAnnotationError:[27,4,1,""]},"asyncworker.types.resolver.ArgResolver":{resolve_param:[27,2,1,""],wrap:[27,2,1,""]},"asyncworker.utils":{Timeit:[17,1,1,""],entrypoint:[17,5,1,""]},"asyncworker.utils.Timeit":{TRANSACTIONS_KEY:[17,3,1,""]},asyncworker:{app:[17,0,0,"-"],bucket:[17,0,0,"-"],conf:[17,0,0,"-"],connections:[18,0,0,"-"],consumer:[17,0,0,"-"],easyqueue:[19,0,0,"-"],exceptions:[17,0,0,"-"],http:[21,0,0,"-"],options:[17,0,0,"-"],rabbitmq:[22,0,0,"-"],routes:[17,0,0,"-"],signals:[23,0,0,"-"],sse:[25,0,0,"-"],task_runners:[17,0,0,"-"],testing:[26,0,0,"-"],time:[17,0,0,"-"],types:[27,0,0,"-"],utils:[17,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","exception","Python exception"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:exception","5":"py:function"},terms:{"0994415283203125e":42,"0x10c10c7c8":42,"\u00fanico":32,"\u00fatei":33,"a\u00e7\u00e3o":37,"abstract":[17,19],"ap\u00f3":36,"aplic\u00e1":11,"aplica\u00e7\u00e3o":[9,14,15,29,31,32],"aplica\u00e7\u00f5":14,"ass\u00edncrona":[14,15,30,36,37],"ass\u00edncrono":[14,15,29,42],"at\u00e9":[36,43],"aten\u00e7\u00e3o":43,"atrav\u00e9":[33,34,37],"autentica\u00e7\u00e3o":33,"byte":[17,18,19,25],"c\u00f3digo":[8,11,14,31,32,33,37,38,42,43],"c\u00f3pia":35,"causar\u00e1":14,"cen\u00e1rio":29,"ci\u00eancia":11,"class":[13,15,17,18,19,22,23,24,25,26,27,30,33,36,37,42],"come\u00e7a":31,"compat\u00edvel":[36,43],"comunica\u00e7\u00e3o":36,"conclu\u00edda":36,"conex\u00e3o":[10,29,36,38],"conex\u00f5":[29,31],"conte\u00fado":39,"cria\u00e7\u00e3o":[34,35,36,37],"declara\u00e7\u00e3o":36,"decor\u00e1":33,"default":[17,36],"defini\u00e7\u00e3o":33,"descri\u00e7\u00e3o":2,"dicion\u00e1rio":[32,36],"din\u00e2mico":[11,33],"ent\u00e3o":[32,33,36,39],"enum":[17,25,31,39],"espec\u00edfico":14,"est\u00e1":[13,14,15,31,33,36,38,39,43],"est\u00e3o":[11,31,33,36],"est\u00edmulo":[14,15,31,35],"estar\u00e1":[8,31,34,35,37,38],"estat\u00e3o":36,"exca\u00e7\u00e3o":36,"exce\u00e7\u00e3o":[36,42],"execu\u00e7\u00e3o":[22,36,42],"explica\u00e7\u00e3o":8,"f\u00f3rmula":36,"far\u00e1":31,"far\u00e3o":31,"ficar\u00e1":38,"final":42,"finaliza\u00e7\u00e3o":29,"float":17,"forma\u00e7\u00e3o":43,"fun\u00e7\u00e3o":[11,15,17,35,36,37,40],"fun\u00e7\u00f5":31,"function":11,"funda\u00e7\u00e3o":33,"implementa\u00e7\u00e3o":[8,33],"implementa\u00e7\u00f5":8,"import":[11,29,33,36,38,39,41,42],"in\u00edcio":[15,37],"incompat\u00edvel":[14,43],"informa\u00e7\u00f5":34,"inicializa\u00e7\u00e3o":29,"inicializa\u00e7\u00f5":[15,30,37],"inst\u00e2ncia":[8,31,32,33,34,36,38,39,42],"instru\u00edmo":33,"int":[17,19,22,33,36],"integra\u00e7\u00e3o":2,"intermedi\u00e1rio":11,"introdu\u00e7\u00e3o":15,"ir\u00e1":36,"lan\u00e7ar":[36,38],"m\u00e1ximo":36,"m\u00e9todo":[1,17,31,33,36,39,41],"m\u00e9trica":42,"m\u00f3dulo":[31,33,38],"m\u00faltipla":[37,40],"m\u00faltiplo":[13,14,31],"manipula\u00e7\u00e3o":32,"manuten\u00e7\u00e3o":32,"mudan\u00e7a":[39,43],"n\u00e3o":[2,8,11,13,14,17,32,33,35,36],"n\u00edvel":33,"n\u00famero":36,"necess\u00e1rio":[11,31,36],"new":[6,17,18,19,33,34,42],"obrigat\u00f3rio":[31,39],"op\u00e7\u00f5":[31,36],"p\u00f3s":39,"padr\u00e3o":[13,33,36,39],"par\u00e2metro":[31,34,35,36,37],"parametriza\u00e7\u00e3o":[34,35,37],"poder\u00e1":[32,35,36],"poss\u00edvei":31,"poss\u00edvel":[11,32,33,36,38,42],"pr\u00e1tica":32,"pr\u00e9via":36,"pr\u00f3prio":[11,32],"preced\u00eancia":36,"precisar\u00e1":33,"r\u00e1pido":[15,37],"raz\u00e3o":11,"receber\u00e1":[36,38],"recomenda\u00e7\u00e3o":8,"renova\u00e7\u00e3o":14,"representar\u00e1":36,"requisi\u00e7\u00e3o":[15,33,38],"requisi\u00e7\u00f5":[34,37],"resolu\u00e7\u00e3o":[11,33],"respons\u00e1vel":33,"return":[11,17,18,19,33,34,38],"s\u00e3o":[31,34,35,36,37],"s\u00f3lido":17,"saber\u00e1":[11,33],"ser\u00e1":[8,17,22,31,33,35,37,41,42,43],"ser\u00e3o":[31,33],"servir\u00e1":33,"situa\u00e7\u00f5":36,"static":17,"tamb\u00e9m":[31,33,36,42],"tentar\u00e1":33,"ter\u00e1":[14,43],"transa\u00e7\u00f5":[37,40],"trav\u00e9":33,"true":[13,17,18,22,36,38],"unit\u00e1rio":[12,15],"usu\u00e1rio":33,"utilit\u00e1rio":[15,37],"utilit\u00e1tio":41,"utiliz\u00e1":32,"v\u00e1lido":33,"v\u00e1ria":[14,15,42],"v\u00eam":39,"vari\u00e1vei":[32,33],"vari\u00e1vel":36,"ver\u00e1":36,"vers\u00e3o":[4,8,9,39,43],"vers\u00f5":[8,9,15,39],"ves\u00f5":39,"voc\u00ea":[8,9,13,14,15,31,32,33,35,36,38,39,43],Adding:6,Ele:31,Eles:33,Obs:32,THe:17,The:[17,19],Useful:19,__call__:33,_amqprouteopt:36,_asyncio:17,_handler:36,_hooks_:32,_id:33,_on_ev:38,_type:27,_wrapper:[11,33],abaixo:[15,35],abc:[17,18],aberta:29,abrimo:29,abstracteventloop:19,accept:[22,36],access:42,access_some_remote_cont:42,acessando:36,acesso:38,ack:[17,19,22,36,38,39],acordo:35,act:17,action:[17,22,36],add:[17,18],add_default_head:17,add_rout:17,adiciona:33,adicionado:33,adicionai:37,adicionando:[1,8],adicionar:[1,8,13],age:32,agora:39,aguarda:36,aguardando:36,ainda:[8,33,43],aioamqp:[6,19],aiohttp:[8,17,33,34,38,43],aiohttp_rout:17,aiologg:[9,14],aioredi:29,ajust:[8,43],ajustar:43,algum:33,alguma:[11,33,36,38,43],algun:[33,35,36],all:[17,18,19,23],allow:[17,18],allow_mut:17,along:17,also:[17,18],alterado:33,alterar:36,amba:[36,38],ambient:36,ambo:38,amqp_conn:[36,38],amqp_messag:[22,36],amqp_rabbitmq:[17,32,36,38,42],amqp_rout:17,amqpconnect:[17,18,19,37,38],amqpmessag:[17,19,22,36],amqprout:17,ancestr:[17,18],ani:[17,18,19,23,27],anotar:41,anoth:36,another_exchang:36,ant:[29,33],anterior:[14,29],antigo:[39,43],apena:[11,14,34,35,36,37,43],aplicado:[11,33],aplicando:[8,12,15],app:[3,11,14,15,24,26,28,33,34,36,37,38,41,42],appid:38,applic:[17,19],aqui:[11,13,33,34,36,39],arbitrary_types_allow:[17,18],arg:23,argresolv:27,argument:[17,19,23],armazenando:[30,37],armazenar:32,asgard:[36,38,39],assim:[11,29,33,36,38,39],assinatura:[31,33,36,39],assumindo:38,async:[11,15,17,18,19,22,23,24,25,29,32,33,34,36,38,39,41,42],asyncio:[17,19,23,42],asynciter:17,asyncowk:[15,31,33],asynctest:13,asyncwork:[1,8,11,14,29,32,33,34,35,36,37,38,41,42,43],asyncworker_:17,asyncworker_flush_timeout:36,asyncworker_http_host:33,asyncworker_http_port:33,asynqueu:[17,19],asynwork:38,atendar:38,atributo:[13,33,36,39],atual:8,atualizada:[4,43],atualizado:43,atualizamo:9,atualizando:[15,37],atualment:14,aumentada:43,autenticado:33,autenticar:33,auth_requir:33,author:33,auto:[17,18],automat:17,automaticament:[36,38],autonameenum:17,avail:[17,18],await:[11,17,29,33,36,42],b2wdigit:15,badg:8,banco:29,base:[17,18,19,20,22,25,26,27,28],basejsonqueu:19,basemodel:[17,18],basequeu:19,baseset:17,basic_auth:33,basicament:43,basta:[13,33,36,41],befor:[17,19],behav:[17,23],bem:[8,29,34],biblioteca:29,bind:33,boa:32,bodi:[17,19,22,38,39],bool:[17,18,19],boot:31,broker:[10,15,19,36],bucket:[25,28,36],bucket_class:[17,25],bucketfullexcept:17,build:8,bulk:36,bulk_flush_interv:[6,17,36],bulk_siz:[17,37,38],by_id:33,cada:[13,31,35,37,38,39],calabl:7,call:[17,19],call_http_handl:[11,17,33],callabl:[7,17,19,34,35,37,42],callback:[10,17,19,23,42],caminho:43,campo:37,can:19,can_dispatch_task:17,cancel:19,capaz:38,caso:[10,13,29,33,36,38,42],caus:17,causa:[13,35],central:31,cercando:33,certeza:13,chamada:[8,10,17,33,35,36,41,42],chamado:[11,31,33,35,36,42],chamamo:31,chamando:[33,39],chamar:[11,33,36,42],chang:1,changelog:[15,39,43],channel:19,chave:36,chegar:35,chegarmo:43,ciclo:[14,29,32],classifi:8,classmethod:[17,18],client:[19,29],climat:8,clock:17,clocktick:17,close:[19,29],code:[1,6,8,9],codeclim:8,codeown:1,coerent:2,coisa:43,collect:[17,18,23],com:[2,9,10,11,13,14,15,29,31,32,33,34,35,36,38,39,41,42,43],comando:38,commit:[3,4,5,6,7,8,9,10],common:[17,18],como:[7,8,14,15,29,31,32,33,34,35,36,42,43],compartilhado:32,compartilhamento:[15,30,37],compartilhar:29,compat:6,compatibilidad:15,completo:37,complexa:[33,43],complexo:33,comportamento:14,comum:29,condit:[17,20],conduct:6,conectado:31,conectar:36,conf:28,config:[17,18],configurado:39,confirmada:[22,36,38],conflito:32,connect:[3,20,23,28,31,36,38],connection_fail_callback:[17,19,36],connection_paramet:19,connectionsmap:[17,18],consegu:36,conseguir:36,considerada:8,considerado:43,consiga:33,construtor:[31,33,36],consultar:39,consum:[19,28],consume_all_queu:17,consumer_nam:19,consumer_tag:[17,19],consumindo:37,consumpt:[17,19],contar:42,content:28,content_typ:19,conter:33,contexto:[33,37,40],contribut:6,coro:17,coro_ref:27,corotina:[11,33,34],coroutin:[17,19,23,42],correta:11,corretament:[11,33],count:[36,38,39],counter:[17,18],coverag:1,create_pool:29,cria:14,criada:29,criamo:39,criando:[13,30,37],criar:[35,36],curl:38,custom:[17,19],customizado:[8,12,15],dada:37,dado:[15,29,30,33,37,42],das:[31,36,39],data:[8,9,10,17,18,19,23,36,38],deadlock:36,declara:1,declaramo:[31,38],declarar:33,decod:19,decor:[8,12,15,17,18,31,34,35,37,40,41],decorada:[11,33,34],decoramo:33,decorando:11,decorato:33,decortor:36,def:[11,29,32,33,34,36,38,39,41,42],defaultvalu:[17,36],defin:[17,20],definida:36,definido:[31,33],definindo:[30,36,37],definir:36,definit:[17,20],delath:33,dele:[33,34,35],deleg:19,delegate_class:19,delivery_tag:[17,19,22,36],deliverymod:19,demandar:43,dentro:[31,36,42],dep:9,depend:[1,43],dependa:14,dependencia:[2,9],dependento:31,deployment_info:38,deployment_success:38,depoi:[29,33,39],depositada:31,depreciada:[8,17],descartada:[22,36],desconectado:38,desejado:36,desenvolvimento:[15,43],deseri:[17,19],deserialization_method:19,deserialized_data:19,dess:[33,35,36],dessa:[31,36,39,43],destino:36,detalh:[8,15,34,35],deve:[11,17,31,33,36],devem:[11,33],deveremo:33,devolv:36,devolvida:[36,38,39],diariament:36,dict:[17,18,19,25,31,36],diferent:[14,15,35,36],diretament:33,disponibiliza:32,disso:[11,36],diz:36,dizendo:33,dizer:31,doc:[1,6,13,34],document:7,documentar:17,dog:36,doi:[33,43],dos:[11,13,31,36],drain_handl:[32,36,38,39,42],dua:[9,43],durant:[14,36],dure:[17,19],each:[17,18],easyqueu:[1,17,18,22,28,36],econtra:15,efetivament:31,ela:41,ele:[14,33,36],eles:36,emptyqueueexcept:19,enabl:6,encher:36,encontrado:33,encontrando:33,endpoint:37,entando:11,entend:[14,15,35],entrypoint:17,enumer:[17,25],env:[34,35,36,37],env_prefix:17,env_set:17,envelop:19,enviado:38,enviar:36,envvar:33,era:39,erro:[1,10,33,36,38],error:[17,36,38,39,42],escolh:[32,34,35,37],escolhendo:37,escolhido:36,escrev:[11,13,14,15,33,34,36],escrevendo:[12,14,15],escrito:36,escutando:[34,35,37],especi:31,especialment:33,esperando:36,esperar:36,ess:[8,11,17,29,31,32,33,36,38,43],essa:[8,9,11,14,15,17,22,31,33,34,36,41],estado:32,estamo:[33,38],estar:[11,33],estavam:2,esteja:14,estejam:33,estimulado:34,estiv:[17,36],estiver:39,esvaziar:36,event:[15,17,19,23,36,37,39],event_bodi:25,event_data_found:25,event_handl:39,event_nam:[25,38],event_name_found:25,event_raw_bodi:25,evento:[14,15,29,35,38],everi:[17,19],every_5_second:41,evitar:[32,36],exc_tb:42,exc_typ:42,exc_val:42,except:[25,27,28,36,38,39],exchang:[17,18,19,36],executado:31,exemplo:[11,29,33,35,37,38],existem:36,exmeplo:31,experiment:33,explicitament:[33,42],externo:35,extra_registri:27,extrair:[33,34],factori:17,fail:[17,19],fail_handl:36,falar:31,falaremo:38,falha:36,falharam:36,fals:[17,18,19,22,36],falta:43,faremo:33,fato:14,faz:[13,33],fazemo:[33,43],fazendo:8,fazer:[11,29,33,34,39],featur:[1,6,7,8,9],fechar:29,feito:33,ficar:36,ficou:36,fila:[22,31,35,36,37,39],file:5,fim:[22,29,36],fiqu:36,fire:23,fix:8,fixa:36,fixo:[15,37,40],fluentd:[36,38,39],flush:37,flush_timeout:36,foo:42,forma:[31,33],framework:[14,15],freez:[17,23],freezabl:[17,18,23],frent:38,from:[6,11,19,29,33,36,38,39,41,42],frozen:23,funciona:[8,15],functool:11,further:[17,19],futur:17,futura:8,futuro:8,gener:[3,17,18,19],gera:33,gerado:[14,15,38],geral:[14,38],gerenciador:[37,40],get:[11,17,19,27,33,34,38],get_authenticated_us:33,get_connect:17,get_connection_for_rout:17,get_event_loop:42,gitattribut:8,github:15,given:17,globai:[32,33],guardar:33,guest:[36,38,39],guia:15,haja:[10,36],handl:[17,19,36],handlar:31,handler:[7,8,12,15,17,21,22,23,30,32,34,36,37,38,39],handler_error:[17,19],happen:17,header:33,heartbeat:19,hello:38,hook:[1,15,30,37],host:[17,19,36,38,39],hostnam:36,html:34,http:[8,12,15,17,23,31,35,37],http_client:[17,26],http_handler_wrapp:17,http_request:11,http_rout:17,httpclientcontext:[17,26],httprout:17,httpserver:[17,24],httpstatu:33,ideia:38,identifi:19,immedi:[17,18,19],implement:[17,19,23],implementa:7,important:33,inclus:32,incompatibilidad:[13,15],indeterminado:[14,15],index:[15,38],indica:[22,36],individualment:37,info:39,inicializada:29,init_redi:29,initi:[17,19],injetado:32,inner:11,insert:1,insid:17,instanc:[17,19],instancia:33,instanciado:33,inteiro:36,interessa:33,interv:[17,25],intervalo:[15,37,40],invalid:[17,20],invalidconnect:[17,20],invalidmessagesizeexcept:19,invalidrout:[17,20],is_connect:19,is_empti:17,is_ful:17,isn:19,isso:[8,11,13,14,15,31,32,33,35,36,38,39,42,43],issu:[1,14],item:[17,18],iter:[17,18,31],json:[19,38],json_respons:[11,33,34,38],jsonqueu:[17,18,19],junto:11,keep:[17,18],keep_runnig:[17,25],kei:[17,18,19,36],keyerror:42,kwarg:[1,17,19,23,31,42],languag:8,lembrando:43,lembrar:32,len:38,lendo:37,levantada:42,liberar:36,licens:5,lidando:33,like:[17,36],linha:[38,43],list:[17,18,23,25,36,39],lista:[11,31,33,35,36,38,39],localhost:29,lock:23,log:[14,19,38],log_callback:42,logger:[19,39],longo:[32,43],loop:[13,14,17,19,29,38,42],los:[11,32],lote:39,mai:[2,8,11,15,17,19,34,35,37,38,43],main:[17,18,38,42],maior:14,mandatori:[17,18,19],mantemo:8,manter:[29,32],manualment:33,map:[17,18],marca:[22,36],marcar:42,mas:[8,33,36,39,43],match:33,max_concurr:17,max_message_length:19,melhor:[8,39],melhorar:1,menor:36,mensagem:[1,15,22,31,35,36,38,39],mensagen:[35,36,38,39],mensgem:37,mesma:[33,42,43],mesmo:[31,33,35,36,38,42],messag:[17,28,32,36,38,39,42],messageerror:[17,19],method:[1,11,23,33,34,38],min:36,minor:43,missingtypeannotationerror:27,model:[17,33,39],modelo:36,modul:[1,15,28],momento:[11,33,36],mostrar:38,mostraremo:34,move:1,msg:[17,19,36],mudam:35,mudamo:43,mudando:2,mudar:39,mudo:39,mudou:39,muita:42,muito:14,multipl:3,mutablemap:17,my_handler_decor:11,myapp:41,myproject:33,mywork:38,nada:36,name:[8,17,18,19,23,38,42],nao:1,necessariament:31,necessidad:[29,33],necessita:36,necessitam:29,need:19,nem:36,nenhum:33,nenhuma:36,ness:[31,33,36,38,41],nessa:[8,9,39],nome:[32,33,36],non_persist:19,none:[17,18,19,25,27,31,42],nos:32,nossa:31,nosso:33,nota:37,notar:33,notif:19,nova:[9,30,35,36,37,43],novo:[13,14,43],obj:27,object:[17,18,19,22,23,24,25,26,27,42],objetivo:[14,15],objeto:[7,11,31,34,35,36,37,38,39,41],obtain:6,occur:17,ocorreu:36,olh:43,olhar:43,on_before_start_consumpt:[17,19],on_connect:25,on_connection_error:[17,19,25],on_consumption_start:[17,19],on_error:19,on_ev:25,on_except:[17,22,25,36],on_message_handle_error:[17,19],on_queue_error:17,on_queue_messag:[17,19],on_shutdown:29,on_startup:[17,29],on_success:[17,22,36],onc:[17,19],ond:[17,31,34,35,36,37],one:19,opcionalment:36,option:[6,18,19,22,27,28,31,37,38],org:34,origem:[31,35],origen:[14,15,31],origin:[22,36,39],original_queu:36,orign:14,other:36,outra:36,outro:[31,36,43],overwritten:[17,19],owner:23,packag:28,page:15,para:[2,4,8,9,11,13,14,15,16,22,29,31,32,34,35,37,38,39,42,43],param:19,param_nam:27,param_typ:27,paramet:[6,17,19],parameter:8,parametro:[11,22,31,33,35,37],parse_path:[21,33],partir:39,pass:[33,36,39],passa:[34,39],passada:36,passado:[33,36],passam:8,passar:33,passarem:8,passaremo:33,passarmo:36,password:[17,19,25,36,38,39],patch:43,path:[31,34,35,37],payload:19,peculiaridad:43,pegando:33,pegar:36,pelo:[11,14,32,33,36,38],permit:[11,29,33,41],permitido:33,persist:19,persistent:29,plan:38,pleno:43,pode:[33,35,36,39,42,43],podem:[14,15,31,33],podemo:[32,34,35,36],poder:[33,36],poderem:38,poderia:11,poi:33,ponto:[31,36,38],pop_al:17,popular:33,por:[13,14,15,29,31,33,35,36,39,43],porqu:35,porta:[34,35,37],posit:1,possa:33,possibilidad:39,possuem:[33,36],possui:36,posui:41,potencialment:43,pra:36,prametro:33,precisa:[13,33,36,43],precisam:[33,38],precisamo:[29,36],precisar:[39,43],precisarem:43,precisarmo:34,preciso:[34,36],prefetch:37,prefetch_count:[17,19,36,38,39],prefretch:36,preparado:8,presa:36,present:33,primeiro:[8,17,31,33],princip:[11,15,30,36,37],print:[36,38,41,42],printit:42,problema:[14,43],process_except:22,process_success:22,processar:36,processed_messag:32,processo:29,procurar:33,program:8,projeto:[2,14,16,43],properti:[17,18,19,22,23],provid:19,publica:36,publicada:36,publish:19,puder:33,put:[17,18,19,36],py38:8,pydant:[2,4,9,17,18,36,43],python:[6,8,14,15],quaisquer:[31,33,43],qual:[31,37],qualquer:[14,15],quando:[1,17,33,34,35,36,38,43],que:[8,9,11,13,14,15,17,29,31,32,34,35,36,37,38,39,41,43],queira:36,quem:[11,31],quer:[33,36],queremo:42,queue:[17,18,28,36,42],queue_nam:[17,19],queueconsumerdeleg:[17,19],rabbitmq:[15,17,23,28,31,35,37,39],rabbitmqmessag:[17,22,36,39],rabitmq:36,rais:[17,19,42],random:19,raw:[3,4,5,6,7,8,9,10,17],readi:[17,19],realizar:36,receb:[8,11,17,31,33,34,35,36,38,39,42],receba:[11,14,15,33],recebam:36,recebem:[11,34,35,37],recebemo:[17,34],recebendo:[8,34,35,36,37],recebida:37,recebido:[33,36],receiv:[17,23,38],recolocada:[22,36],recomendado:[9,43],recomendamo:32,reconectar:38,recorrent:15,redi:29,regist:[17,18,23],registr:29,registra:31,registrada:31,registrado:[33,35],registrando:31,registrar:31,registri:[8,33],registryitem:27,regra:[11,34,35,37],reject:[17,19,22,36,38,39],rejeitada:[22,36],rejeitar:36,releas:[8,9,10],remov:1,removida:8,report:[1,8],representa:[29,31],req:[33,34,38],requer:43,request:[8,9,11,17,31,34,35,37,38],requestwrapp:[8,11,17],requeu:[17,19,22,36,38],resolve_param:27,respectivament:33,respons:[17,18,34,38],resultado:33,retentativa:36,retorna:[33,34],retornada:11,retornar:39,retri:36,retro:43,rodada:41,rodado:[2,13,38],rodando:[15,29,37,40],rodar:[36,38],rodarem:29,rode:[14,15],rota:[31,36,38],rout:[1,6,11,19,20,28,31,32,34,35,37,38,39,42],route_for:[1,17],route_info:[17,25],route_typ:[17,18],routedef:17,routesregistri:[1,17],routetyp:[11,17,18,31,32,33,34,36,38,39,42],routing_kei:[17,18,19,36],run:[17,29,31,38,41],run_everi:[17,41],run_every_max_concurr:17,run_on_shutdown:[17,30,37],run_on_startup:[1,17,30,37],run_until_complet:42,runner:13,saber:[31,43],schedul:17,scheduledtaskrunn:17,search:15,second:17,seconds_between_conn_retri:19,segu:[33,43],seguint:[31,33,36,38,43],seguir:33,segundo:36,seja:[11,14,31,33,36,38,41,42,43],sejam:[31,32],self:33,sem:[33,36,38,39,43],sempr:[11,33,36,38,43],semver:43,send:[19,23],sendo:[2,13,14,33],ser:[2,11,14,15,22,29,31,33,34,35,36,38,39,43],seria:38,serial:19,serializ:19,serialized_data:[17,18,19,22],server:[15,34,35,37],servidor:[15,36,38],set:[17,27,33],set_connect:[17,18],setup:[2,4],seu:[8,11,13,14,31,32,33,35,36,37,43],should:[17,19],shudtdown:[15,30,37],shutdown:[17,24],shutdown_os_sign:17,side:[15,37],sigint:17,signal:[17,18,28],signalhandl:24,significa:[14,33,36,43],significado:31,sigterm:17,simpl:[11,33,34,43],simplesmet:34,sinaliza:29,singleton:32,sintax:33,size:17,sleep:[17,42],sobr:[8,15,30,37,38],someth:17,sourc:[17,18,19,20,21,22,23,24,25,26,27,31,36],sphinx:[1,6],sse:[17,23,28,38,39],sse_conn:38,sse_rout:17,sseconnect:[17,18,38],sseconsum:25,ssemessag:25,sserout:17,stabl:34,stage:[17,19],start:[17,19,25],startup:[15,17,24,30,37],state:25,statu:33,status_update_ev:38,stop:[17,19],stop_consum:19,str:[17,18,19,25,27,31],structur:6,sua:[9,13,14,15,29,30,33,36,37,38,43],subclass:[17,18],submodul:28,subpackag:28,substitui:14,sucesso:[33,36],suficient:33,suport:7,suporta:35,tag:[1,2,3,4,5,6,7,8,9,10,19],take:23,talvez:33,tamanho:36,task:[17,38],task_runn:28,taskid:38,taskstatu:38,teham:36,tem:[11,14,15,31,36],temo:[11,31,33,36],tempo:[14,15,35,36,37,40,42],tentanto:38,tentar:33,tentativa:8,ter:[13,36,42],test:[2,9,12,15,28],tha:23,tick:17,time:[19,28,42],timeit:[15,17,37,40],timeout:37,tipo:[15,31,33,36,37],tivermo:36,toda:[32,33,36,39],todo:[8,14,31,33,36],tomada:36,topo:11,tornamo:39,tornando:32,total:42,traceback:42,track:[17,18],transact:[17,42],transactions_kei:17,tratada:[14,36],tratamento:36,trigger:[17,19],tudo:15,type:[8,11,17,18,19,25,31,32,33,34,36,38,39,42],type_definit:27,typehint:33,types_registri:33,typesregistri:[27,33],uma:[1,8,11,15,29,30,32,33,34,35,37,39,40,42,43],unauthor:33,uncaught:[17,19],undecodablemessageexcept:19,union:[17,18,19,25],unpars:17,updat:[6,8,9],url:[25,38],usa:36,usada:[31,36],usado:[31,33,36],usag:[17,18],usam:14,usamo:29,usando:38,usar:[11,14],use:[8,9,23],use_default_loop:13,used:[17,19],user:[33,36,38,39],user_id:33,userdict:17,userlist:23,usernam:[17,19,25,36],using:23,uso:[15,29,39],util:[28,32,42],utilizado:32,utilizando:29,utilizar:[32,42],vai:[9,33,36,43],vale:32,valid:[17,19],validate_method:17,valor:[33,37,43],valu:[17,18,27],valueerror:[17,19,20],vamo:[17,33],vazia:33,veja:34,vejamo:[33,34],vem:11,ver:35,version:[33,34,42,43],versionamento:43,vez:[2,36],veze:42,vhost:[17,18,36,38,39,42],via:14,vida:[14,29,32],vindo:[34,35,37],virtual:[17,18,36],virtual_host:19,wait:17,wait_clos:29,wait_for_data:25,web:[8,11,17,33,34,38],web_request:17,web_routedef:17,when:[17,19],which:23,with_typ:[17,18],words_to_index:32,worker:[14,15,29,37],world:38,wrap:[11,27],wrapper:[8,9,11,17],xablau:[36,42],xena:36,xxxxxxxxxxxxx:17,zerado:36},titles:["Changelog","0.10.0","0.10.1","0.11.0","0.11.1","0.11.2","0.11.3","0.11.4","0.11.5","0.12.0","0.12.1","Aplicando decorators customizados a um handler HTTP","Guia de desenvolvimento","Escrevendo Testes Unit\u00e1rios","Incompatibilidades","Bem vindos \u00e0 documenta\u00e7\u00e3o oficial do projeto Asyncworker","Introdu\u00e7\u00e3o","asyncworker package","asyncworker.connections package","asyncworker.easyqueue package","asyncworker.exceptions package","asyncworker.http package","asyncworker.rabbitmq package","asyncworker.signals package","asyncworker.signals.handlers package","asyncworker.sse package","asyncworker.testing package","asyncworker.types package","asyncworker","Hooks de startup e shudtdown","Asyncworker App","Sobre a classe principal App","Compartilhamento de dados e inicializa\u00e7\u00f5es ass\u00edncronas","Regras para cria\u00e7\u00e3o de um handler HTTP","HTTP","Tipos de Handlers","RabbitMQ","Guia de uso","In\u00edcio r\u00e1pido","Atualizando sua App Asyncworker","Utilit\u00e1rios","Rodando uma fun\u00e7\u00e3o em um intervalo fixo de tempo","Timeit","Compatibilidade de Vers\u00f5es do asyncowker"],titleterms:{"a\u00e7\u00e3o":36,"ass\u00edncrona":32,"atrav\u00e9":38,"atualiza\u00e7\u00e3o":[8,9,10,43],"c\u00f3digo":36,"class":31,"cria\u00e7\u00e3o":33,"depend\u00eancia":43,"documenta\u00e7\u00e3o":15,"estar\u00e1":33,"fun\u00e7\u00e3o":41,"in\u00edcio":38,"inicializa\u00e7\u00f5":32,"introdu\u00e7\u00e3o":16,"m\u00faltipla":42,"par\u00e2metro":33,"parametriza\u00e7\u00e3o":33,"r\u00e1pido":38,"requisi\u00e7\u00f5":38,"s\u00e3o":33,"ser\u00e1":36,"transa\u00e7\u00f5":42,"unit\u00e1rio":13,"utilit\u00e1rio":40,"vers\u00f5":43,adicionai:36,amqpconnect:36,apena:33,aplicando:11,app:[17,29,30,31,32,39],armazenando:32,asyncowk:43,asyncwork:[15,17,18,19,20,21,22,23,24,25,26,27,28,30,31,39],atualizando:39,base:[23,24],bem:15,bucket:17,bulk_siz:36,cada:36,callabl:33,campo:36,changelog:0,compartilhamento:32,compatibilidad:43,completo:36,conf:17,connect:[17,18,19],consum:[17,25],consumindo:38,content:[17,18,19,20,21,22,23,24,25,26,27],contexto:42,criando:31,customizado:11,dada:36,dado:[32,38],decor:[11,21,33,36,42],definindo:31,desenvolvimento:12,easyqueu:19,endpoint:38,env:33,escolh:33,escolhendo:36,escrevendo:13,escutando:33,event:38,except:[17,19,20],exemplo:36,fila:38,fixo:41,flush:36,gerenciador:42,guia:[12,37],handler:[11,24,31,33,35],hook:29,http:[11,21,24,33,34,38],incompatibilidad:14,indic:15,individualment:36,intervalo:41,lendo:38,mai:[33,36],mensgem:36,messag:[19,22,25],modul:[17,18,19,20,21,22,23,24,25,26,27],nota:[8,9,10,36],nova:31,objeto:33,ofici:15,ond:33,option:[17,36],packag:[17,18,19,20,21,22,23,24,25,26,27],para:[33,36],parametro:36,path:33,porta:33,prefetch:36,princip:31,projeto:15,qual:36,que:33,queue:19,rabbitmq:[22,24,36,38],recebem:33,recebendo:[33,38],recebida:36,registri:27,regra:33,request:33,resolv:27,rodando:[38,41],rout:[17,33,36],run_on_shutdown:29,run_on_startup:29,server:[33,38],seu:38,shudtdown:29,side:38,signal:[23,24],sobr:[31,36],sse:[24,25],startup:29,sua:[31,39],submodul:[17,19,21,22,23,24,25,27],subpackag:[17,23],tabl:15,task_runn:17,tempo:41,test:[13,17,26],time:17,timeit:42,timeout:36,tipo:35,type:27,uma:[31,36,38,41],uso:37,util:17,valor:36,vindo:[15,33],worker:38}})