import asyncio
import functools

from cachetools import keys


def cached(cache, key=keys.hashkey):
	"""Memoize an async function in any cachetools cache, coalescing concurrent calls."""

	def decorator(fn):
		inflight = {}

		def done(k, task):
			inflight.pop(k, None)
			if task.cancelled() or task.exception() is not None:
				return  # failures are never cached
			try:
				cache[k] = task.result()
			except ValueError:  # too large for the cache
				pass

		@functools.wraps(fn)
		async def wrapper(*args, **kwargs):
			k = key(*args, **kwargs)
			try:
				return cache[k]
			except KeyError:
				pass
			task = inflight.get(k)
			if task is None:
				task = inflight[k] = asyncio.ensure_future(fn(*args, **kwargs))
				task.add_done_callback(lambda t: done(k, t))
			return await asyncio.shield(
				task
			)  # one caller cancelling won't cancel the rest

		wrapper.cache = cache  # type: ignore
		return wrapper

	return decorator
