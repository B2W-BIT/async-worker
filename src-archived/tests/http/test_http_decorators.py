from http import HTTPStatus

from aiohttp import web
from asynctest import mock, TestCase

from asyncworker import App
from asyncworker.decorators import wraps
from asyncworker.http import decorators
from asyncworker.http.decorators import parse_path
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.routes import call_http_handler
from asyncworker.testing import HttpClientContext


class HTTPDecoratorsTest(TestCase):
    async def setUp(self):
        self.app = App()

        @self.app.http.post(["/get_by_id/{_id}"])
        @parse_path
        async def get_by_id(_id: int):
            return web.json_response({"numero": _id})

        @self.app.http.post(["/param/{p1}/{p2}"])
        @parse_path
        async def path_multiple_params(p1: int, p2: int):
            return web.json_response({"p1": p1, "p2": p2})

    async def test_parse_one_path_param(self):
        async with HttpClientContext(self.app) as client:
            resp = await client.post("/get_by_id/42")
            data = await resp.json()
            self.assertEqual({"numero": 42}, data)

    async def test_parse_two_path_param(self):
        async with HttpClientContext(self.app) as client:
            resp = await client.post("/param/42/44")
            data = await resp.json()
            self.assertEqual({"p1": 42, "p2": 44}, data)

    async def test_raise_and_log_if_types_mismtach(self):
        """
        Se declararmos o argumento de um tipo inconpatível com o valor recebido
        lançamos uma exceção.
        Devemos gerar um logger.exception()
        """
        logger_mock_template = mock.CoroutineMock(
            exception=mock.CoroutineMock()
        )
        with mock.patch.object(
            decorators, "logger", logger_mock_template
        ) as logger_mock:
            async with HttpClientContext(self.app) as client:
                resp = await client.post("/get_by_id/abc")
                self.assertEqual(HTTPStatus.INTERNAL_SERVER_ERROR, resp.status)
                logger_mock.exception.assert_awaited_with(
                    {
                        "event": "incompatible-types-handler-arg",
                        "arg-type": int,
                        "arg-value": "abc",
                    }
                )

    async def test_can_be_the_second_decorator(self):
        """
        Valida que o parse_path pode não ser o deorator mais próximo do handler
        original
        """

        def other_deco(handler):
            @wraps(handler)
            async def _h(req: RequestWrapper):
                return await call_http_handler(req, handler)

            return _h

        @self.app.http.get(["/parse_path/{p}"])
        @parse_path
        @other_deco
        async def _parse_path_handler(req_wrapper: RequestWrapper, p: int):
            return web.json_response({"p": p})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/parse_path/42")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"p": 42}, data)

    async def test_can_be_away_from_handler_and_away_from_http_entrypoint(self):
        """
        Valida que o @parse_path pode estar longe do handler 
        *e* longe do @app.http.*
        Dessa forma:

        @app.http.get(...)
        @one_deco
        @parse_path
        @other_deco
        async def _handler(...):
        """

        def other_deco(handler):
            @wraps(handler)
            async def _h(req: RequestWrapper):
                return await call_http_handler(req, handler)

            return _h

        def one_deco(handler):
            @wraps(handler)
            async def _h(req: RequestWrapper):
                return await call_http_handler(req, handler)

            return _h

        @self.app.http.get(["/parse_path_again/{p}"])
        @one_deco
        @parse_path
        @other_deco
        async def _parse_path_handler(p: int):
            return web.json_response({"p": p})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/parse_path_again/42")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"p": 42}, data)

    async def test_can_have_a_param_with_same_name_of_handler(self):
        """
        Valida que os decorators pelo caminho podem receber parametros
        que possuem o mesmo nome de parametros do handler original, e isso
        não interfere na chamada do handler.

        def deco_1(handler):
            @wraps(handler)
            async def wrap(r: RequestWrapper):
                return await call_http_handler(r, handler)

            return wrap

        @app.http.get(["/path/{r}"])
        @parse_path
        @deco_1
        async def _handler(r: int, wrapper: RequestWrapper):
            return web.json_response({})
        """

        def one_deco(handler):
            @wraps(handler)
            async def _h(r: RequestWrapper):
                return await call_http_handler(r, handler)

            return _h

        @self.app.http.get(["/parse_path_again/{p}"])
        @parse_path
        @one_deco
        async def _parse_path_handler(r: RequestWrapper, p: int):
            return web.json_response({"p": p})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/parse_path_again/42")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"p": 42}, data)

    async def test_intermediate_deco_can_add_available_handler_arguments(self):
        """
        Um decorator intemediário pode adicionar novos parametros no
        types_registry do request. E esse parametro será corretamente
        passado ao handler
        """

        def one_deco(handler):
            @wraps(handler)
            async def _h(r: RequestWrapper):
                r.types_registry.set("String")
                return await call_http_handler(r, handler)

            return _h

        @self.app.http.get(["/parse_path_again/{p}"])
        @parse_path
        @one_deco
        async def _parse_path_handler(r: RequestWrapper, p: int, s: str):
            return web.json_response({"p": p})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/parse_path_again/42")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"p": 42}, data)
