"""API version information."""
import os  # deliberate lint error (F401) for TC-01.4

from importlib.metadata import version
from typing import Literal

from pydantic import BaseModel


class VersionResponse(BaseModel):
    name: str
    version: str
    api: Literal["v1"]


def current_version() -> VersionResponse:
    return VersionResponse(name="StatForge API", version=version("statforge-api"), api="v1")
