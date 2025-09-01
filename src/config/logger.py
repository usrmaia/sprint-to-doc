import logging

from datetime import datetime
from os import makedirs, path
from pathlib import Path

from src.config.env import env


logs_dir = path.join(Path(__file__).resolve().parent.parent.parent, "logs")
makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG if env.DEBUG else logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            filename=path.join(logs_dir, f"{datetime.now().date()}.log"),
        ),
    ],
)
