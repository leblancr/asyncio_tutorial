# asyncio_tutorial/main.py
from asyncio import eager_task_factory

from asyncio_tutorial import asyncio
from task_groups import task_groups
from gather_results import gather_results
from timing_utils import async_time_function, execution_times
import time
import inspect


# Create tasks them await them
# That means create them then launch them all at the same time
async def main():
    start_time = time.time()
    print(f"main started at {start_time}")
    try:
        loop = asyncio.get_running_loop()
        loop.set_task_factory(eager_task_factory)

        # Define a dictionary to store decorated functions with their names
        async_functions = {
            'task_groups': async_time_function(task_groups),
            'gather_results': async_time_function(gather_results),
            # Add more functions here as needed
        }

        # Gather results from decorated functions
        tasks = [async_functions[func_name]() for func_name in async_functions]
        results = await asyncio.gather(*tasks)  # * means unpack

        print('\n--- Results ---')

        # Print results dynamically, zip makes tuples (func_name, result)
        for func_name, result in zip(async_functions.keys(), results):
            print(f"Result from {func_name}: {result}")

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
