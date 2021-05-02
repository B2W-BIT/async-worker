from asynctest import TestCase

from asyncworker.connections import AMQPConnection, ConnectionsMapping
from asyncworker.exceptions import InvalidConnection


class ConnectionsMappingTest(TestCase):
    async def setUp(self):
        self.connection = AMQPConnection(
            hostname="localhost", username="guest", password="pwd"
        )
        self.mapping = ConnectionsMapping()

    async def test_del_item_ok(self):
        self.mapping["conn"] = self.connection

        self.assertEqual(self.connection, self.mapping["conn"])
        del self.mapping["conn"]
        with self.assertRaises(KeyError):
            self.mapping["conn"]

    async def test_del_item_frozen_set(self):
        self.mapping["conn"] = self.connection

        self.assertEqual(self.connection, self.mapping["conn"])
        await self.mapping.freeze()
        with self.assertRaises(RuntimeError):
            del self.mapping["conn"]

    async def test_set_item_map_is_frozen(self):

        await self.mapping.freeze()
        with self.assertRaises(RuntimeError):
            self.mapping["conn"] = self.connection

    async def test_set_duplicate_item(self):
        self.mapping["conn"] = self.connection

        with self.assertRaises(InvalidConnection):
            self.mapping["conn"] = self.connection
