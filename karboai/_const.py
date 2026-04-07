KARBO_API = "https://api.karboai.com"

SOCKET_TOPICS = {
    0: "message",
    1: "join",
    2: "leave",
    7: "voiceStart",
    8: "voiceEnd",
    12: "sticker",
}

ERRORS = {
    400: ("KarboAI.BadRequest", "May empty message, content too long, too many images"),
    401: ("KarboAI.Unauthorized", "Invalid bot token"),
    403: ("KarboAI.Forbidden", "Access denied"),
    404: ("KarboAI.NotFound", "Content doesn't exist"),
    413: ("KarboAI.FileTooLarge", "Please upload files smaller than XX bytes length"),
    429: ("KarboAI.TooManyRequests", "Rate limit exceeded"),
}
