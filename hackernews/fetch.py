from datetime import datetime

from hackernews.api import HackerNewsAPI
from hackernews.store import HackerStore, Story


class HackerNewsFetcherException(Exception):
    pass


class HackerNewsFetcher:
    def __init__(self, api: HackerNewsAPI, store: HackerStore):
        self.api = api
        self.store = store

    async def fetch(self, limit: int = 10):
        stories = await self.api.get_new_stories()
        if len(stories) > limit:
            stories = stories[:limit]
        else:
            yield HackerNewsFetcherException(
                "API can not return more than {} stories".format(len(stories)))
        for story in stories:
            try:
                await self.fetch_story(story)
            except HackerNewsFetcherException as ex:
                yield ex
            else:
                yield

    async def fetch_story(self, story_id: int):
        data = await self.api.get_item(story_id)
        if data is not None:
            story = Story(
                id=story_id,
                title=data.get('title'),
                url=data.get('url'),
                time=datetime.utcfromtimestamp(data.get('time')),
                author=data.get('by'),
                score=int(data.get('score'))
            )
            self.store.append(story)
        else:
            raise HackerNewsFetcherException(
                "Story {} is empty".format(story_id))
