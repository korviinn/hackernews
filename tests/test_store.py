import io
import sqlite3
from datetime import datetime
from unittest import TestCase

from hackernews.store import HackerStoreCSV, Story, HackerStoreSqlite


class TestHackerStoreCSV(TestCase):
    def test_append(self):
        file = io.StringIO()
        store = HackerStoreCSV(file)
        store.append(Story(
            id=1,
            title="Title",
            url="Url",
            time=datetime.utcfromtimestamp(0),
            author="Author",
            score=1
        ))
        expected = "\r\n".join(("id,title,url,time,author,score",
                                "1,Title,Url,1970-01-01 00:00:00,Author,1",
                                ""))
        self.assertEqual(file.getvalue(), expected)


class TestHackerStoreSqlite(TestCase):
    def test_append(self):
        conn = sqlite3.connect(":memory:")
        store = HackerStoreSqlite(conn)
        store.append(Story(
            id=1,
            title="Title",
            url="Url",
            time=datetime.utcfromtimestamp(0),
            author="Author",
            score=1
        ))
        cur = conn.cursor()
        cur.execute("SELECT * FROM news")
        expected = (1, 'Title', 'Url', '1970-01-01 00:00:00', 'Author', 1)
        self.assertEqual(cur.fetchone(), expected)