from http import HTTPStatus

from aiohttp.test_utils import make_mocked_request
from aiohttp.web import json_response
from asynctest import TestCase

from asyncworker import App
from asyncworker.decorators import wraps
from asyncworker.http.types import PathParam
from asyncworker.http.wrapper import RequestWrapper
from asyncworker.routes import call_http_handler
from asyncworker.testing import HttpClientContext
from asyncworker.types.registry import TypesRegistry
from asyncworker.types.resolver import ArgResolver


class TestPathParamTypeHint(TestCase):
    maxDiff = None

    async def setUp(self):
        self.app = App()

    async def test_parse_simple_int(self):
        @self.app.http.get(["/num/{n}"])
        async def _get(n: PathParam[int]):
            return json_response({"n": await n.unpack()})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/42")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"n": 42}, data)

    async def test_one_param_mismatched_type(self):
        @self.app.http.get(["/num/{n}"])
        async def _get(n: PathParam[int]):
            return json_response({"n": await n.unpack()})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/abc")
            self.assertEqual(HTTPStatus.BAD_REQUEST, resp.status)
            data = await resp.text()
            self.assertEqual(
                "invalid literal for int() with base 10: 'abc'", data
            )

    async def test_multiple_params(self):
        @self.app.http.get(["/num/{n}/{other}"])
        async def _get(other: PathParam[str], n: PathParam[int]):
            return json_response(
                {"n": await n.unpack(), "other": await other.unpack()}
            )

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/42/name")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({"n": 42, "other": "name"}, data)

    async def test_multiple_params_of_the_same_type(self):
        @self.app.http.get(["/num/{n}/{other}"])
        async def _get(other: PathParam[int], n: PathParam[int]):
            return json_response(
                {"n": await n.unpack(), "other": await other.unpack()}
            )

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/42/99")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({"n": 42, "other": 99}, data)

    async def test_handler_receives_path_param_and_request_wrapper(self):
        @self.app.http.get(["/num/{n}/{other}"])
        async def _get(
            other: PathParam[str], n: PathParam[int], wrapper: RequestWrapper
        ):
            return json_response(
                {
                    "n": await n.unpack(),
                    "other": await other.unpack(),
                    "path": wrapper.http_request.path,
                }
            )

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/42/name")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual(
                {"n": 42, "other": "name", "path": "/num/42/name"}, data
            )

    async def test_path_param_complex_type(self):
        class MyObject:
            def __init__(self, val: str):
                self.value = val

        @self.app.http.get(["/num/{other}"])
        async def _get(other: PathParam[MyObject]):
            name = (await other.unpack()).value
            return json_response({"name": name})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/num/name")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({"name": "name"}, data)

    async def test_path_param_from_request(self):
        request = make_mocked_request("GET", "/num/42", match_info={"n": "42"})
        wrapper = RequestWrapper(
            http_request=request, types_registry=TypesRegistry()
        )
        path_param_instance = await PathParam.from_request(
            wrapper, arg_name="n", arg_type=int
        )
        self.assertEqual(42, await path_param_instance.unpack())

    async def test_aiohttp_fake_request(self):
        async def _get(n: PathParam[int]):
            return await n.unpack()

        request = make_mocked_request("GET", "/num/42", match_info={"n": "42"})
        request_wrapper = RequestWrapper(
            http_request=request, types_registry=TypesRegistry()
        )
        resolver = ArgResolver(request_wrapper.types_registry)

        async def _resolve_wrap(_handler, request_wrapper):
            p: PathParam[int] = PathParam(10)
            request_wrapper.types_registry.set(p, PathParam[int])
            return await resolver.wrap(_handler)

        self.assertEqual(10, await _resolve_wrap(_get, request_wrapper))

    async def test_with_custom_decorator(self):
        def _deco(handler):
            @wraps(handler)
            async def _wrap(r: RequestWrapper):
                r.types_registry.set(42, type_definition=int)
                return await call_http_handler(r, handler)

            return _wrap

        @self.app.http.get(["/path/{n}"])
        @_deco
        async def _path(r: RequestWrapper, n: PathParam[int], p: int):
            return json_response({"n": await n.unpack(), "p": p})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/path/10")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"n": 10, "p": 42}, data)

    async def test_with_multiple_custom_decorator(self):
        def _deco_1(handler):
            @wraps(handler)
            async def _wrap(r: RequestWrapper):
                r.types_registry.set(42, type_definition=int)
                return await call_http_handler(r, handler)

            return _wrap

        def _deco_2(handler):
            @wraps(handler)
            async def _wrap(r: RequestWrapper):
                r.types_registry.set("value", type_definition=str)
                return await call_http_handler(r, handler)

            return _wrap

        @self.app.http.get(["/path/{n}"])
        @_deco_2
        @_deco_1
        async def _path(r: RequestWrapper, n: PathParam[int], p: int, v: str):
            return json_response({"n": await n.unpack(), "p": p, "v": "value"})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/path/10")
            self.assertEqual(HTTPStatus.OK, resp.status)
            data = await resp.json()
            self.assertEqual({"n": 10, "p": 42, "v": "value"}, data)

    async def test_path_param_decorator_must_be_generic(self):
        async def _path(n: PathParam, p: PathParam[int]):
            return json_response({"n": await n.unpack()})

        original_qualname = _path.__qualname__

        with self.assertRaises(TypeError) as exc:

            app = App()

            app.http.get(["/path/{n}"])(_path)

        self.assertIn(original_qualname, exc.exception.args[0])
        self.assertTrue(
            "asyncworker.http.types.PathParam" in exc.exception.args[0]
        )

        self.assertTrue("must be Generic Type" in exc.exception.args[0])

    async def test_exceptions_must_show_original_handler_name(self):
        """
        Mesmo que um handler esteja decorado o nome original deve ser mencionado na mensagem de exception.
        Isso vai ajudar a encontrar onde está o problema.
        """

        def _deco_2(handler):
            @wraps(handler)
            async def _wrap(r: RequestWrapper):
                r.types_registry.set("value", type_definition=str)
                return await call_http_handler(r, handler)

            return _wrap

        async def my_handler(n: PathParam):
            return json_response({})

        original_qualname = my_handler.__qualname__

        with self.assertRaises(TypeError) as exc:

            self.app.http.get(["/path/{n}"])(_deco_2(my_handler))

        self.assertIn(original_qualname, exc.exception.args[0])

    async def test_path_param_bool_true_values(self):
        @self.app.http.get(["/bool/{on}/{true}/{yes}/{one}"])
        async def bool_true(
            on: PathParam[bool],
            true: PathParam[bool],
            yes: PathParam[bool],
            one: PathParam[bool],
        ):
            return json_response(
                {
                    "on": await on.unpack(),
                    "true": await true.unpack(),
                    "yes": await yes.unpack(),
                    "one": await one.unpack(),
                }
            )

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/bool/oN/truE/yEs/1")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual(
                {"on": True, "true": True, "yes": True, "one": True}, data
            )

    async def test_path_param_bool_false_values(self):
        @self.app.http.get(["/bool/{on}/{true}/{yes}/{one}"])
        async def bool_true(
            on: PathParam[bool],
            true: PathParam[bool],
            yes: PathParam[bool],
            one: PathParam[bool],
        ):
            return json_response(
                {
                    "on": await on.unpack(),
                    "true": await true.unpack(),
                    "yes": await yes.unpack(),
                    "one": await one.unpack(),
                }
            )

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/bool/oFf/falSe/No/0")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual(
                {"on": False, "true": False, "yes": False, "one": False}, data
            )

    async def test_path_param_bool_invalid_values(self):
        @self.app.http.get(["/bool/{on}"])
        async def bool_true(on: PathParam[bool],):
            return json_response({"on": await on.unpack()})

        async with HttpClientContext(self.app) as client:
            resp = await client.get("/bool/invalid")
            self.assertEqual(HTTPStatus.OK, resp.status)

            data = await resp.json()
            self.assertEqual({"on": False}, data)
