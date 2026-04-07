from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from pydantic import BaseModel

if TYPE_CHECKING:
    from .client import KarboAI


class BotStatus(str, Enum):
    NOT_OFFICIAL = "NOT_OFFICIAL"
    OFFICIAL = "OFFICIAL"
    BANNED = "BANNED"


class Frame(BaseModel):
    frame_id: str
    file: str


class Reaction(BaseModel):
    reaction: str
    is_sticker: bool
    count: int
    me: bool


class Author(BaseModel):
    user_id: str
    nickname: str
    avatar_url: str
    avatar_frame: Frame | None = None
    role: int | None = None
    app_role: int | None = None
    panel_color: str | None = None
    level: int | None = None
    nickname_color: str | None = None
    nickname_emoji: str | None = None


class User(BaseModel):
    user_id: str
    nickname: str
    avatar: str
    role: int
    short_info: str


class Member(BaseModel):
    user_id: str
    nickname: str
    avatar: str
    role: int


class Message(BaseModel):
    message_id: str
    chat_id: str
    content: str
    created_time: int
    type: int
    reply_message_id: str | None = None
    audio: str | None = None
    sticker: str | None = None
    images: list[str] = []
    author: Author
    audio_duration_ms: int | None = None
    waveform: list[Any] | None = None
    video_note: str | None = None
    video_note_duration_ms: int | None = None
    transparent: bool | None = None
    bubble_id: str | None = None
    bubble_version: int | None = None
    reactions: list[Reaction] | None = None


class MeResponse(BaseModel):
    bot_id: str
    name: str
    status: BotStatus


class MessageResponse(BaseModel):
    message_id: str
    created_time: int


class UploadResponse(BaseModel):
    url: str


class MembersResponse(BaseModel):
    items: list[User]


class OkResponse(BaseModel):
    ok: bool


class Context:
    __slots__ = ("karbo", "message")

    def __init__(self, karbo: KarboAI, message: Message):
        self.karbo = karbo
        self.message = message


EventHandler = Callable[[Context], Awaitable[None]]
Middleware = Callable[[Context], Awaitable[bool | None]]
ConnectCallback = Callable[[], Awaitable[None]]


class _Listener:
    def __init__(self, callback: EventHandler, middlewares: list[Middleware]):
        self.callback = callback
        self.middlewares = middlewares
