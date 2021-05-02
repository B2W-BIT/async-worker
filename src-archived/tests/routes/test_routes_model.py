from typing import Optional
from unittest import TestCase
from unittest.mock import patch

from asyncworker.conf import settings
from asyncworker.routes import Model, HTTPRoute


class MyModel(Model):
    field: Optional[int]


class RouteModelTest(TestCase):
    def test_set_item_field_exist(self):

        model = MyModel()
        model["field"] = 42
        self.assertEqual(42, model["field"])

    def test_set_item_field_does_not_exist(self):
        model = MyModel()
        with self.assertRaises(KeyError):
            model["not_found"] = 10

    def test_eq_compare_with_dict(self):
        model = MyModel(field=55)
        self.assertTrue(model == {"field": 55})

    def test_eq_compare_with_other_model(self):
        model = MyModel(field=99)
        self.assertTrue(model == model)

    def test_len(self):
        model = MyModel(field=100)
        self.assertEqual(1, len(model))

    def test_keys(self):
        model = MyModel()
        self.assertEqual(["field"], list(model.keys()))


class HTTPRouteTests(TestCase):
    def test_it_raises_an_error_if_user_declares_a_conflicting_metrics_route(
        self
    ):
        with self.assertRaises(ValueError):
            HTTPRoute(methods=["GET"], routes=[settings.METRICS_ROUTE_PATH])

    def test_it_doesnt_raises_an_error_if_user_declares_a_metrics_route_with_asyncworker_metrics_disabled(
        self
    ):

        with patch(
            "asyncworker.routes.conf.settings",
            METRICS_ROUTE_ENABLED=False,
            METRICS_ROUTE_PATH=settings.METRICS_ROUTE_PATH,
        ):
            route = HTTPRoute(
                methods=["GET"], routes=[settings.METRICS_ROUTE_PATH]
            )
            self.assertIsInstance(route, HTTPRoute)
