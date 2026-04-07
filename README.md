# KarboAI

Python library for [KarboAI](https://karboai.com) bot development.

## Install

```bash
pip install karboai
```

## Usage

```python
from karboai import KarboAI, Router, bold

karbo = KarboAI(token="your-token", id="your-bot-id", enable_logging=True)
router = Router()

@router.command("/start")
async def start(ctx):
    await karbo.text(ctx.message.chat_id, bold("Welcome!"))

@router.on("message")
async def echo(ctx):
    await karbo.text(ctx.message.chat_id, ctx.message.content)

karbo.bind(router)
karbo.attach()
```

## API

| Method | Description |
|--------|-------------|
| `me()` | Bot info |
| `text(chat_id, content, reply_message_id?)` | Send text |
| `image(chat_id, images, reply_message_id?)` | Send images |
| `upload(buffer, file_name?)` | Upload image, returns URL |
| `message(chat_id, message_id)` | Get message |
| `members(chat_id, limit?, offset?)` | Chat members |
| `user(user_id)` | User info |
| `leave(chat_id)` | Leave chat |
| `kick(chat_id, user_id)` | Kick user |
| `attach(callback?)` | Connect to WebSocket |
| `bind(*routers)` | Bind routers |

## Events

`message`, `join`, `leave`, `voiceStart`, `voiceEnd`, `sticker`

## Text formatting

`bold()`, `italic()`, `centralize()`, `code()`, `strikethrough()`, `underline()`, `hyperlink(text, url)`

## Error handling

```python
from karboai import KarboError

try:
    await karbo.me()
except KarboError as e:
    print(e.status_code, e.name, e)
```
