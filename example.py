from karboai import KarboAI, Router, bold, italic

karbo = KarboAI(
    token="your-bot-token",
    id="your-bot-id",
    enable_logging=True,
)

router = Router()


@router.command("/start")
async def on_start(ctx):
    await karbo.text(ctx.message.chat_id, bold("Hello! Welcome to KarboAI bot."))


@router.command("/help")
async def on_help(ctx):
    await karbo.text(
        ctx.message.chat_id,
        "Available commands:\n/start\n/help",
    )


@router.on("message")
async def on_message(ctx):
    await karbo.text(ctx.message.chat_id, f"You said: {italic(ctx.message.content)}")


@router.on("join")
async def on_join(ctx):
    await karbo.text(ctx.message.chat_id, f"Welcome, {ctx.message.author.nickname}!")


karbo.bind(router)
karbo.attach()

import asyncio

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
