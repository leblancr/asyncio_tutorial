# asyncio_tutorial/main.py
from asyncio import eager_task_factory

from asyncio_tutorial import asyncio
from task_groups import task_groups
from gather_results import gather_results
from timing_utils import async_time_function, execution_times
import time
import tracemalloc

tracemalloc.start()


# Create tasks them await them
# That means create them then launch them all at the same time
async def main():
    start_time = time.time()
    print(f"main started at {time.strftime('%X')}")
    try:
        # results = []
        loop = asyncio.get_running_loop()
        loop.set_task_factory(eager_task_factory)

        # Define a dictionary to store decorated functions with their names
        async_functions = {
            'task_groups': async_time_function(task_groups),
            'gather_results': async_time_function(gather_results),
            # Add more functions here as needed
        }

        # using gather
        tasks = [func() for func in async_functions.values()]

        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Results are now collected and available in `results`
        print('\n--- Results ---')
        for result in results:
            print(result)

        print("\n--- Execution Times ---")
        for func_name, exec_time in execution_times.items():
            print(f"{func_name}: {exec_time:.2f} seconds")

        finish_time = time.time()
        total_time = finish_time - start_time
        print(f"main finished at {finish_time}")
        print(f"Total time: {total_time:.2f} seconds")
    except  asyncio.CancelledError as e:
        print(e)

# Run the main function within the asyncio event loop
asyncio.run(main())  # main is an async function
