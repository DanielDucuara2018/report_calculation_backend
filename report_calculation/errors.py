from typing import Any


class Error(Exception):
    code: int
    reason: str
    description: str

    def __init__(self, **data: Any):
        self.data = data

    def __str__(self):
        fields = [
            ("code", self.code),
            ("reason", self.reason),
            ("data", repr(self.data)),
        ]
        fields_repr = ", ".join(f"{field}={value}" for field, value in fields)
        return fields_repr


class InvalidSymbol(Error):

    code = 1000
    reason = "invalid-symbol"
    description = "Invalid symbol in exchange."


class NoDataFound(Error):

    code = 1001
    reason = "no-data-found"
    description = "No data found in DB."


class NoUserFound(Error):
    code = 1002
    reason = "no-user-found"
    description = "No user found in DB."


class NoTeletramBotProcess(Error):
    code = 1003
    reason = "not-telegram-bot-running"
    description = "There is not telegram bot running."


class TeletramBotAlreadyRunning(Error):
    code = 1004
    reason = "telegram-bot-alredy-running"
    description = "There is already a telegram bot running"
