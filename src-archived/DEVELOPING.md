# Desenvolvendo o asyncworker


## Instalando o ambiente

O Asyncworker usa o `pipenv` com gerenciador de ambientes e dependências. Para instalar as dependencias necessárias, faça:

```
$ pipenv install --dev --pre
```

## Todando os testes unitários

Depois disso você poderá rodar os testes unitários com:

```
$ pipenv run test
```

## Rodando testes de integração

Os testes de integração dependem de um RabbitMQ rodando localmente, para isso faça:

```
$ docker run -d --rm --net=host rabbitmq:3.6-management
```

e depois:

```
$ pipenv run itest
```

## Rodando todos os testes

Para rodar todos os testes (unitários e de integração), faça:

```
$ pipenv run all-tests
```
