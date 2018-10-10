import argparse
import asyncio
import sqlite3
import sys

from tqdm import tqdm

import hackernews
from hackernews.fetch import HackerNewsFetcher
from hackernews.api import HackerNewsAPI
from hackernews.store import HackerStoreCSV, HackerStoreSqlite


class Runner:
    def __init__(self):
        self.interrupted = False
        self.parser = argparse.ArgumentParser(
            description=hackernews.__description__,
            prog=hackernews.__project__)
        mode = self.parser.add_mutually_exclusive_group(required=True)
        mode.add_argument(
            '--csv',
            dest='csv_filename',
            type=str,
            help='Use given csv file to store news',
            default=None)
        mode.add_argument(
            '--sqlite',
            dest='sqlite_filename',
            type=str,
            help='Use given sqlite database to store news',
            default=None)
        self.parser.add_argument(
            '--count',
            dest='count',
            type=int,
            help='Amount of items to fetch',
            default=10
        )

        self.args = None

    async def run(self):
        self.args = self.parser.parse_args()
        try:
            async with HackerNewsAPI() as api:
                if self.args.csv_filename is not None:
                    with open(self.args.csv_filename, 'w') as file:
                        store = HackerStoreCSV(file)
                        await self.run_fetcher(api, store)
                        return 0
                elif self.args.sqlite_filename is not None:
                    with sqlite3.connect(self.args.sqlite_filename) as conn:
                        store = HackerStoreSqlite(conn)
                        await self.run_fetcher(api, store)
                        return 0

        # Top level exception handling, not an error
        # pylint: disable=broad-except
        except Exception as ex:
            print("Application failed: " + str(ex))
            return 2

    async def run_fetcher(self, api, store):
        fetcher = HackerNewsFetcher(api, store)
        progressbar = tqdm(total=min(self.args.count, 500))
        count = 0

        # Pylint bug: async generators not supported
        # pylint: disable=not-an-iterable
        async for ex in fetcher.fetch(self.args.count):
            if ex is not None:
                progressbar.write("Error: " + str(ex))
            else:
                count += 1
            if self.interrupted:
                break
            progressbar.update(1)

        progressbar.close()
        print("Fetched {} stories".format(count))

    async def stop(self):
        self.interrupted = True
        await asyncio.sleep(1)
        return 1


def main():
    runner = Runner()
    loop = asyncio.get_event_loop()
    root = runner.run()
    try:
        exitcode = loop.run_until_complete(root)
    except KeyboardInterrupt:
        exitcode = loop.run_until_complete(runner.stop())
    sys.exit(exitcode)


if __name__ == '__main__':
    main()
