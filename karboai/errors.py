from ._const import ERRORS


class KarboError(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code
        name, msg = ERRORS.get(status_code, ("KarboAI.Unknown", "Unknown error"))
        self.name = name
        super().__init__(msg)
