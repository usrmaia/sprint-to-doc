from agno.tools.file import FileTools
from agno.tools.clickup_tool import ClickUpTools

from src.config.env import env

base_dir = env.DATA_DIR / "docs"

file_tools = FileTools(base_dir=base_dir)

clickup_tools = ClickUpTools(
    api_key=env.CLICKUP_ACCESS_TOKEN,
    master_space_id=env.CLICKUP_SPACE_ID,
    create_task=False,
    update_task=False,
    delete_task=False,
)
