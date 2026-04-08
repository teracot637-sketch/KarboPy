from .types import Context, EventHandler, Middleware, _Listener
from .utils import _router_name


def _cmd_middleware(prefix: str) -> Middleware:
    async def _mw(ctx: Context):
        return True if ctx.message.content.startswith(prefix) else None
    return _mw


class Router:
    def __init__(self, name=None):
        self._name = name or _router_name()
        self._listeners = {}
        self._middlewares = []

    @property
    def name(self):
        return self._name

    @property
    def listeners(self):
        return self._listeners

    def pre(self, middleware):
        self._middlewares.append(middleware)

    def on(self, event, callback=None):
        def decorator(func):
            if event not in self._listeners:
                self._listeners[event] = []
            self._listeners[event].append(_Listener(func, list(self._middlewares)))
            return func

        if callback is not None:
            return decorator(callback)
        return decorator

    def command(self, prefix, callback=None):
        def decorator(func):
            if "message" not in self._listeners:
                self._listeners["message"] = []
            self._listeners["message"].append(
                _Listener(func, [_cmd_middleware(prefix)] + list(self._middlewares))
            )
            return func

        if callback is not None:
            return decorator(callback)
        return decorator
