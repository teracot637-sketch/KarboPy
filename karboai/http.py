import json
from typing import Type, TypeVar

import aiohttp
from pydantic import BaseModel

from ._const import KARBO_API
from .errors import KarboError
from .logging import logger

T = TypeVar("T", bound=BaseModel)


class Http:
    def __init__(self, token: str):
        self._headers = {
            "Content-Type": "application/json",
            "Bot-Token": token,
        }

    async def _request(self, method: str, path: str, schema: Type[T], **kwargs) -> T:
        url = f"{KARBO_API}{path}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self._headers, **kwargs) as resp:
                if not resp.ok:
                    logger.error("%s %s -> %d", method, path, resp.status)
                    raise KarboError(resp.status)
                logger.info("%s %s -> %d", method, path, resp.status)
                return schema.model_validate(await resp.json())

    async def get(self, path: str, schema: Type[T]) -> T:
        return await self._request("GET", path, schema)

    async def post(self, path: str, body: dict, schema: Type[T]) -> T:
        return await self._request("POST", path, schema, data=json.dumps(body))

    async def upload(self, path: str, buffer: bytes, file_name: str, schema: Type[T]) -> T:
        import mimetypes

        form = aiohttp.FormData()
        form.add_field(
            "file",
            buffer,
            filename=file_name,
            content_type=mimetypes.guess_type(file_name)[0] or "image/png",
        )

        headers = {k: v for k, v in self._headers.items() if k != "Content-Type"}
        return await self._request("POST", path, schema, data=form, headers=headers)
