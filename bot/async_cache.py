import asyncio
import functools
from collections.abc import Callable, Coroutine, Hashable, MutableMapping
from typing import Any, ParamSpec, Protocol, TypeVar, cast

from cachetools import keys

P = ParamSpec("P")
R = TypeVar("R")
R_co = TypeVar("R_co", covariant=True)


class CachedFunction(Protocol[P, R_co]):
    """An async callable with the original signature, plus a `.cache` attribute."""

    cache: MutableMapping[Any, Any]

    def __call__(
        self, *args: P.args, **kwargs: P.kwargs
    ) -> Coroutine[Any, Any, R_co]: ...


def cached(
    cache: MutableMapping[Any, Any],
    key: Callable[..., Hashable] = keys.hashkey,
) -> Callable[[Callable[P, Coroutine[Any, Any, R]]], CachedFunction[P, R]]:
    """Memoize an async function in any cachetools cache, coalescing concurrent calls."""

    def decorator(fn: Callable[P, Coroutine[Any, Any, R]]) -> CachedFunction[P, R]:
        inflight: dict[Hashable, asyncio.Future[R]] = {}

        def done(k: Hashable, task: asyncio.Future[R]) -> None:
            inflight.pop(k, None)
            if task.cancelled() or task.exception() is not None:
                return  # failures are never cached
            try:
                cache[k] = task.result()
            except ValueError:  # too large for the cache
                pass

        @functools.wraps(fn)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            k = key(*args, **kwargs)
            try:
                return cache[k]
            except KeyError:
                pass
            task = inflight.get(k)
            if task is None:
                task = asyncio.ensure_future(fn(*args, **kwargs))
                inflight[k] = task
                task.add_done_callback(lambda t: done(k, t))
            # shield: one caller cancelling won't cancel the rest
            return await asyncio.shield(task)

        wrapper.cache = cache  # ty: ignore[missing-attribute]
        return cast("CachedFunction[P, R]", wrapper)

    return decorator
