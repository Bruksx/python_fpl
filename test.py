import asyncio
import requests
import time
import asyncio
import httpx

manager_history="https://fantasy.premierleague.com/api/entry/{}/history/"


start = time.time()
for i in range(1, 11):
    r = requests.get(manager_history.format(i))
    print(r)
print(time.time() - start)

start = time.time()
with requests.Session() as s:
    for i in range(1, 11):
       r =  s.get(manager_history.format(i))
       print(r)
print(time.time() - start)

"""
async def get_history(id):
    async with httpx.AsyncClient() as client:
        return await client.get(manager_history.format(id))

async def main():
    start = time.time()
    r = await asyncio.gather(map(get_history, range(1,10)))
    print(time.time() - start)

asyncio.run(main())
"""
async def get_async(id):
    async with httpx.AsyncClient() as client:
        r = await client.get(manager_history.format(id))
        return r.text

urls = range(1,11)

async def launch():
    start = time.time()
    resps = await asyncio.gather(*map(get_async, urls))
    print(time.time() - start)

asyncio.run(launch())