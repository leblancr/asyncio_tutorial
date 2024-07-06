# asyncio_tutorial/gather_results.py

from asyncio_tutorial import asyncio
import time


async def factorial(name, number):
    f = 1
    
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({number}), currently i={i}...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")
    return f
    
async def gather_results():
    task_obj = await asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
    factorial("D", 5),
    factorial("E", 6),
)
 