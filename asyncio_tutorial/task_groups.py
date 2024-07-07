# asyncio_tutorial/task_groups.py
from asyncio import shield

from asyncio_tutorial import asyncio
import time

from asyncio_tutorial.timing_utils import async_time_function


# coroutine, returns an awaitable object (no return statement
# async functions need to use the await keyword when running
async def say_after(delay, what):
    await asyncio.sleep(delay)  # , print(f"created task with {delay} second delay"))
    print(what)

@async_time_function
async def task_groups():
    try:
        start_time = time.time()
        print(f"task_groups started at {start_time}")

        background_tasks = set()  # save task references so not garbage collected

        # asyncio handles the awaiting of these tasks implicitly
        # when the context manager exits
        # so it's really just creating tasks
        # All tasks are awaited when the context manager exits.
        async with asyncio.TaskGroup() as tg:
            task_obj1 = tg.create_task(say_after(1, 'hello'), name='task_obj1')
            task_obj2 = tg.create_task(say_after(2, 'world'), name='task_obj2')
            task_to_cancel = task_obj2
        
            try:
                # res = await shield(task_obj2)  # shiield fron cancel
                # Wait for task_obj2 with a timeout of 1 second
                result = await asyncio.wait_for(task_to_cancel, timeout=3)
                print(f"Result of task_obj2: {result}")
            except asyncio.TimeoutError:
                print(f"Timeout occurred, cancelling {task_to_cancel.get_name()}")
                task_obj2.cancel()  # Cancel the task if it takes too long    
                await task_obj2  # Await cancellation to propagate
            
            # my create loop creating tasks for the task group
            for task_delay in range(1, 5):
                task = tg.create_task(say_after(task_delay, str(f"delayed {task_delay}")))
                background_tasks.add(task)  # save task references so not garbage collected
        
            print(f"task_groups started at {time.strftime('%X')}")
            # Exit context manager here, implied await the tasks now
            # This is where the awaitable objects start running
            # When the last one is done the message is printed
            # main is async so awaiting all these awaitables until they're all done
        print(f"task_groups finished at {time.strftime('%X')}")
    except  asyncio.CancelledError as e:
        print(e)
