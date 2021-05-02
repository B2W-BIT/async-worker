import asynctest

from asyncworker.bucket import Bucket, BucketFullException


class BucketTest(asynctest.TestCase):
    def test_instantiate_with_max_size(self):
        bucket = Bucket(size=1024)
        self.assertEqual(1024, bucket.size)

    def test_tell_if_bucket_is_full(self):
        bucket = Bucket(size=1)
        bucket._items = [10]
        self.assertTrue(bucket.is_full())

        bucket = Bucket(size=10)
        bucket._items = [1, 2, 3]
        self.assertFalse(bucket.is_full())

        bucket._items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertTrue(bucket.is_full())

    def test_put_new_item_in_the_bucket(self):
        bucket = Bucket(size=10)
        bucket.put(10)
        bucket.put(10)
        bucket.put(10)
        self.assertEqual(3, bucket.used)
        self.assertFalse(bucket.is_full())

    def test_pop_all_messages_and_leave_bucket_empty(self):
        bucket = Bucket(size=10)
        bucket.put(10)
        bucket.put(10)
        bucket.put(10)
        items = bucket.pop_all()
        self.assertEqual(items, [10, 10, 10])
        self.assertEqual([], bucket._items)

    def test_tells_current_occupied_size(self):
        bucket = Bucket(size=10)
        bucket._items = [1, 2, 3]

        self.assertEqual(3, bucket.used)

        bucket._items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(10, bucket.used)

    def test_push_item_with_bucket_already_full(self):
        """
        Precisamos dar raise quando o bucket já está cheio e alguém
        tenta inserir mais um item
        """
        bucket = Bucket(size=3)
        bucket.put(20)
        bucket.put(20)
        bucket.put(20)

        with self.assertRaises(BucketFullException):
            bucket.put(10)

    def test_tells_if_bucket_is_empty(self):
        bucket = Bucket(size=1)
        bucket.pop_all()
        self.assertTrue(bucket.is_empty())

        bucket = Bucket(size=10)
        for i in range(3):
            bucket.put(i)
        self.assertFalse(bucket.is_empty())

        bucket.pop_all()
        self.assertTrue(bucket.is_empty())
