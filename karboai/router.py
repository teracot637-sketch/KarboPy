from __future__ import annotations

from .types import Context, EventHandler, Middleware, _Listener
from .utils import _router_name


def _cmd_middleware(prefix: str) -> Middleware:
    async def _mw(ctx: Context) -> bool | None:
        return ctx.message.content.startswith(prefix) or None
    return _mw


class Router:
    def __init__(self, name: str | None = None):
        self._name = name or _router_name()
        self._listeners: dict[str, list[_Listener]] = {}
        self._middlewares: list[Middleware] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def listeners(self) -> dict[str, list[_Listener]]:
        return self._listeners

    def pre(self, middleware: Middleware) -> None:
        self._middlewares.append(middleware)

    def on(self, event: str, callback: EventHandler) -> None:
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(
            _Listener(callback, list(self._middlewares))
        )

    def command(self, prefix: str, callback: EventHandler) -> None:
        if "message" not in self._listeners:
            self._listeners["message"] = []
        self._listeners["message"].append(
            _Listener(callback, [_cmd_middleware(prefix)] + list(self._middlewares))
        )
