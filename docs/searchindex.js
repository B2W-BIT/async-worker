Search.setIndex({docnames:["devguide/index","index","src/asyncworker/asyncworker","src/asyncworker/asyncworker.connections","src/asyncworker/asyncworker.easyqueue","src/asyncworker/asyncworker.http","src/asyncworker/asyncworker.sse","src/asyncworker/asyncworker.testing","src/asyncworker/asyncworker.types","src/asyncworker/modules","userguide/asyncworker-app/index","userguide/asyncworker-app/intro","userguide/handlers/http/doc","userguide/handlers/http/index","userguide/handlers/index","userguide/index"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["devguide/index.rst","index.rst","src/asyncworker/asyncworker.rst","src/asyncworker/asyncworker.connections.rst","src/asyncworker/asyncworker.easyqueue.rst","src/asyncworker/asyncworker.http.rst","src/asyncworker/asyncworker.sse.rst","src/asyncworker/asyncworker.testing.rst","src/asyncworker/asyncworker.types.rst","src/asyncworker/modules.rst","userguide/asyncworker-app/index.rst","userguide/asyncworker-app/intro.rst","userguide/handlers/http/doc.rst","userguide/handlers/http/index.rst","userguide/handlers/index.rst","userguide/index.rst"],objects:{"":{asyncworker:[2,0,0,"-"]},"asyncworker.app":{App:[2,1,1,""]},"asyncworker.app.App":{freeze:[2,2,1,""],get_connection:[2,2,1,""],get_connection_for_route:[2,2,1,""],handlers:[2,3,1,""],route:[2,2,1,""],run:[2,2,1,""],run_every:[2,2,1,""],run_on_shutdown:[2,2,1,""],run_on_startup:[2,2,1,""],shutdown:[2,2,1,""],shutdown_os_signals:[2,3,1,""],startup:[2,2,1,""]},"asyncworker.bucket":{Bucket:[2,1,1,""],BucketFullException:[2,4,1,""]},"asyncworker.bucket.Bucket":{is_empty:[2,2,1,""],is_full:[2,2,1,""],pop_all:[2,2,1,""],put:[2,2,1,""],used:[2,2,1,""]},"asyncworker.conf":{Settings:[2,1,1,""]},"asyncworker.conf.Settings":{Config:[2,1,1,""]},"asyncworker.conf.Settings.Config":{allow_mutation:[2,3,1,""],env_prefix:[2,3,1,""]},"asyncworker.connections":{AMQPConnection:[2,1,1,""],Connection:[2,1,1,""],ConnectionsMapping:[2,1,1,""],SSEConnection:[2,1,1,""]},"asyncworker.connections.AMQPConnection":{Config:[2,1,1,""],items:[2,2,1,""],keys:[2,2,1,""],put:[2,2,1,""],register:[2,2,1,""],set_connections:[2,2,1,""],values:[2,2,1,""]},"asyncworker.connections.AMQPConnection.Config":{arbitrary_types_allowed:[2,3,1,""]},"asyncworker.connections.ConnectionsMapping":{add:[2,2,1,""],with_type:[2,2,1,""]},"asyncworker.consumer":{Consumer:[2,1,1,""]},"asyncworker.consumer.Consumer":{consume_all_queues:[2,2,1,""],keep_runnig:[2,2,1,""],on_before_start_consumption:[2,2,1,""],on_connection_error:[2,2,1,""],on_consumption_start:[2,2,1,""],on_message_handle_error:[2,2,1,""],on_queue_error:[2,2,1,""],on_queue_message:[2,2,1,""],queue_name:[2,2,1,""],start:[2,2,1,""]},"asyncworker.easyqueue":{connection:[4,0,0,"-"],exceptions:[4,0,0,"-"],message:[4,0,0,"-"],queue:[4,0,0,"-"]},"asyncworker.easyqueue.connection":{AMQPConnection:[4,1,1,""]},"asyncworker.easyqueue.connection.AMQPConnection":{close:[4,2,1,""],connection_parameters:[4,2,1,""],is_connected:[4,2,1,""]},"asyncworker.easyqueue.exceptions":{EmptyQueueException:[4,4,1,""],InvalidMessageSizeException:[4,4,1,""],MessageError:[4,4,1,""],UndecodableMessageException:[4,4,1,""]},"asyncworker.easyqueue.message":{AMQPMessage:[4,1,1,""]},"asyncworker.easyqueue.message.AMQPMessage":{ack:[4,2,1,""],channel:[4,3,1,""],connection:[4,3,1,""],delivery_tag:[4,3,1,""],deserialized_data:[4,2,1,""],queue_name:[4,3,1,""],reject:[4,2,1,""],serialized_data:[4,3,1,""]},"asyncworker.easyqueue.queue":{BaseJsonQueue:[4,1,1,""],BaseQueue:[4,1,1,""],DeliveryModes:[4,1,1,""],JsonQueue:[4,1,1,""],QueueConsumerDelegate:[4,1,1,""]},"asyncworker.easyqueue.queue.BaseJsonQueue":{content_type:[4,3,1,""],deserialize:[4,2,1,""],serialize:[4,2,1,""]},"asyncworker.easyqueue.queue.BaseQueue":{deserialize:[4,2,1,""],serialize:[4,2,1,""]},"asyncworker.easyqueue.queue.DeliveryModes":{NON_PERSISTENT:[4,3,1,""],PERSISTENT:[4,3,1,""]},"asyncworker.easyqueue.queue.JsonQueue":{consume:[4,2,1,""],deserialize:[4,2,1,""],put:[4,2,1,""],serialize:[4,2,1,""],stop_consumer:[4,2,1,""]},"asyncworker.easyqueue.queue.QueueConsumerDelegate":{on_before_start_consumption:[4,2,1,""],on_connection_error:[4,2,1,""],on_consumption_start:[4,2,1,""],on_message_handle_error:[4,2,1,""],on_queue_message:[4,2,1,""]},"asyncworker.exceptions":{InvalidConnection:[2,4,1,""],InvalidRoute:[2,4,1,""]},"asyncworker.http":{decorators:[5,0,0,"-"]},"asyncworker.http.decorators":{parse_path:[5,5,1,""]},"asyncworker.options":{Actions:[2,1,1,""],AutoNameEnum:[2,1,1,""],DefaultValues:[2,1,1,""],Events:[2,1,1,""],Options:[2,1,1,""],RouteTypes:[2,1,1,""]},"asyncworker.options.Actions":{ACK:[2,3,1,""],REJECT:[2,3,1,""],REQUEUE:[2,3,1,""]},"asyncworker.options.DefaultValues":{BULK_FLUSH_INTERVAL:[2,3,1,""],BULK_SIZE:[2,3,1,""],ON_EXCEPTION:[2,3,1,""],ON_SUCCESS:[2,3,1,""],RUN_EVERY_MAX_CONCURRENCY:[2,3,1,""]},"asyncworker.options.Events":{ON_EXCEPTION:[2,3,1,""],ON_SUCCESS:[2,3,1,""]},"asyncworker.options.Options":{BULK_FLUSH_INTERVAL:[2,3,1,""],BULK_SIZE:[2,3,1,""],MAX_CONCURRENCY:[2,3,1,""]},"asyncworker.options.RouteTypes":{AMQP_RABBITMQ:[2,3,1,""],HTTP:[2,3,1,""],SSE:[2,3,1,""]},"asyncworker.routes":{AMQPRoute:[2,1,1,""],HTTPRoute:[2,1,1,""],Model:[2,1,1,""],Route:[2,1,1,""],RoutesRegistry:[2,1,1,""],SSERoute:[2,1,1,""],call_http_handler:[2,5,1,""],http_handler_wrapper:[2,5,1,""]},"asyncworker.routes.HTTPRoute":{aiohttp_routes:[2,2,1,""],validate_method:[2,2,1,""]},"asyncworker.routes.Model":{get:[2,2,1,""],keys:[2,2,1,""]},"asyncworker.routes.Route":{factory:[2,2,1,""]},"asyncworker.routes.RoutesRegistry":{add_route:[2,2,1,""],amqp_routes:[2,3,1,""],http_routes:[2,3,1,""],route_for:[2,2,1,""],sse_routes:[2,3,1,""]},"asyncworker.routes.SSERoute":{add_default_headers:[2,2,1,""]},"asyncworker.sse":{consumer:[6,0,0,"-"],message:[6,0,0,"-"]},"asyncworker.sse.consumer":{SSEConsumer:[6,1,1,""],State:[6,1,1,""]},"asyncworker.sse.consumer.SSEConsumer":{interval:[6,3,1,""],keep_runnig:[6,2,1,""],on_connection:[6,2,1,""],on_connection_error:[6,2,1,""],on_event:[6,2,1,""],on_exception:[6,2,1,""],start:[6,2,1,""]},"asyncworker.sse.consumer.State":{EVENT_DATA_FOUND:[6,3,1,""],EVENT_NAME_FOUND:[6,3,1,""],WAIT_FOR_DATA:[6,3,1,""]},"asyncworker.sse.message":{SSEMessage:[6,1,1,""]},"asyncworker.task_runners":{ScheduledTaskRunner:[2,1,1,""]},"asyncworker.task_runners.ScheduledTaskRunner":{can_dispatch_task:[2,2,1,""],start:[2,2,1,""],stop:[2,2,1,""]},"asyncworker.testing":{HttpClientContext:[2,1,1,""],http_client:[2,5,1,""]},"asyncworker.time":{ClockTicker:[2,1,1,""]},"asyncworker.time.ClockTicker":{stop:[2,2,1,""]},"asyncworker.types":{registry:[8,0,0,"-"],resolver:[8,0,0,"-"]},"asyncworker.types.registry":{RegistryItem:[8,1,1,""],TypesRegistry:[8,1,1,""]},"asyncworker.types.registry.TypesRegistry":{get:[8,2,1,""],set:[8,2,1,""]},"asyncworker.types.resolver":{ArgResolver:[8,1,1,""],MissingTypeAnnotationError:[8,4,1,""]},"asyncworker.types.resolver.ArgResolver":{resolve_param:[8,2,1,""],wrap:[8,2,1,""]},"asyncworker.utils":{Timeit:[2,1,1,""],entrypoint:[2,5,1,""]},"asyncworker.utils.Timeit":{TRANSACTIONS_KEY:[2,3,1,""]},asyncworker:{app:[2,0,0,"-"],bucket:[2,0,0,"-"],conf:[2,0,0,"-"],connections:[2,0,0,"-"],consumer:[2,0,0,"-"],easyqueue:[4,0,0,"-"],exceptions:[2,0,0,"-"],http:[5,0,0,"-"],options:[2,0,0,"-"],routes:[2,0,0,"-"],sse:[6,0,0,"-"],task_runners:[2,0,0,"-"],testing:[2,0,0,"-"],time:[2,0,0,"-"],types:[8,0,0,"-"],utils:[2,0,0,"-"]}},objnames:{"0":["py","module","Python m\u00f3dulo"],"1":["py","class","Python classe"],"2":["py","method","Python m\u00e9todo"],"3":["py","attribute","Python atributo"],"4":["py","exception","Python exce\u00e7\u00e3o"],"5":["py","function","Python fun\u00e7\u00e3o"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:exception","5":"py:function"},terms:{"S\u00e3o":11,"\u00edndic":1,"\u00fate":12,"a\u00e7\u00e3":15,"abstract":[2,4],"ass\u00edncron":[1,10,15],"atrav\u00e9s":[12,13,15],"c\u00f3dig":[2,3,4,5,6,7,8,11,12,15],"c\u00f3p":14,"ci\u00eanc":12,"class":[1,2,3,4,6,7,8,10,12,15],"conex\u00f5":11,"cria\u00e7\u00e3":[13,14,15],"default":2,"defini\u00e7\u00e3":12,"din\u00e2m":12,"ent\u00e3":12,"enum":[2,6,11],"est\u00e3":[11,12],"est\u00edmul":[1,11,14],"far\u00e3":11,"float":2,"fun\u00e7\u00e3":[1,12,14,15],"fun\u00e7\u00f5":11,"function":12,"funda\u00e7\u00e3":12,"import":12,"in\u00edci":[1,15],"inst\u00e2nc":[11,12,13],"instru\u00edm":12,"int":[2,4,12],"intermedi\u00e1ri":12,"m\u00e9tod":[11,12],"m\u00f3dul":[1,11,12],"m\u00faltipl":[11,15],"n\u00edvel":12,"necess\u00e1ri":[11,12],"new":[2,3,4],"obrigat\u00f3ri":11,"op\u00e7\u00f5":11,"p\u00e1gin":1,"padr\u00e3":12,"par\u00e2metr":[2,4,11,13,14,15],"poss\u00edv":11,"poss\u00edvel":12,"pr\u00f3pri":12,"r\u00e1p":[1,15],"raz\u00e3":12,"requisi\u00e7\u00e3":[1,12],"requisi\u00e7\u00f5":[13,15],"return":[4,12,13],"ser\u00e3":[11,12],"static":2,"transa\u00e7\u00f5":15,"trav\u00e9s":12,"unit\u00e1ri":[0,1],"usu\u00e1ri":12,"utilit\u00e1ri":[1,15],"v\u00e1l":12,"v\u00e1r":1,"vers\u00e3":[12,13],"with":2,Como:13,Ele:11,Eles:12,Essa:[12,13],Essas:1,Esse:[11,12],Esses:12,Isso:[12,14],Mais:12,Por:[1,11,12,14],Uma:[1,12,15],__call__:12,_asynci:2,_id:12,_type:8,_wrapp:12,abaix:[1,14],abc:[2,3],abstracteventloop:4,ack:[2,4],acord:14,actions:2,acts:2,add:[2,3],add_default_headers:2,add_rout:2,adiant:12,adicion:[12,15],aind:12,aioamqp:4,aiohttp:[2,12,13],aiohttp_rout:2,algum:12,alguns:[12,14],all:[2,3,4],allow:[2,3],allow_mutation:2,along:2,also:[2,3],alter:12,amqp_rabbitmq:2,amqp_rout:2,amqpconnection:[2,3,4,15],amqpmessag:[2,4],amqprout:2,ancestral:[2,3],and:[2,3,4],antes:12,any:[2,3,4,8],apen:[13,14,15],aplic:[1,11,13,14,15],app:[1,7,9,12,13,15],application:[2,4],aqu:[12,13],arbitrary_types_allowed:[2,3],argresolv:8,arguments:[2,4],armazen:[10,15],assim:12,assinatur:[11,12],async:[1,2,3,4,6,12,13],asynci:[2,4],asynciterator:2,asyncowk:[11,12],asyncwork:[12,13,14,15],asyncworker_:2,asyncworker_http_host:12,asyncworker_http_port:12,asynqueu:[2,4],atribut:12,atualiz:[1,15],aut:[2,3],autentic:12,auth_required:12,authorization:12,automatically:2,autonameenum:2,availabl:[2,3],await:[2,12],awaited:2,b2wdigital:1,bas:[2,3,4,6,7,8,9],basejsonqueu:4,basemodel:[2,3],basequeu:4,basesettings:2,basic_auth:12,bast:12,befor:[2,4],behav:2,bem:13,binding:12,body:[2,4],bool:[2,3,4],boot:11,brok:[1,4],bucket:[6,9],bucket_class:[2,6],bucketfullexception:2,bulk_flush_interval:2,bulk_siz:[2,15],busc:1,by_id:12,bytes:[2,3,4,6],cad:[11,14,15],call:[2,4],call_http_handl:[2,12],callabl:[2,4,13,14,15],callback:[2,4],called:[2,4],camp:15,can:4,can_dispatch_task:2,cancelling:4,cas:12,caus:[2,14],caused:2,central:11,cerc:12,cham:[11,12,14],changelog:1,channel:4,cheg:14,classmethod:[2,3],client:4,clock:2,clocktick:2,clos:4,collections:[2,3],comec:11,common:[2,3],compartilh:[1,10,15],complet:15,complex:12,condition:2,conect:11,conf:9,config:[2,3],connection:[2,3,9],connection_parameters:4,connections:[9,11],connectionsmapping:[2,3],connects:4,consig:12,construtor:[11,12],consum:[4,9,15],consume_all_queu:2,consumed:[2,4],consumer_nam:4,consumer_tag:[2,4],consumption:[2,4],cont:12,content:2,content_typ:4,contents:9,context:[12,15],cor:2,coro_ref:8,corotin:[12,13],coroutin:[2,4],corret:12,count:[2,3],cri:[10,14,15],custom:[2,4],customiz:[13,14,15],dad:[1,10,12,15],dat:[2,3,4],declar:[11,12],decod:4,decor:[12,13],decorat:12,decorator:[2,3,11,13,14,15],decorators:[13,14,15],def:[12,13],defaultvalu:2,defin:[2,10,12,15],definition:2,del:[12,13,14],delath:12,delegat:4,delegate_class:4,delivery_tag:[2,4],deliverymod:4,dentr:11,dependent:11,depo:12,deposit:11,desenvolv:1,deserializ:4,deserialization:2,deserialization_method:4,deserialized:[2,4],deserialized_dat:4,dess:[11,12,14],detalh:[1,13,14],dev:[11,12],dict:[2,3,4,6,11],diferent:[1,14],diret:12,diss:12,diz:[11,12],doc:13,docs:13,dois:12,during:[2,4],each:[2,3],easyqueu:[2,3,9],econtr:1,efet:11,emptyqueueexception:4,encontr:12,endpoint:15,entand:12,entend:[1,14],entrypoint:2,enumeration:[2,6],env_prefix:2,env_settings:2,envelop:4,envs:[13,14,15],envvars:12,erro:12,error:2,escolh:[13,14,15],escrev:[0,1,12,13],escut:[13,14,15],especial:[11,12],estam:12,estar:[11,13,14,15],estej:12,estimul:13,event:[1,2,14],event_body:6,event_data_found:6,event_nam:6,event_name_found:6,event_raw_body:6,events:[1,2,4,15],every:[2,4],exception:[2,4,6,8],exceptions:9,exchang:[2,3,4],execut:11,exempl:[12,14,15],exmepl:11,experimental:12,explicit:12,extern:14,extra:[12,13],extra_registri:8,factory:2,fails:[2,4],fal:11,fals:[2,3,4],far:[11,12],faz:[12,13],feit:12,fil:[11,14,15],fix:[1,15],flush:15,font:[2,3,4,5,6,7,8,11],form:[11,12],framework:1,freez:2,freezabl:[2,3],from:[4,12],funcion:1,functools:12,furth:[2,4],futur:2,generat:[2,3],generated:4,generic:[2,3,4],ger:[1,12],gerenc:15,get:[2,4,8,12,13],get_authenticated_us:12,get_connection:2,get_connection_for_rout:2,github:1,given:2,glob:12,guard:12,gui:1,handl:[2,5,11,13,14,15],handled:[2,4],handler_error:[2,4],handlers:[1,2,10,13,15],handling:[2,4],happens:2,headers:12,heartbeat:4,hooks:[1,10,15],host:[2,4],html:13,http:[1,2,11,14,15],http_client:[2,7],http_handler_wrapp:2,http_rout:2,httpclientcontext:[2,7],httprout:2,https:[1,13],httpserv:2,httpstatus:12,identifi:4,immediat:[2,3,4],implement:[2,4,12],incompatibil:1,indetermin:1,individual:15,inform:13,inicializ:[1,10,15],initialization:[2,4],inner:12,insid:2,instanc:12,instanced:[2,4],interess:12,interval:[1,2,6,15],introdu:1,invalid:2,invalidconnection:2,invalidmessagesizeexception:4,invalidrout:2,is_connected:4,is_empty:2,is_full:2,isn:4,item:2,items:[2,3],iterabl:[2,3,11],iteration:2,json:4,json_respons:[12,13],jsonqueu:[2,3,4],junt:12,keep_runnig:[2,6],keeping:[2,3],keeps:[2,3],key:[2,4],keys:[2,3],kwargs:[2,4,11],lend:15,lid:12,lik:2,list:[2,3,6,11,12,14],logg:4,logging:4,loop:[2,4],los:12,main:[2,3],mandatory:[2,3,4],manual:12,mapping:[2,3],match:12,max_concurrency:2,max_message_length:4,may:[2,4],mensag:[1,11,14],mensagens:14,mensg:15,mesm:[11,12,14],messag:[2,9],messageerror:[2,4],methods:[12,13],missingtypeannotationerror:8,model:2,models:12,modul:9,moment:12,mostr:13,msg:[2,4],mud:14,mutablemapping:2,my_handler_decorator:12,myproject:12,nam:[2,3,4],necess:12,necessari:11,needed:4,nenhum:12,ness:[11,12],nom:12,non:[2,3,4,6,8,11],non_persistent:4,noss:[11,12],not:[12,15],notifications:4,nov:[10,12,13,14,15],obj:8,object:[2,3,4,6,7,8],objet:[1,11,13,14,15],occurred:2,on_before_start_consumption:[2,4],on_connection:6,on_connection_error:[2,4,6],on_consumption_start:[2,4],on_error:4,on_event:6,on_exception:[2,6],on_message_handle_error:[2,4],on_queue_error:2,on_queue_messag:[2,4],on_startup:2,on_success:2,once:[2,4],onde:[11,13,14,15],one:4,optional:[2,4,8],options:[3,9,11,15],org:13,orig:[11,14],origens:[1,11],outr:11,overwritten:[2,4],packag:9,par:[1,4,11,13,14,15],param_nam:8,param_typ:8,parametr:[11,12,14,15],parametriz:[13,14,15],parse_path:[5,12],pass:[12,13],password:[2,4,6],path:[13,14,15],paths:[11,12],payload:4,peg:12,pel:12,permit:12,persistent:4,pod:[1,11,12,13,14],pois:12,pont:11,pop_all:2,popul:12,porqu:14,port:[13,14,15],poss:12,possu:12,prametr:12,precis:[12,13],prefetch:15,prefetch_count:[2,4],present:12,primeir:[11,12],principal:[1,10,12,15],procur:12,properti:[2,3,4],property:[2,4],provided:4,publish:4,published:4,publishing:4,pud:12,put:[2,3,4],pydantic:[2,3],python:1,quaisqu:[11,12],qualqu:1,quand:[12,13,14],quer:12,queu:[2,3,9],queue_nam:[2,4],queueconsumerdelegat:[2,4],rabbitmq:[1,2,9,11,14,15],rabbitmqmessag:2,raised:[2,4],random:4,raw:2,ready:[2,4],receb:[1,11,13,14,15],receiv:2,recorrent:1,regist:[2,3],registers:2,registr:[11,12,14],registry:12,registryit:8,regr:[13,14,15],reject:[2,4],represent:11,req:[12,13],request:[2,11,13,14,15],requeu:[2,4],resolu:12,resolve_p:8,respect:12,respons:[12,13],responsibl:[2,3],result:12,retorn:[12,13],returns:[2,3],rod:[1,15],rot:11,rout:[9,11,13,14,15],route_for:2,route_inf:[2,6],route_typ:[2,3],routedef:2,routesregistry:2,routetyp:[2,3,11,12,13],routing:4,routing_key:[2,3,4],run:[2,11],run_every:2,run_every_max_concurrency:2,run_on_shutdown:[2,10,15],run_on_startup:[2,10,15],running:2,sab:[11,12],schedul:2,scheduledtaskrunn:2,seconds:2,seconds_between_conn_retry:4,seg:12,segu:12,seguint:[11,12],sej:[11,12],self:12,sempr:12,send:12,sending:4,ser:[1,11,12,13,14,15],serializ:4,serializabl:4,serialized:4,serialized_dat:[2,3,4],serv:[1,13,14,15],servidor:1,set:[8,12],set_connections:[2,3],settings:2,should:[2,4],shudtdown:[1,10,15],shutdown:2,shutdown_os_signals:2,sid:[1,15],sigint:2,signal:2,signals:[2,3,9],signif:12,signific:11,sigterm:2,simpl:[12,13],simplesmet:13,sintax:12,siz:2,sleep:2,sobr:[1,10,12,15],something:2,sse:[2,9],sse_rout:2,sseconnection:[2,3],sseconsum:6,ssemessag:6,sserout:2,stabl:13,stag:[2,4],start:[2,6],started:[2,4],starts:[2,4],startup:[1,2,10,15],stat:6,status:12,stop:2,stop_consum:4,stopping:4,str:[2,3,4,6,8,11],subclass:[2,3],submodul:9,subpackag:9,sucess:12,suficient:12,suport:14,tag:4,talvez:12,task:2,task_runners:9,temp:[1,14,15],tent:12,test:[0,1],testing:9,that:[2,3,4],the:[2,3,4],tick:2,tim:[4,9],timeit:[1,2,15],timeout:15,tip:[1,11,12,15],tod:[11,12],top:12,track:[2,3],transactions:2,transactions_key:2,triggered:[2,4],tru:[2,3],tud:1,type:[2,3,4,6,8,11,12,13],type_definition:8,typehints:12,types:12,types_registry:12,typesregistry:[8,12],typing:[2,3,4],unauthorized:12,uncaught:[2,4],undecodablemessageexception:4,union:[2,3,4,6],unparsed:2,url:6,usad:[11,12],usag:[2,3],usar:12,used:[2,4],useful:4,user:12,user_id:12,userdict:2,usernam:[2,4,6],users:12,uso:1,utils:9,vai:12,valid:[2,4],validate_method:2,validation:2,valor:[12,15],valu:[2,3,8],valueerror:[2,4],vam:12,vari:12,vaz:12,vej:[12,13],vem:12,ver:14,vhost:[2,3],vind:[13,14,15],virtual:[2,3],virtual_host:4,voc:[1,11,12,14],wait_for_dat:6,waiting:2,was:[2,4],web:[12,13],web_request:2,web_routedef:2,when:[2,4],will:[2,4],with_typ:[2,3],work:[1,15],workers:1,wrap:8,wraps:12,xxxxxxxxxxxxx:2},titles:["Guia de desenvolvimento","Bem vindos \u00e0 documenta\u00e7\u00e3o oficial do projeto Asyncworker","asyncworker package","asyncworker.connections package","asyncworker.easyqueue package","asyncworker.http package","asyncworker.sse package","asyncworker.testing package","asyncworker.types package","asyncworker","Asyncworker App","Sobre a classe principal App","Regras para cria\u00e7\u00e3o de um handler HTTP","HTTP","Tipos de Handlers","Guia de uso"],titleterms:{"class":11,"cria\u00e7\u00e3":12,"par\u00e2metr":12,and:1,apen:12,aplic:12,app:[2,10,11],asyncwork:[1,2,3,4,5,6,7,8,9,10,11],bem:1,bucket:2,callabl:12,conf:2,connection:4,connections:[2,3],consum:[2,6],contents:[2,3,4,5,6,7,8],cri:11,customiz:12,decorator:12,decorators:[5,12],defin:11,desenvolv:0,document:1,easyqueu:4,envs:12,escolh:12,escut:12,estar:12,exceptions:[2,4],gui:[0,15],handl:12,handlers:[11,12,14],http:[5,12,13],indic:1,messag:[4,6],modul:[2,3,4,5,6,7,8],nov:11,objet:12,oficial:1,onde:12,options:2,packag:[2,3,4,5,6,7,8],par:12,parametriz:12,path:12,port:12,principal:11,projet:1,queu:4,receb:12,registry:8,regr:12,request:12,resolv:8,rout:[2,12],serv:12,sobr:11,sse:6,submodul:[2,4,5,6,8],subpackag:2,tabl:1,task_runners:2,testing:[2,7],tim:2,tip:14,types:8,uso:15,utils:2,vind:[1,12]}})