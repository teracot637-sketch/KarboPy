from __future__ import annotations

from typing import TYPE_CHECKING

import socketio

from ._const import KARBO_API, SOCKET_TOPICS
from .logging import logger
from .router import Router
from .types import Context, Message, _Listener

if TYPE_CHECKING:
    from .client import KarboAI


class Dispatcher:
    def __init__(self, client: KarboAI):
        self._client = client
        self._socket = None
        self._listeners: dict[str, list[_Listener]] = {}

    def bind(self, *routers: Router) -> None:
        for router in routers:
            for event, items in router.listeners.items():
                if event not in self._listeners:
                    self._listeners[event] = []
                self._listeners[event].extend(items)
            logger.info("bound router: %s", router.name)

    async def attach(self, token: str, callback) -> None:
        sio = socketio.AsyncClient()

        @sio.on("connect")
        async def _on_connect():
            logger.info("connected to KarboAI")
            await callback()

        @sio.on("new_message")
        async def _on_message(data):
            msg = Message.model_validate(data)
            if msg.author.user_id == self._client.id:
                return

            event = SOCKET_TOPICS.get(msg.type, "message")
            logger.info(
                "event=%s chatId=%s userId=%s type=%d",
                event, msg.chat_id, msg.author.user_id, msg.type,
            )

            for listener in self._listeners.get(event, []):
                ok = True
                for mw in listener.middlewares:
                    if not await mw(Context(self._client, msg)):
                        ok = False
                        break
                if ok:
                    await listener.callback(Context(self._client, msg))

        self._socket = sio
        await sio.connect(
            KARBO_API,
            socketio_path="/bot/ws",
            transports=["websocket"],
            auth={"bot_token": token},
        )
