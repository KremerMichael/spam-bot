import pandas as pd
import requests
from typing import Dict, List, Union

# async jazz
import aiohttp
import asyncio
from aiohttp import ClientSession

MAX_RETRIES = 3
SLEEP = 1
PARALLEL = 5
class spammer:
    """class built for spamming requests
    """

    def __init__(self, parallel: int=PARALLEL, sleep: int=SLEEP, max_retries: int=MAX_RETRIES):
        """init
        parallel, num of parallel requests to run at once,
        sleep, time to pause between requests
        max_retries, retries to make in case of fail
        """

        self.max_retries = max_retries
        self.sleep = sleep
        self.sem = asyncio.Semaphore(value=parallel)
        pass

    async def standard_handler(response: requests.models.Response) -> Union[Dict, requests.models.Response]:
        """Standard handler, tries to get json or just returns response
        """

        # Get json
        try:
            response_json = await response.json()

        except requests.exceptions.JSONDecodeError as err:
            return response

        return response_json


    # Semaphore to handle rate limit of 10
    async def spam_requests(session, request) -> requests.models.Response:
        """Generalized function for spamming requests"""

        # Handling rate limits
        await self.sem.acquire()
        await asyncio.sleep(self.sleep)
        self.sem.release()

        # Get & return response
        response = await session.request(method=request.method, url=request.url, headers=request.headers)
        response.raise_for_status()
        return response

    async def run_program(session, request, handler, retries=0):
        """Wrapper for running program in an asynchronous manner, handles errors & retries as well"""

        # try to get response
        try:
            response = await spam_requests(session, request)
            handled_response = await handler(response)
            return handled_response

        # Retry if HTTPError
        except requests.exceptions.HTTPError as http_err:
            new_retries = retries + 1
            if new_retries > self.max_retries: # Give up
                return None
            else: # Try again
                # Handling rate limits
                await self.sem.acquire()
                print('slow pause')
                await asyncio.sleep(self.sleep * 2)
                self.sem.release()
                return run_program(offset, session, handler, new_retries)

        # Print & move on
        except Exception as err:
            print(f"Exception occured: {err}")
            return None

    async def run(reqs: List[], handler = self.standard_handler) -> List:
        """Main run program
        """

        tmp_list = []
        async with ClientSession() as session:
            tmp_list = await asyncio.gather(*[run_program(session, req, handler) for req in reqs])
        return tmp_list
