# Asyncworker with metrics on Docker Compose

## Executando

Para montar o ambiente, rode `docker-compose up`. Pode levar um
tempo para baixar e construir as imagens. Ao final, alguns serviços
serão expostos:

- http://localhost:8080 - Asyncworker
- http://localhost:9000 - Prometheus
- http://localhost:3000 - Grafana. Acessível através do usuário `admin` e senha `admin`

## Criando um novo dashboard

1. Rode a stack seguindo os passos descritos em `Executando`
2. Crie e edite o dashboard no Grafana
3. Siga os passos para [exportar um dashboard](https://grafana.com/docs/grafana/latest/dashboards/export-import/#exporting-a-dashboard)
4. Adicione o `.json` em `./docker/grafana/dashboards`. Note que os diretórios do sistema de arquivo são usados criar pastas no grafana, então escolha um caminho que faça sentido para a organização. Atulamente, temos duas pastas: `asyncworker` onde ficam os dashboards oficiais, criados usando somente métricas exportadas automaticamente pelo async-worker e `applications`, onde são adicionados dashboards de exemplo, que dependem de métricas customizadas, específicas de aplicações.

## Atualizando um dashboard existente

1. Rode a stack seguindo os passos descritos em `Executando`
2. Abra e edite o dashboard no Grafana
3. Siga os passos para [exportar um dashboard](https://grafana.com/docs/grafana/latest/dashboards/export-import/#exporting-a-dashboard)
4. Substitua o arquivo correspondente ao dashboard em `./docker/grafana/dashboards`
