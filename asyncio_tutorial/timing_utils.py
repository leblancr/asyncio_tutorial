# timing_utils.py

import functools
import time

# Dictionary to store timing information
execution_times = {}

# decorator, a function that takes a function
def async_time_function(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)  # await the decorated function
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times[func.__name__] = execution_time  # Store execution time
        return result  # return the result of the decorated function
    return wrapper
