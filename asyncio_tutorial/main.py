# asyncio_tutorial/main.py

from asyncio_tutorial import asyncio
from task_groups import task_groups
from gather_results import gather_results
import time


# Create tasks them await them
# That means create them then launch them all at the same time
async def main():
    start_time = time.time()
    print(f"main started at {start_time}")
    try:
        # gather means gather the results of multiple coroutines (awaitable functions)
        # takes multiple functions as arguments
        gather_task = asyncio.gather(
            task_groups(),
            gather_results(),
        )

        results = await gather_task
        print('results', results)

        # Print results with indication of which function they correspond to
        for idx, result in enumerate(results):
            if idx == 0:
                print(f"Result from task_groups(): {result}")
            else:
                print(f"Result from factorial({chr(ord('A') + idx - 1)}, {idx + 1}): {result}")

        finish_time = time.time()
        total_time = finish_time - start_time
        print(f"main finished at {finish_time}")
        print(f"Total time: {total_time:.2f} seconds")
    except  asyncio.CancelledError as e:
        print(e)

# Run the main function within the asyncio event loop
asyncio.run(main())  # main is an async function
