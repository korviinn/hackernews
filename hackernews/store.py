import csv
import sqlite3
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Story:
    id: int
    title: str
    url: str
    time: datetime
    author: str
    score: int


# This design is a requirement
# pylint: disable=too-few-public-methods
class HackerStore(ABC):

    @abstractmethod
    def append(self, story: Story):
        pass


# pylint: disable=too-few-public-methods
class HackerStoreCSV(HackerStore):
    fieldnames = ['id', 'title', 'url', 'time', 'author', 'score']

    def __init__(self, file, **csvargs):
        self.file = file
        self.writer = csv.DictWriter(
            self.file, fieldnames=self.fieldnames, **csvargs)
        self.writer.writeheader()

    def append(self, story: Story):
        self.writer.writerow(dict(
            id=str(story.id),
            title=story.title,
            url=story.url,
            time=str(story.time),
            author=story.author,
            score=story.score
        ))


# pylint: disable=too-few-public-methods
class HackerStoreSqlite(HackerStore):
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        with self.conn:
            self.conn.execute("DROP TABLE IF EXISTS news")
            self.conn.execute("CREATE TABLE news (id int, title text, url text,"
                              "time date, author text, score int)")

    def append(self, story: Story):
        with self.conn:
            self.conn.execute("INSERT INTO news VALUES (?,?,?,?,?,?)",
                              (story.id, story.title, story.url,
                               story.time, story.author, story.score))
