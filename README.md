
Hackernews
==========




Hackernews client.


Task description
----------------

Write a Python script which does the following: 
  - Retrieve the “new”-stories from Hacker News (<https://news.ycombinator.com/>) 
    with the following API: <https://github.com/HackerNews/API>
  - Write an abstract base class HackerStore for storing the news 
  - Write two sub classes which inherit from HackerStore 
    * HackerStoreCSV: Writes the data into a CSV-file 
    * HackerStoreSqlite: Writes the data into a sqlite database 
  - Note: if the file/database already exists, it can be overwritten 
  - You can use any public python-library which might be helpful 
  - Write a README.md which describes how to use your script

