import random
import string


def bold(text: str) -> str:
    return f"**{text}**"


def italic(text: str) -> str:
    return f"__{text}__"


def centralize(text: str) -> str:
    return f"[C]{text}"


def code(text: str) -> str:
    return f"`{text}`"


def strikethrough(text: str) -> str:
    return f"~~{text}~~"


def underline(text: str) -> str:
    return f"++{text}++"


def hyperlink(text: str, url: str) -> str:
    return f"[{text}]({url})"


def _router_name() -> str:
    rand = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
    return f"router-{rand}"
