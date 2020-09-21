from typing import Any

from pydantic import BaseModel

from .core import Response


class ValidationErrorContent(BaseModel):
    detail: Any
    body: Any


class ValidationErrorResponse(Response):
    content: ValidationErrorContent
