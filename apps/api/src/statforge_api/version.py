"""API version information."""

from importlib.metadata import version
from typing import Literal

from pydantic import BaseModel


class VersionResponse(BaseModel):
    name: str
    version: str
    api: Literal["v1"]


def current_version() -> VersionResponse:
    return VersionResponse(name="StatForge API", version=version("statforge-api"), api="v1")
