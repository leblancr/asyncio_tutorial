import asyncio
import time

# coroutine, returns an awaitable object (no return statement
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

# Create tasks them await them
# That means create them then launch them all at the same time
async def main():
    # asyncio handles the awaiting of these tasks implicitly
    # when the context manager exits
    # so it's really just creating tasks
    async with asyncio.TaskGroup() as tg:
        tg.create_task(say_after(1, 'hello'))
        tg.create_task(say_after(2, 'world'))
        
        # my create loop creating tasks for the task group
        for task_delay in range(9):
            tg.create_task(say_after(task_delay, str(task_delay)))

        print(f"started at {time.strftime('%X')}")
    # Exit context manager here
    # This is where the awaitable objects start running
    # When the last one is done the message is printed
    # main is async so awaiting all these awaitables until they're all done
    print(f"finished at {time.strftime('%X')}")


# Run the main function within the asyncio event loop
asyncio.run(main())  # main is an async function
