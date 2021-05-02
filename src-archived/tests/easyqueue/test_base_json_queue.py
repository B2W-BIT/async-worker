import unittest
from unittest.mock import ANY

from asyncworker.easyqueue.queue import BaseJsonQueue


class BaseJsonQueueTests(unittest.TestCase):
    def setUp(self):
        self.base_json_queue = BaseJsonQueue(ANY, ANY, ANY)

    def test_serialize(self):
        body = {"teste": "aãç"}
        result = self.base_json_queue.serialize(body)

        self.assertEqual('{"teste": "a\\u00e3\\u00e7"}', result)

    def test_serialize_with_ensure_ascii_false(self):
        body = {"teste": "aãç"}
        result = self.base_json_queue.serialize(body, ensure_ascii=False)

        self.assertEqual('{"teste": "aãç"}', result)

    def test_deserialize(self):
        body = '{"teste": "aãç"}'.encode("utf-8")
        result = self.base_json_queue.deserialize(body)

        self.assertEqual({"teste": "aãç"}, result)
