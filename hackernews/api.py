import aiohttp


class HackerNewsAPI:
    methods = dict(
        item="/item/{id}.json",
        new_stories="/newstories.json"
    )

    def __init__(self, endpoint="https://hacker-news.firebaseio.com/v0/"):
        """
        API client for hacker news.
        For more details on API see: https://github.com/HackerNews/API

        Can be used as a context manager or should be closed manually.

        :param endpoint: optional alternative endpoint
        """
        self.endpoint = endpoint
        self.session = aiohttp.ClientSession()

    async def _query(self, method: str, **kwargs):
        url = self.endpoint + self.methods[method].format(**kwargs)
        response = await self.session.get(url)
        return await response.json()

    async def get_item(self, item_id: int) -> dict:
        """
        Get any item by id.

        Fields possible:

        =========== =========================================================
        id 	        The item's unique id.
        deleted 	true if the item is deleted.
        type 	    The type of item. One of "job", "story", "comment",
                    "poll", or "pollopt".
        by 	        The username of the item's author.
        time 	    Creation date of the item, in Unix Time.
        text 	    The comment, story or poll text. HTML.
        dead 	    true if the item is dead.
        parent 	    The comment's parent: either another comment or
                    the relevant story.
        poll 	    The pollopt's associated poll.
        kids 	    The ids of the item's comments, in ranked display order.
        url 	    The URL of the story.
        score 	    The story's score, or the votes for a pollopt.
        title 	    The title of the story, poll or job.
        parts 	    A list of related pollopts, in display order.
        descendants In the case of stories or polls, the total comment count.
        =========== =========================================================

        :param item_id: id of item
        :return: item data as a dict
        """
        return await self._query('item', id=item_id)

    async def get_new_stories(self) -> [int]:
        """
        Get a list of ids of new stories.

        :return: list of ids
        """
        return await self._query('new_stories')

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
