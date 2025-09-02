import src.config.logger

from agno.agent import Agent

from src.config.env import env
from src.knowledge import knowledge, memory, storage
from src.model import model
from src.tools import clickup_tools, file_tools
from src.prompts import (
    task_instructions,
    task_system_message,
    file_instructions,
    file_system_message,
)

task_agent = Agent(
    model=model,
    name="Task Agent",
    agent_id="task_agent",
    instructions=task_instructions,
    system_message=task_system_message,
    memory=memory,
    knowledge=knowledge,
    storage=storage,
    tools=[clickup_tools],
    show_tool_calls=env.DEBUG,
    markdown=True,
    add_history_to_messages=True,
    num_history_runs=1,
    enable_user_memories=True,
    enable_session_summaries=True,
    add_datetime_to_instructions=True,
    debug_mode=env.DEBUG,
    telemetry=False,
)

task_agent.reset_session()  # Bug

file_agent = Agent(
    model=model,
    name="File Agent",
    agent_id="file_agent",
    instructions=file_instructions,
    system_message=file_system_message,
    tools=[file_tools],
    show_tool_calls=env.DEBUG,
    markdown=True,
    num_history_runs=1,
    debug_mode=env.DEBUG,
    telemetry=False,
)

file_agent.reset_session()  # Bug

if __name__ == "__main__":
    msg = "Baseando-se na task 'OG-19 - Visualizar perfil do paciente' que possui o task_id '86aa2d9fh'. Crie a documentação de requisitos."

    task_content = task_agent.run(msg).content
    print("task_res.content:\n", task_content)

    file_content = file_agent.run(task_content).content
    print("file_res.content:\n", file_content)
