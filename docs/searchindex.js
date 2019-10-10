Search.setIndex({docnames:["changelog/index","changelog/v0.10.0","changelog/v0.10.1","index","intro","src/asyncworker/asyncworker","src/asyncworker/asyncworker.connections","src/asyncworker/asyncworker.easyqueue","src/asyncworker/asyncworker.exceptions","src/asyncworker/asyncworker.rabbitmq","src/asyncworker/asyncworker.signals","src/asyncworker/asyncworker.signals.handlers","src/asyncworker/asyncworker.sse","src/asyncworker/asyncworker.testing","src/asyncworker/asyncworker.types","src/asyncworker/modules","userguide/backends","userguide/handlers/http","userguide/handlers/index","userguide/index","userguide/quickstart"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["changelog/index.rst","changelog/v0.10.0.rst","changelog/v0.10.1.rst","index.rst","intro.rst","src/asyncworker/asyncworker.rst","src/asyncworker/asyncworker.connections.rst","src/asyncworker/asyncworker.easyqueue.rst","src/asyncworker/asyncworker.exceptions.rst","src/asyncworker/asyncworker.rabbitmq.rst","src/asyncworker/asyncworker.signals.rst","src/asyncworker/asyncworker.signals.handlers.rst","src/asyncworker/asyncworker.sse.rst","src/asyncworker/asyncworker.testing.rst","src/asyncworker/asyncworker.types.rst","src/asyncworker/modules.rst","userguide/backends.rst","userguide/handlers/http.rst","userguide/handlers/index.rst","userguide/index.rst","userguide/quickstart.rst"],objects:{"":{asyncworker:[5,0,0,"-"]},"asyncworker.app":{App:[5,1,1,""]},"asyncworker.app.App":{freeze:[5,2,1,""],get_connection:[5,2,1,""],get_connection_for_route:[5,2,1,""],handlers:[5,3,1,""],route:[5,2,1,""],run:[5,2,1,""],run_every:[5,2,1,""],run_on_shutdown:[5,2,1,""],run_on_startup:[5,2,1,""],shutdown:[5,2,1,""],shutdown_os_signals:[5,3,1,""],startup:[5,2,1,""]},"asyncworker.bucket":{Bucket:[5,1,1,""],BucketFullException:[5,4,1,""]},"asyncworker.bucket.Bucket":{is_empty:[5,2,1,""],is_full:[5,2,1,""],pop_all:[5,2,1,""],put:[5,2,1,""],used:[5,2,1,""]},"asyncworker.conf":{Settings:[5,1,1,""]},"asyncworker.conf.Settings":{Config:[5,1,1,""]},"asyncworker.conf.Settings.Config":{allow_mutation:[5,3,1,""],env_prefix:[5,3,1,""]},"asyncworker.connections":{AMQPConnection:[6,1,1,""],Connection:[6,1,1,""],ConnectionsMapping:[6,1,1,""],SSEConnection:[6,1,1,""]},"asyncworker.connections.AMQPConnection":{Config:[6,1,1,""],items:[6,2,1,""],keys:[6,2,1,""],put:[6,2,1,""],register:[6,2,1,""],set_connections:[6,2,1,""],values:[6,2,1,""]},"asyncworker.connections.AMQPConnection.Config":{arbitrary_types_allowed:[6,3,1,""]},"asyncworker.connections.ConnectionsMapping":{add:[6,2,1,""],with_type:[6,2,1,""]},"asyncworker.consumer":{Consumer:[5,1,1,""]},"asyncworker.consumer.Consumer":{consume_all_queues:[5,2,1,""],keep_runnig:[5,2,1,""],on_before_start_consumption:[5,2,1,""],on_connection_error:[5,2,1,""],on_consumption_start:[5,2,1,""],on_message_handle_error:[5,2,1,""],on_queue_error:[5,2,1,""],on_queue_message:[5,2,1,""],queue_name:[5,2,1,""],start:[5,2,1,""]},"asyncworker.easyqueue":{connection:[7,0,0,"-"],exceptions:[7,0,0,"-"],message:[7,0,0,"-"],queue:[7,0,0,"-"]},"asyncworker.easyqueue.connection":{AMQPConnection:[7,1,1,""]},"asyncworker.easyqueue.connection.AMQPConnection":{close:[7,2,1,""],connection_parameters:[7,2,1,""],is_connected:[7,2,1,""]},"asyncworker.easyqueue.exceptions":{EmptyQueueException:[7,4,1,""],InvalidMessageSizeException:[7,4,1,""],MessageError:[7,4,1,""],UndecodableMessageException:[7,4,1,""]},"asyncworker.easyqueue.message":{AMQPMessage:[7,1,1,""]},"asyncworker.easyqueue.message.AMQPMessage":{ack:[7,2,1,""],channel:[7,3,1,""],connection:[7,3,1,""],delivery_tag:[7,3,1,""],deserialized_data:[7,2,1,""],queue_name:[7,3,1,""],reject:[7,2,1,""],serialized_data:[7,3,1,""]},"asyncworker.easyqueue.queue":{BaseJsonQueue:[7,1,1,""],BaseQueue:[7,1,1,""],DeliveryModes:[7,1,1,""],JsonQueue:[7,1,1,""],QueueConsumerDelegate:[7,1,1,""]},"asyncworker.easyqueue.queue.BaseJsonQueue":{content_type:[7,3,1,""],deserialize:[7,2,1,""],serialize:[7,2,1,""]},"asyncworker.easyqueue.queue.BaseQueue":{deserialize:[7,2,1,""],serialize:[7,2,1,""]},"asyncworker.easyqueue.queue.DeliveryModes":{NON_PERSISTENT:[7,3,1,""],PERSISTENT:[7,3,1,""]},"asyncworker.easyqueue.queue.JsonQueue":{consume:[7,2,1,""],deserialize:[7,2,1,""],put:[7,2,1,""],serialize:[7,2,1,""],stop_consumer:[7,2,1,""]},"asyncworker.easyqueue.queue.QueueConsumerDelegate":{on_before_start_consumption:[7,2,1,""],on_connection_error:[7,2,1,""],on_consumption_start:[7,2,1,""],on_message_handle_error:[7,2,1,""],on_queue_message:[7,2,1,""]},"asyncworker.exceptions":{InvalidConnection:[8,4,1,""],InvalidRoute:[8,4,1,""]},"asyncworker.options":{Actions:[5,1,1,""],AutoNameEnum:[5,1,1,""],DefaultValues:[5,1,1,""],Events:[5,1,1,""],Options:[5,1,1,""],RouteTypes:[5,1,1,""]},"asyncworker.options.Actions":{ACK:[5,3,1,""],REJECT:[5,3,1,""],REQUEUE:[5,3,1,""]},"asyncworker.options.DefaultValues":{BULK_FLUSH_INTERVAL:[5,3,1,""],BULK_SIZE:[5,3,1,""],ON_EXCEPTION:[5,3,1,""],ON_SUCCESS:[5,3,1,""],RUN_EVERY_MAX_CONCURRENCY:[5,3,1,""]},"asyncworker.options.Events":{ON_EXCEPTION:[5,3,1,""],ON_SUCCESS:[5,3,1,""]},"asyncworker.options.Options":{BULK_FLUSH_INTERVAL:[5,3,1,""],BULK_SIZE:[5,3,1,""],MAX_CONCURRENCY:[5,3,1,""]},"asyncworker.options.RouteTypes":{AMQP_RABBITMQ:[5,3,1,""],HTTP:[5,3,1,""],SSE:[5,3,1,""]},"asyncworker.rabbitmq":{message:[9,0,0,"-"]},"asyncworker.rabbitmq.message":{RabbitMQMessage:[9,1,1,""]},"asyncworker.rabbitmq.message.RabbitMQMessage":{accept:[9,2,1,""],body:[9,2,1,""],process_exception:[9,2,1,""],process_success:[9,2,1,""],reject:[9,2,1,""],serialized_data:[9,2,1,""]},"asyncworker.routes":{AMQPRoute:[5,1,1,""],HTTPRoute:[5,1,1,""],Model:[5,1,1,""],Route:[5,1,1,""],RoutesRegistry:[5,1,1,""],SSERoute:[5,1,1,""],call_http_handler:[5,5,1,""],http_handler_wrapper:[5,5,1,""]},"asyncworker.routes.HTTPRoute":{aiohttp_routes:[5,2,1,""],validate_method:[5,2,1,""]},"asyncworker.routes.Model":{get:[5,2,1,""],keys:[5,2,1,""]},"asyncworker.routes.Route":{factory:[5,2,1,""]},"asyncworker.routes.RoutesRegistry":{add_route:[5,2,1,""],amqp_routes:[5,3,1,""],http_routes:[5,3,1,""],route_for:[5,2,1,""],sse_routes:[5,3,1,""]},"asyncworker.routes.SSERoute":{add_default_headers:[5,2,1,""]},"asyncworker.signals":{base:[10,0,0,"-"],handlers:[11,0,0,"-"]},"asyncworker.signals.base":{Freezable:[10,1,1,""],Signal:[10,1,1,""]},"asyncworker.signals.base.Freezable":{freeze:[10,2,1,""],frozen:[10,2,1,""]},"asyncworker.signals.base.Signal":{send:[10,2,1,""]},"asyncworker.signals.handlers":{base:[11,0,0,"-"],http:[11,0,0,"-"],rabbitmq:[11,0,0,"-"],sse:[11,0,0,"-"]},"asyncworker.signals.handlers.base":{SignalHandler:[11,1,1,""]},"asyncworker.signals.handlers.base.SignalHandler":{shutdown:[11,2,1,""],startup:[11,2,1,""]},"asyncworker.signals.handlers.http":{HTTPServer:[11,1,1,""]},"asyncworker.signals.handlers.http.HTTPServer":{shutdown:[11,2,1,""],startup:[11,2,1,""]},"asyncworker.signals.handlers.rabbitmq":{RabbitMQ:[11,1,1,""]},"asyncworker.signals.handlers.rabbitmq.RabbitMQ":{startup:[11,2,1,""]},"asyncworker.signals.handlers.sse":{SSE:[11,1,1,""]},"asyncworker.signals.handlers.sse.SSE":{startup:[11,2,1,""]},"asyncworker.sse":{consumer:[12,0,0,"-"],message:[12,0,0,"-"]},"asyncworker.sse.consumer":{SSEConsumer:[12,1,1,""],State:[12,1,1,""]},"asyncworker.sse.consumer.SSEConsumer":{interval:[12,3,1,""],keep_runnig:[12,2,1,""],on_connection:[12,2,1,""],on_connection_error:[12,2,1,""],on_event:[12,2,1,""],on_exception:[12,2,1,""],start:[12,2,1,""]},"asyncworker.sse.consumer.State":{EVENT_DATA_FOUND:[12,3,1,""],EVENT_NAME_FOUND:[12,3,1,""],WAIT_FOR_DATA:[12,3,1,""]},"asyncworker.sse.message":{SSEMessage:[12,1,1,""]},"asyncworker.task_runners":{ScheduledTaskRunner:[5,1,1,""]},"asyncworker.task_runners.ScheduledTaskRunner":{can_dispatch_task:[5,2,1,""],start:[5,2,1,""],stop:[5,2,1,""]},"asyncworker.testing":{HttpClientContext:[13,1,1,""],http_client:[13,5,1,""]},"asyncworker.time":{ClockTicker:[5,1,1,""]},"asyncworker.time.ClockTicker":{stop:[5,2,1,""]},"asyncworker.types":{registry:[14,0,0,"-"],resolver:[14,0,0,"-"]},"asyncworker.types.registry":{TypesRegistry:[14,1,1,""]},"asyncworker.types.registry.TypesRegistry":{get:[14,2,1,""],set:[14,2,1,""]},"asyncworker.types.resolver":{ArgResolver:[14,1,1,""],MissingTypeAnnotationError:[14,4,1,""]},"asyncworker.types.resolver.ArgResolver":{resolve_param:[14,2,1,""],wrap:[14,2,1,""]},"asyncworker.utils":{Timeit:[5,1,1,""],entrypoint:[5,5,1,""]},"asyncworker.utils.Timeit":{TRANSACTIONS_KEY:[5,3,1,""]},asyncworker:{app:[5,0,0,"-"],bucket:[5,0,0,"-"],conf:[5,0,0,"-"],connections:[6,0,0,"-"],consumer:[5,0,0,"-"],easyqueue:[7,0,0,"-"],exceptions:[8,0,0,"-"],options:[5,0,0,"-"],rabbitmq:[9,0,0,"-"],routes:[5,0,0,"-"],signals:[10,0,0,"-"],sse:[12,0,0,"-"],task_runners:[5,0,0,"-"],testing:[13,0,0,"-"],time:[5,0,0,"-"],types:[14,0,0,"-"],utils:[5,0,0,"-"]}},objnames:{"0":["py","module","Python m\u00f3dulo"],"1":["py","class","Python classe"],"2":["py","method","Python m\u00e9todo"],"3":["py","attribute","Python atributo"],"4":["py","exception","Python exce\u00e7\u00e3o"],"5":["py","function","Python fun\u00e7\u00e3o"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:exception","5":"py:function"},terms:{"\u00edndic":3,"abstract":[5,7],"ass\u00edncron":3,"atrav\u00e9s":[17,19],"c\u00f3dig":[5,6,7,8,9,10,11,12,13,14,17,20],"ci\u00eanc":17,"class":[5,6,7,9,10,11,12,13,14],"conex\u00e3":20,"conte\u00fad":[],"default":5,"descri\u00e7\u00e3":2,"din\u00e2m":17,"enum":[5,12],"espec\u00edf":16,"est\u00e3":17,"est\u00edmul":[3,16],"float":5,"fun\u00e7\u00e3":17,"function":17,"import":[17,20],"in\u00edci":[3,19],"inst\u00e2nc":[17,20],"int":[5,7,9],"intermedi\u00e1ri":17,"m\u00e9tod":1,"m\u00f3dul":[3,20],"necess\u00e1ri":17,"new":[5,6,7],"p\u00e1gin":3,"par\u00e2metr":[5,7],"poss\u00edvel":[17,20],"pr\u00f3pri":17,"r\u00e1p":[3,19],"raz\u00e3":17,"requisi\u00e7\u00e3":[3,20],"requisi\u00e7\u00f5":[16,17,19],"return":[7,17,20],"static":5,"usu\u00e1ri":17,"v\u00e1l":17,"v\u00e1r":3,"with":5,Como:17,Essa:17,Essas:3,Esse:[17,20],Isso:17,Por:[3,16],Seu:[],Uma:3,_asynci:5,_on_event:20,_type:14,_wrapp:17,abaix:3,abc:[5,6],abstracteventloop:7,accept:9,acess:20,ack:[5,7,9,20],actions:[5,9],acts:5,add:[5,6],add_default_headers:5,add_rout:5,adiant:17,adicion:[1,17],aioamqp:7,aiohttp:[5,17,20],aiohttp_rout:5,algum:[17,20],alguns:16,all:[5,6,7,10],allow:[5,6],allow_mutation:5,along:5,also:[5,6],ambas:20,ambos:20,amqp:16,amqp_conn:20,amqp_messag:9,amqp_rabbitmq:[5,20],amqp_rout:5,amqpconnection:[5,6,7,20],amqpmessag:[5,7,9],amqprout:5,ancestral:[5,6],and:[1,5,6,7],any:[5,6,7,10,14],apen:19,aplic:[3,19],apllic:[],app:[11,13,15,17,20],appid:20,application:[5,7],aqu:17,arbitrary_types_allowed:[5,6],are:10,argresolv:14,args:10,arguments:[5,7,10],aser:[],asgard:20,assim:[17,20],assinatur:17,assum:20,async:[5,6,7,9,10,11,12,17,20],asynci:[5,7,10],asynciterator:5,asyncowk:17,asyncwok:[],asyncwork:[1,16,17,20],asyncworker_:5,asynqueu:[5,7],asynwork:20,atend:20,atribut:17,atual:16,aut:[5,6],autentic:17,auth_required:17,authorization:17,automat:20,automatically:5,autonameenum:5,availabl:[5,6],await:[5,17],awaited:5,backend:16,backends:[3,19],bas:[5,6,7,8,9,12,13,14,15],baseapp:[],based:10,basejsonqueu:7,basemodel:[5,6],basequeu:7,basesettings:5,basic_auth:17,befor:[5,7],behav:[5,10],bem:17,bla:[],body:[5,7,9,20],bool:5,brok:[3,7],bucket:[12,15],bucket_class:[5,12],bucketfullexception:5,bulk_flush_interval:5,bulk_siz:[5,20],busc:3,bytes:[5,6,7,12],cad:20,call:[5,7],call_http_handl:[5,17],callabl:[5,7],callback:[5,7,10],called:[5,7],can:7,can_dispatch_task:5,cancelling:7,capaz:20,cas:20,caus:5,caused:5,cham:17,chang:1,changelog:3,channel:7,classmethod:[5,6],client:7,clock:5,clocktick:5,clos:7,cod:1,codeowners:1,coerent:2,collections:[5,6,10],comando:20,common:[5,6],condition:[5,8],conf:15,config:[5,6],confirm:20,connect:10,connection:[5,6,8,15],connection_parameters:7,connections:[15,20],connectionsmapping:[5,6],connects:7,consig:17,consum:[7,15,16,19],consume_all_queu:5,consumed:[5,7],consumer_nam:7,consumer_tag:[5,7],consumption:[5,7],cont:17,content:5,content_typ:7,contents:15,cor:5,coro_ref:14,corotin:17,coroutin:[5,7,10],corret:17,count:[5,6],counts:20,coverag:1,curl:20,custom:[5,7],customiz:19,dad:[16,17,19],dat:[5,6,7,10,20],decl:1,declar:20,decod:7,decor:17,decorator:[5,6,17],decorators:19,def:[17,20],defaultvalu:5,defin:[5,8],definition:[5,8],del:17,delegat:7,delegate_class:7,delivery_tag:[5,7,9],deliverymod:7,dependenc:2,dependency:1,deployment_inf:20,deployment_success:20,desconect:20,deserializ:7,deserialization:5,deserialization_method:7,deserialized:[5,7],deserialized_dat:7,dess:17,detalh:17,dev:17,devolv:20,dict:[5,12],diferent:[3,16],diret:17,diss:17,doc:17,docs:[1,17],drain_handl:20,during:[5,7],each:[5,6],easyqueu:[1,5,6,9,15],econtr:3,emptyqueueexception:7,encontr:17,endpoint:[16,19],entand:17,entend:[3,16],entrypoint:5,enumeration:[5,12],env_prefix:5,env_settings:5,envelop:7,envi:20,erro:[1,20],error:5,errors:20,erros:20,escrev:[3,17],escrit:[],estam:20,estar:[17,20],estav:2,estimul:17,etc:[],event:[3,5,10,16,20],event_body:12,event_data_found:12,event_nam:[12,20],event_name_found:12,event_raw_body:12,events:[3,5,7,16,19],every:[5,7],exception:[5,7,8,12,14,20],exceptions:15,exchang:[5,6,7],exempl:[17,20],extra:17,extra_registri:14,facilit:[],factory:5,fails:[5,7],fal:20,fals:[5,7],faz:17,featur:1,fic:20,fil:19,fired:10,fix:3,flask:[],fluentd:20,font:[5,6,7,8,9,10,11,12,13,14],foo:[],framework:3,freez:[5,10],freezabl:[5,6,10],frent:20,from:[7,17,20],frozen:10,functools:17,furth:[5,7],futur:5,generat:[5,6],generated:7,generic:[5,6,7],ger:[3,20],geral:20,get:[5,7,14,17,20],get_authenticated_us:17,get_connection:5,get_connection_for_rout:5,given:5,glob:[],guest:20,gui:3,handl:[5,16,19,20],handled:[5,7],handler_error:[5,7],handlers:[3,5,10,19],handling:[5,7],happens:5,headers:17,heartbeat:7,hell:20,hook:1,host:[5,7,20],hostnam:[],html:17,http:[3,5,10,16,18,19],http_client:[5,13],http_handler_wrapp:5,http_rout:5,httpclientcontext:[5,13],httpm:[],httprout:5,https:17,httpserv:[5,11],httpstatus:17,ide:20,identifi:7,implement:[5,7,16],implementation:10,indetermin:3,index:20,inform:17,initialization:[5,7],inner:17,insert:1,insert_user_into_type_registry:[],insid:5,inspir:[],instanc:17,instanced:[5,7],integr:2,interval:[3,5,12],introdu:3,invalid:[5,8],invalidconnection:[5,8],invalidmessagesizeexception:7,invalidrout:[5,8],is_connected:7,is_empty:5,is_full:5,isn:7,issu:1,item:5,items:[5,6],iterabl:[5,6],iteration:5,json:[7,20],json_respons:[17,20],jsonqueu:[5,6,7],junt:17,keep_runnig:[5,12],keeping:[5,6],keeps:[5,6],key:[5,7],keys:[5,6],kwarg:1,kwargs:[5,7,10],lanc:20,len:20,lend:19,lik:5,linh:20,list:[5,6,10,12,17,20],locks:10,log:20,logg:7,logging:7,loop:[5,7,20],los:17,main:[5,6,20],mapping:[5,6],max_concurrency:5,max_message_length:7,may:[5,7],melhor:1,mensag:[1,3,20],mensagens:[16,20],mesm:20,messag:[5,15,20],messageerror:[5,7],meth:[],method:10,methods:[1,17,20],microframework:[],missingtypeannotationerror:14,model:5,models:17,modul:[1,15],moment:17,mostr:[17,20],mov:1,msg:[5,7],mud:2,mutablemapping:5,my_handler_decorator:17,myproject:17,mywork:20,nam:[5,6,7,20],named:10,nao:1,needed:7,ness:20,non:[5,6,7,12,14],non_persistent:7,not:17,notifications:7,obj:14,object:[5,6,7,9,10,11,12,13,14],objet:[3,17,20],occurred:5,on_before_start_consumption:[5,7],on_connection:12,on_connection_error:[5,7,12],on_consumption_start:[5,7],on_error:7,on_event:12,on_exception:[5,9,12],on_message_handle_error:[5,7],on_queue_error:5,on_queue_messag:[5,7],on_startup:5,on_success:[5,9],once:[5,7],onde:17,one:7,optional:[5,7,14],options:[6,9,15,20],org:17,orig:16,origens:3,orign:3,overwritten:[5,7],owner:10,packag:15,par:[2,3,4,7,17,20],param_typ:14,parametr:17,pass:17,password:[5,7,12,20],payload:7,peg:17,pel:[16,17,20],permit:17,persistent:7,plan:20,pod:[3,17,20],pont:20,pop_all:5,popul:17,position:1,poss:17,possibil:16,prametr:17,precis:[17,20],prefetch_count:[5,7,20],principal:17,print:20,process:16,process_exception:9,process_success:9,projet:[2,4,16],properti:7,property:[5,7,9,10],provided:7,publish:7,published:7,publishing:7,pud:17,put:[5,6,7],pydantic:[2,5,6],python:3,quaisqu:17,qualqu:3,quand:[1,17,20],queu:[5,6,15],queue_nam:[5,7],queueconsumerdelegat:[5,7],rabbitmq:[3,5,10,15,16,19],rabbitmqmessag:[5,9],raised:[5,7],random:7,raw:5,ready:[5,7],receb:[3,16,19],receiv:5,received:20,receivers:10,reconect:20,recorrent:3,ref:[],regist:[5,6],registered:10,registers:5,registry:17,regr:17,reject:[5,7,9,20],remov:1,reports:1,req:[17,20],request:[5,19,20],requeu:[5,7,9,20],resolu:17,resolve_p:14,respons:[17,20],responsibl:[5,6],retorn:17,returns:[5,6],rod:[2,3,19],rot:20,rout:[1,8,15,17,20],route_for:[1,5],route_inf:[5,12],route_typ:[5,6],routedef:5,routesregistry:[1,5],routetyp:[5,6,17,20],routing:7,routing_key:[5,6,7],run:[5,20],run_every:5,run_every_max_concurrency:5,run_on_shutdown:5,run_on_startup:[1,5],running:5,sab:17,schedul:5,scheduledtaskrunn:5,seconds:5,seconds_between_conn_retry:7,seguint:[16,20],sej:[17,20],sempr:[17,20],send:[2,10],sending:7,sends:10,ser:[2,3,16,17,20],serializ:7,serializabl:7,serialized:7,serialized_dat:[5,6,7,9],serv:[3,16,19],servidor:[3,20],set:[14,17],set_connections:[5,6],settings:5,setup:2,should:[5,7],shutdown:[5,11],shutdown_os_signals:5,sid:[3,16,19],sigint:5,signal:[5,10],signalhandl:11,signals:[5,6,15],sigterm:5,simpl:17,simplesmet:17,siz:5,sleep:5,sobr:[17,20],something:5,sphinx:1,sse:[5,10,15,20],sse_conn:20,sse_rout:5,sseapplication:[],sseconnection:[5,6,20],sseconsum:12,ssemessag:12,sserout:5,stabl:17,stag:[5,7],start:[5,12],started:[5,7],starts:[5,7],startup:[5,11],stat:12,status:17,status_update_event:20,stop:5,stop_consum:7,stopping:7,str:[5,6,7,12],stre:[],subclass:[5,6],submodul:15,subpackag:15,sucess:17,suficient:17,suport:16,tag:[1,2,7],tak:10,task:[5,20],task_runners:15,taskid:20,taskstatus:20,temp:3,tentant:20,test:2,testing:15,text:[],tha:10,that:[5,6,7],the:[1,5,6,7,10],tick:5,tim:[7,15],timeit:5,tip:17,titlesonly:[],tod:17,top:17,track:[5,6],transactions:5,transactions_key:5,triggered:[5,7],tru:[5,6,9,20],type:[5,6,7,12,14,17,20],type_definition:14,typehints:17,types:17,types_registry:17,typesregistry:[14,17],typing:[5,6,7],unauthorized:17,uncaught:[5,7],undecodablemessageexception:7,union:[5,6,7,12],unparsed:5,url:[12,20],usag:[5,6],usand:20,usar:17,use:10,used:[5,7],useful:7,user:[17,20],userdict:5,userlist:10,usernam:[5,7,12],using:10,uso:3,utils:15,valid:[5,7],validate_method:5,validation:5,valu:[5,6],valueerror:[5,7,8],vej:17,vem:17,vez:2,vhost:[5,6,20],via:16,virtual:[5,6],virtual_host:7,voc:[3,20],wait_for_dat:12,waiting:5,was:[5,7],web:[17,20],web_request:5,web_routedef:5,when:[5,7],which:10,will:[5,7],with_typ:[5,6],work:[3,16,19],workers:3,world:20,wrap:14,wraps:17,xxxxxxxxxxxxx:5},titles:["Changelog","0.10.0","0.10.1","Bem vindos \u00e0 documenta\u00e7\u00e3o oficial do projeto Asyncworker","Introdu\u00e7\u00e3o","asyncworker package","asyncworker.connections package","asyncworker.easyqueue package","asyncworker.exceptions package","asyncworker.rabbitmq package","asyncworker.signals package","asyncworker.signals.handlers package","asyncworker.sse package","asyncworker.testing package","asyncworker.types package","asyncworker","Backends","HTTP","Handlers","Guia de uso","In\u00edcio r\u00e1pido"],titleterms:{"atrav\u00e9s":20,"in\u00edci":20,"prop\u00f3sit":[],"r\u00e1p":20,"requisi\u00e7\u00f5":20,and:3,apen:17,aplic:17,app:5,asyncwork:[3,5,6,7,8,9,10,11,12,13,14,15],backends:16,bas:[10,11],bem:3,bucket:5,changelog:0,conf:5,connection:7,connections:[5,6],consum:[5,12,20],contents:[5,6,7,8,9,10,11,12,13,14],customiz:17,dad:20,decorators:17,document:3,easyqueu:7,endpoint:20,events:20,exceptions:[5,7,8],fil:20,gui:19,handl:17,handlers:[11,17,18],http:[11,17,20],indic:3,introdu:4,lend:20,messag:[7,9,12],modul:[5,6,7,8,9,10,11,12,13,14],oficial:3,options:5,packag:[5,6,7,8,9,10,11,12,13,14],projet:3,queu:7,rabbitmq:[9,11,20],receb:[17,20],registry:14,request:17,resolv:14,rod:20,rout:5,serv:20,sid:20,signals:[10,11],sse:[11,12],submodul:[5,7,9,10,11,12,14],subpackag:[5,10],tabl:3,task_runners:5,testing:[5,13],tim:5,types:14,uso:19,utils:5,vind:3,work:20}})