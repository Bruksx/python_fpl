import asyncio
import time

async def func():
    time.sleep(10)

async def main():
    return asyncio.create_task(func())
    print("yes")

asyncio.run(main())