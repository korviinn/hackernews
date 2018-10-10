import aiohttp


class HackerNewsAPI:
    methods = dict(
        item="/item/{id}.json",
        new_stories="/newstories.json"
    )

    def __init__(self, endpoint="https://hacker-news.firebaseio.com/v0/"):
        self.endpoint = endpoint
        self.session = aiohttp.ClientSession()

    async def _query(self, method: str, **kwargs):
        url = self.endpoint + self.methods[method].format(**kwargs)
        response = await self.session.get(url)
        return await response.json()

    async def get_item(self, item_id: int) -> dict:
        return await self._query('item', id=item_id)

    async def get_new_stories(self) -> [int]:
        return await self._query('new_stories')

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
