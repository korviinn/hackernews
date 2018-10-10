import asyncio
from unittest import TestCase

from hackernews.fetch import HackerNewsFetcher, HackerNewsFetcherException
from hackernews.store import HackerStore, Story


class MockAPI:

    def __init__(self, count=10):
        self.count = 10

    async def get_new_stories(self):
        return list(range(self.count))

    async def get_item(self, item_id):
        if 0 < item_id < self.count:
            return {
                "id": item_id,
                "title": "Dummy Story",
                "url": "http://no.url",
                "time": 1,
                "by": "Dummy Author",
                "score": 1
            }
        else:
            return None

class MockStore(HackerStore):
    def __init__(self):
        self.stories = []

    def append(self, story: Story):
        self.stories.append(story)


class TestHackerNewsFetcher(TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_fetch(self):
        store = MockStore()
        api = MockAPI()
        fetcher = HackerNewsFetcher(api, store)

        async def do_fetch():
            async for _ in fetcher.fetch(5):
                pass

        self.loop.run_until_complete(do_fetch())
        self.assertEqual(len(store.stories), 5-1)

    def test_empty_story(self):
        store = MockStore()
        api = MockAPI()
        fetcher = HackerNewsFetcher(api, store)

        async def do_fetch():
            async for ex in fetcher.fetch(1):
                return ex

        ex = self.loop.run_until_complete(do_fetch())
        self.assertIsInstance(ex, HackerNewsFetcherException)
        self.assertTrue(str(ex).find("empty") != -1)

    def test_more_than_allowed(self):
        store = MockStore()
        api = MockAPI()
        fetcher = HackerNewsFetcher(api, store)

        async def do_fetch():
            async for ex in fetcher.fetch(50):
                return ex

        ex = self.loop.run_until_complete(do_fetch())
        self.assertIsInstance(ex, HackerNewsFetcherException)
        self.assertTrue(str(ex).find("can not return more") != -1)

    def test_fetch_one(self):
        store = MockStore()
        api = MockAPI()
        fetcher = HackerNewsFetcher(api, store)
        self.loop.run_until_complete(fetcher.fetch_story(3))
        self.assertEqual(store.stories[0].id, 3)
