from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel, Field
from os import getenv
from typing import Literal, Optional


class _ENV(BaseModel):
    ENV: Literal["development", "production"]
    DEBUG: bool
    DATA_DIR: Path

    CLICKUP_ACCESS_TOKEN: str = Field(..., min_length=1)
    CLICKUP_SELECTED_LIST_NAME: list[str] = Field(..., min_length=1)

load_dotenv()

env = _ENV(
    ENV=getenv("ENV", "development"),  # type: ignore
    DEBUG=getenv("DEBUG", "False").lower() in ("true", "1"),
    CLICKUP_ACCESS_TOKEN=getenv("CLICKUP_ACCESS_TOKEN", None),
    CLICKUP_SELECTED_LIST_NAME=list(
        map(
            str.strip,
            getenv("CLICKUP_SELECTED_LIST_NAME", "").split(","),
        )
    ),
)
