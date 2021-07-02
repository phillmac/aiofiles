"""Async executor versions of file functions from the os module."""
import asyncio
from functools import partial, wraps
import os


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run

async def _scandir(*args, **kwargs):
    for item in os.scandir(*args, **kwargs): yield item

stat = wrap(os.stat)
rename = wrap(os.rename)
remove = wrap(os.remove)
mkdir = wrap(os.mkdir)
makedirs = wrap(os.makedirs)
rmdir = wrap(os.rmdir)
exists = wrap(os.path.exists)
abspath = wrap(os.path.abspath) 
replace = wrap(os.replace)
scandir = wrap(_scandir)

if hasattr(os, "sendfile"):
    sendfile = wrap(os.sendfile)
