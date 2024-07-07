# asyncio_tutorial/gather_results.py

from asyncio_tutorial import asyncio, async_time_function
import time


async def factorial(name, number):
    f = 1
    
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f
    
@async_time_function
async def gather_results():
    results = await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
        factorial("D", 5),
    )
    return results  # Return the gathered results
 