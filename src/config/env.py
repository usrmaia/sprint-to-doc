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
    CLICKUP_SPACE_ID: str = Field(..., min_length=1)

    CHUNK_SIZE: int = Field(..., gt=0)
    CHUNK_OVERLAP: int = Field(..., ge=0)
    NUM_DOCUMENTS: int = Field(..., gt=0)

    USE_LLM_MODEL: Literal["gemini", "ollama", "openai"]
    GEMINI_MODEL: Optional[str]
    GEMINI_API_KEY: Optional[str]
    OLLAMA_MODEL: Optional[str]
    OLLAMA_BASE_URL: Optional[str]
    OPENAI_MODEL: Optional[str]
    OPENAI_API_KEY: Optional[str]

    EMBEDDING_MODEL: Optional[str]
    EMBEDDING_DIMENSION: int = Field(..., gt=0)

    VECTOR_DB_COLLECTION: str = Field(..., min_length=1)
    VECTOR_DB_RECREATE: bool
    QDRANT_URL: str = Field(..., min_length=1)

load_dotenv()

env = _ENV(
    ENV=getenv("ENV", "development"),  # type: ignore
    DEBUG=getenv("DEBUG", "False").lower() in ("true", "1"),
    DATA_DIR=Path(__file__).parent.parent.parent / getenv("DATA_DIR", "data"),
    CLICKUP_ACCESS_TOKEN=getenv("CLICKUP_ACCESS_TOKEN", None),
    CLICKUP_SELECTED_LIST_NAME=list(
        map(
            str.strip,
            getenv("CLICKUP_SELECTED_LIST_NAME", "").split(","),
        )
    ),
    CLICKUP_SPACE_ID=getenv("CLICKUP_SPACE_ID", None),
    CHUNK_SIZE=getenv("CHUNK_SIZE", None),
    CHUNK_OVERLAP=getenv("CHUNK_OVERLAP", None),
    NUM_DOCUMENTS=getenv("NUM_DOCUMENTS", None),
    USE_LLM_MODEL=getenv("USE_LLM_MODEL", None),
    GEMINI_MODEL=getenv("GEMINI_MODEL", None),
    GEMINI_API_KEY=getenv("GEMINI_API_KEY", None),
    OLLAMA_MODEL=getenv("OLLAMA_MODEL", None),
    OLLAMA_BASE_URL=getenv("OLLAMA_BASE_URL", None),
    OPENAI_MODEL=getenv("OPENAI_MODEL", None),
    OPENAI_API_KEY=getenv("OPENAI_API_KEY", None),
    EMBEDDING_MODEL=getenv("EMBEDDING_MODEL", None),
    EMBEDDING_DIMENSION=getenv("EMBEDDING_DIMENSION", 0),
    VECTOR_DB_COLLECTION=getenv("VECTOR_DB_COLLECTION", None),
    VECTOR_DB_RECREATE=getenv("VECTOR_DB_RECREATE", "false").lower() in ("true", "1"),
    QDRANT_URL=getenv("QDRANT_URL", None),
)
