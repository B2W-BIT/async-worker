import asyncio
from http import HTTPStatus
from uuid import uuid4

from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPNotFound
from aiohttp.web_response import Response
from asynctest import TestCase, patch, CoroutineMock

from asyncworker import App
from asyncworker.conf import settings
from asyncworker.http.wrapper import RequestWrapper


class HTTPMetricsTests(TestCase):
    app_url = f"http://{settings.HTTP_HOST}:{settings.HTTP_PORT}"

    async def setUp(self):
        self.app = App()
        self.client = ClientSession()

        self.callback = callback = CoroutineMock()
        self.route_path = "/mock_handler"
        self.route_method = "GET"
        self.metrics = metrics = patch(
            "asyncworker.metrics.aiohttp_resources.metrics"
        ).start()

        @self.app.http.get(routes=[self.route_path])
        async def handler(wrapper: RequestWrapper):
            request = wrapper.http_request
            metrics.requests_in_progress.labels.assert_called_once_with(
                method=request.method, path=request.path
            )
            metrics.requests_in_progress.labels.return_value.inc.assert_called_once()
            metrics.requests_in_progress.labels.return_value.dec.assert_not_called()
            await callback(request)
            return Response(text="ok")

        self.dynamic_route_path = "/resource/{id}"

        @self.app.http.get(routes=[self.dynamic_route_path])
        async def handler(wrapper: RequestWrapper):
            request = wrapper.http_request
            metrics.requests_in_progress.labels.assert_called_once_with(
                method="GET", path=self.dynamic_route_path
            )
            metrics.requests_in_progress.labels.return_value.inc.assert_called_once()
            metrics.requests_in_progress.labels.return_value.dec.assert_not_called()
            await callback(request)
            return Response(text="ok")

        await self.app.startup()

    async def tearDown(self):
        await asyncio.gather(self.app.shutdown(), self.client.close())
        patch.stopall()

    async def test_successful_request(self):
        url = f"{self.app_url}{self.route_path}"
        async with self.client.get(url) as response:
            content = await response.text()
            self.assertEqual(response.status, HTTPStatus.OK)

        self.metrics.response_size.labels.assert_called_once_with(
            method=self.route_method, path=self.route_path
        )
        self.metrics.request_duration.labels.assert_called_once_with(
            method=self.route_method,
            path=self.route_path,
            status=response.status,
        )
        self.metrics.requests_in_progress.labels.assert_called_with(
            method=self.route_method, path=self.route_path
        )
        self.metrics.response_size.labels.return_value.observe.assert_called_once_with(
            len(content)
        )
        self.metrics.request_duration.labels.return_value.observe.assert_called_once()
        self.metrics.requests_in_progress.labels.return_value.dec.assert_called_once()

    async def test_unsuccessful_request(self):
        url = f"{self.app_url}{self.route_path}"
        self.callback.side_effect = KeyError
        async with self.client.get(url) as response:
            await response.text()
            self.assertEqual(response.status, HTTPStatus.INTERNAL_SERVER_ERROR)

        self.metrics.response_size.labels.assert_not_called()
        self.metrics.request_duration.labels.assert_called_once_with(
            method=self.route_method,
            path=self.route_path,
            status=response.status,
        )
        self.metrics.requests_in_progress.labels.assert_called_with(
            method=self.route_method, path=self.route_path
        )
        self.metrics.response_size.labels.return_value.observe.assert_not_called()
        self.metrics.request_duration.labels.return_value.observe.assert_called_once()
        self.metrics.requests_in_progress.labels.return_value.dec.assert_called_once()

    async def test_notfound_request(self):
        url = f"{self.app_url}{self.route_path}"
        self.callback.side_effect = HTTPNotFound
        async with self.client.get(url) as response:
            content = await response.text()
            self.assertEqual(response.status, HTTPStatus.NOT_FOUND)

        self.metrics.response_size.labels.assert_called_once_with(
            method=self.route_method, path=self.route_path
        )
        self.metrics.request_duration.labels.assert_called_once_with(
            method=self.route_method,
            path=self.route_path,
            status=response.status,
        )
        self.metrics.requests_in_progress.labels.assert_called_with(
            method=self.route_method, path=self.route_path
        )
        self.metrics.response_size.labels.return_value.observe.assert_called_once_with(
            len(content)
        )
        self.metrics.request_duration.labels.return_value.observe.assert_called_once()
        self.metrics.requests_in_progress.labels.return_value.dec.assert_called_once()

    async def test_request_to_route_with_dynamic_path(self):
        request_path = self.dynamic_route_path.format(id=uuid4().hex)

        url = f"{self.app_url}{request_path}"
        async with self.client.get(url) as response:
            content = await response.text()
            self.assertEqual(response.status, HTTPStatus.OK)

        self.metrics.response_size.labels.assert_called_once_with(
            method="GET", path=self.dynamic_route_path
        )
        self.metrics.request_duration.labels.assert_called_once_with(
            method="GET", path=self.dynamic_route_path, status=response.status
        )
        self.metrics.requests_in_progress.labels.assert_called_with(
            method="GET", path=self.dynamic_route_path
        )
        self.metrics.response_size.labels.return_value.observe.assert_called_once_with(
            len(content)
        )
        self.metrics.request_duration.labels.return_value.observe.assert_called_once()
        self.metrics.requests_in_progress.labels.return_value.dec.assert_called_once()

    async def test_request_to_route_with_404_path(self):
        request_path = f"/{uuid4().hex}"

        url = f"{self.app_url}{request_path}"
        async with self.client.get(url) as response:
            content = await response.text()
            self.assertEqual(response.status, HTTPStatus.NOT_FOUND)

        self.metrics.response_size.labels.assert_called_once_with(
            method="GET", path="unregistered_path"
        )
        self.metrics.request_duration.labels.assert_called_once_with(
            method="GET", path="unregistered_path", status=response.status
        )
        self.metrics.requests_in_progress.labels.assert_called_with(
            method="GET", path="unregistered_path"
        )
        self.metrics.response_size.labels.return_value.observe.assert_called_once_with(
            len(content)
        )
        self.metrics.request_duration.labels.return_value.observe.assert_called_once()
        self.metrics.requests_in_progress.labels.return_value.dec.assert_called_once()
