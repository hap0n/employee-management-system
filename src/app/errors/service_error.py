import traceback
from dataclasses import dataclass
from typing import Mapping


@dataclass
class Error:
    error_msg: str
    details: Mapping[str, str]
    http_code: int


class ServiceError(Exception):
    message: str = ""
    http_code: int = 500

    def __init__(self, details: dict = None, original_exception: Exception = None, message=None):
        self.details = details or {}
        self.original_exception = original_exception

        if message:
            self.message = message

        if original_exception:
            self.details["original_exception"] = traceback.format_exception(
                etype=type(original_exception), value=original_exception, tb=original_exception.__traceback__,
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.details})"

    def __str__(self) -> str:
        return self.__repr__()

    def to_domain(self) -> Error:
        return Error(error_msg=self.message, details=self.details, http_code=self.http_code)
