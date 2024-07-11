# asyncio_tutorial/task_groups.py
from asyncio import shield
from pprint import pprint

from asyncio_tutorial import asyncio
import time

from asyncio_tutorial.timing_utils import async_time_function


# coroutine, returns an awaitable object (no return statement
# async functions need to use the await keyword when running
async def say_after(delay, what):
    # await asyncio.sleep(delay)  # , print(f"created task with {delay} second delay"))
    print(f"say_after before sleep: {time.strftime('%X')}")
    await asyncio.sleep(delay, print(f"sleep delay: {delay} second(s) when say_after() runs"))
    print(f"say_after after {delay} second(s) sleep: {time.strftime('%X')}")
    print(what)

    return what

@async_time_function
async def task_groups():
    try:
        print(f"task_groups function started at {time.strftime('%X')}")

        background_tasks = set()  # save task references so not garbage collected

        # asyncio handles the awaiting of these tasks implicitly
        # when the context manager exits
        # so it's really just creating tasks
        # All tasks are awaited when the context manager exits.
        print('Create tasks in TaskGroup context manager')
        async with asyncio.TaskGroup() as tg:
            task1_delay = 1
            task2_delay = 2

            print(f"tg.create_task(say_after({task1_delay}, 'hello'))")
            task1_obj = tg.create_task(say_after(task1_delay, 'hello'), name='task1_obj')
            background_tasks.add(task1_obj)

            print(f"tg.create_task(say_after({task2_delay}, 'world'))")
            task_to_cancel = tg.create_task(say_after(task2_delay, 'world'), name='task_obj2')
            background_tasks.add(task_to_cancel)

            try:
                # res = await shield(task_obj2)  # shield fron cancel
                # Wait for task_obj2 with a timeout of 1 second
                result = await asyncio.wait_for(task_to_cancel, timeout=30)
                # print(f"Result of task_obj2: {result}")
            except asyncio.TimeoutError:
                print(f"*** Timeout occurred, cancelling {task_to_cancel.get_name()} ***")
                task_to_cancel.cancel()  # Cancel the task if it takes too long
                await task_to_cancel  # Await cancellation to propagate
            
            # my create loop creating tasks for the task group
            print('tg.create_task group loop')
            for task_delay in range(3, 6):
                print(f"tg.create_task(say_after({task_delay}, delayed {task_delay}))")
                # print(f"for task_delay {task_delay}")
                task = tg.create_task(say_after(task_delay, str(f"delayed {task_delay}")))
                background_tasks.add(task)  # save task references so not garbage collected
        
            # pprint(background_tasks)
            print(f"task_groups started awaiting at {time.strftime('%X')}")
            # Exit context manager here, implied await the tasks now
            # This is where the awaitable objects start running
            # When the last one is done the message is printed
            # main is async so awaiting all these awaitables until they're all done

        # Now await each task individually to get their results
        # pprint(background_tasks)
        print('background_task results')
        for task in background_tasks:
            print(task.result())
        print(f"task_groups finished at {time.strftime('%X')}")
    except  asyncio.CancelledError as e:
        print(e)
