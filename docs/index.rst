Hackernews
==========


Task statement
--------------

Write a Python script which does the following: 

  - Retrieve the "new"-stories from Hacker News (https://news.ycombinator.com/) 
    with the following API: https://github.com/HackerNews/API
  - Write an abstract base class HackerStore for storing the news 
  - Write two sub classes which inherit from HackerStore 

      * HackerStoreCSV: Writes the data into a CSV-file 
      * HackerStoreSqlite: Writes the data into a sqlite database 

  - Note: if the file/database already exists, it can be overwritten 
  - You can use any public python-library which might be helpful 
  - Write a README.md which describes how to use your script



Implementation
--------------


The Fetcher instance is pulling data using the API instance and storing into provided Store.
The Runner builds this chain and provides user interface.

.. autoclass:: hackernews.fetch.HackerNewsFetcher
    :members:

.. autoclass:: hackernews.api.HackerNewsAPI
    :members:

.. autoclass:: hackernews.store.HackerStore
    :members:

.. autoclass:: hackernews.store.HackerStoreCSV
    :members:

.. autoclass:: hackernews.store.HackerStoreSqlite
    :members:

.. autoclass:: hackernews.__main__.Runner
    :members:


Usage
-----


``python setup.py install``

``hackernews [-h] (--csv CSV_FILENAME | --sqlite SQLITE_FILENAME) [--count COUNT]``

Arguments:

    ============================ =========================================
    ``-h, --help``               Show help
    ``--csv CSV_FILENAME``       Use given csv file to store news
    ``--sqlite SQLITE_FILENAME`` Use given sqlite database to store news
    ``--count COUNT``            Amount of items to fetch
    ============================ =========================================



