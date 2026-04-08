from __future__ import annotations

from typing import Callable

from .dispatcher import Dispatcher
from .http import Http
from .logging import setup_logging
from .router import Router
from .types import (
    MembersResponse,
    Message,
    MessageResponse,
    MeResponse,
    OkResponse,
    UploadResponse,
    User,
)


class KarboAI:
    def __init__(self, token: str, id: str, enable_logging: bool = False):
        self._token = token
        self._id = id
        self._http = Http(token)
        self._dispatcher = Dispatcher(self)
        setup_logging(enable_logging)

    @property
    def id(self) -> str:
        return self._id

    async def me(self) -> MeResponse:
        return await self._http.get("/bot/me", MeResponse)

    async def text(self, chat_id: str, content: str, reply_message_id: str | None = None) -> MessageResponse:
        return await self._send(chat_id=chat_id, content=content, reply_message_id=reply_message_id)

    async def image(self, chat_id: str, images: list[str], reply_message_id: str | None = None) -> MessageResponse:
        return await self._send(chat_id=chat_id, images=images, reply_message_id=reply_message_id)

    async def upload(self, buffer: bytes, file_name: str = "file.png") -> str:
        resp = await self._http.upload("/bot/upload/image", buffer, file_name, UploadResponse)
        return resp.url

    async def message(self, chat_id: str, message_id: str) -> Message:
        return await self._http.get(f"/bot/chat/{chat_id}/message/{message_id}", Message)

    async def members(self, chat_id: str, limit: int = 100, offset: int = 0) -> MembersResponse:
        return await self._http.get(f"/bot/chat/{chat_id}/members?limit={limit}&offset={offset}", MembersResponse)

    async def user(self, user_id: str) -> User:
        return await self._http.get(f"/bot/user/{user_id}", User)

    async def leave(self, chat_id: str) -> bool:
        resp = await self._http.post(f"/bot/leave-chat/{chat_id}", {}, OkResponse)
        return resp.ok

    async def kick(self, chat_id: str, user_id: str) -> bool:
        resp = await self._http.post(f"/bot/chat/{chat_id}/kick", {"user_id": user_id}, OkResponse)
        return resp.ok

    async def attach(self, callback: Callable[[], None] | None = None) -> None:
        async def _cb():
            pass
        await self._dispatcher.attach(self._token, callback or _cb)

    def bind(self, *routers: Router) -> None:
        self._dispatcher.bind(*routers)

    async def _send(self, *, chat_id: str, content: str | None = None, images: list[str] | None = None, reply_message_id: str | None = None) -> MessageResponse:
        body: dict = {"chat_id": chat_id}
        if content:
            body["content"] = content
        if images:
            body["images"] = images
        if reply_message_id:
            body["reply_message_id"] = reply_message_id
        return await self._http.post("/bot/send-message", body, MessageResponse)
