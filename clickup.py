import requests
import logging

from src.config.env import env
import src.config.logger

# https://developer.clickup.com/reference
# https://developer.clickup.com/openapi

session = requests.Session()

session.headers.update(
    {
        "Authorization": f"Bearer {env.CLICKUP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
)

res_team = session.get(f"https://api.clickup.com/api/v2/team")
team_id = res_team.json().get("teams")[0].get("id")
logging.info(f"Team ID: {team_id}")

res_space = session.get(f"https://api.clickup.com/api/v2/team/{team_id}/space")
space_id = res_space.json().get("spaces")[0].get("id")
logging.info(f"Space ID: {space_id}")

res_folder = session.get(f"https://api.clickup.com/api/v2/space/{space_id}/folder")
folders = res_folder.json().get("folders", [])
projects_folder = list(filter(lambda f: f.get("name") == "Projetos", folders))[0]
lists = projects_folder.get("lists", [])
selected_lists = list(
    filter(
        lambda l: l.get("name").startswith(tuple(env.CLICKUP_SELECTED_LIST_NAME)), lists
    )
)
selected_lists = list(
    map(lambda l: {"id": l.get("id"), "name": l.get("name")}, selected_lists)
)
logging.info(f"Selected Lists IDs: {selected_lists}")

completed_tasks = []
for _list in selected_lists:
    url = f"https://api.clickup.com/api/v2/list/{_list.get('id')}/task?tags[]=agent&include_markdown_description=true&include_closed=true&statuses[]=concluído"
    res_tasks = session.get(url)
    tasks = res_tasks.json().get("tasks", [])
    completed_tasks.extend(tasks)
    logging.info(
        f"Completed Tasks for List ID {_list.get('id')} - {_list.get('name')}: {len(tasks)}"
    )

import json
import os

os.makedirs(env.DATA_DIR, exist_ok=True)

with open(env.DATA_DIR / "completed_tasks_full.json", "w", encoding="utf-8") as f:
    json.dump(completed_tasks, f, ensure_ascii=False, indent=2)

    logging.info("Completed tasks written to completed_tasks_full.json")

formatted_tasks = []
with open(env.DATA_DIR / "completed_tasks.json", "w", encoding="utf-8") as f:
    formatted_tasks = list(
        map(
            lambda ct: {
                "id": ct.get("id"),
                "name": ct.get("name"),
                "description": ct.get("markdown_description"),
                "list_name": ct.get("list").get("name"),
                "linked_tasks": list(
                    map(
                        lambda lt: {
                            "id": (
                                lt.get("task_id")
                                if ct.get("id") != lt.get("task_id")
                                else lt.get("link_id")
                            ),
                            "name": next(
                                (
                                    act.get("name")
                                    for act in completed_tasks  # act - aux completed_tasks
                                    if (
                                        ct.get("id") != lt.get("task_id")
                                        and lt.get("task_id") == act.get("id")
                                    )
                                    or (
                                        ct.get("id") == lt.get("task_id")
                                        and lt.get("link_id") == act.get("id")
                                    )
                                ),
                                "Task not found",
                            ),
                        },
                        ct.get("linked_tasks", []),
                    )
                ),
            },
            completed_tasks,
        )
    )

    json.dump(formatted_tasks, f, ensure_ascii=False, indent=2)

    logging.info("Completed tasks written to completed_tasks.json")

os.makedirs(env.DATA_DIR / "tasks", exist_ok=True)

for task in formatted_tasks:
    with open(
        env.DATA_DIR / "tasks" / f"{task.get('id')}.md", "w", encoding="utf-8"
    ) as f:
        # frontmatter YAML - metadados
        f.write("---\n")
        f.write(f"id: {task.get('id')}\n")
        f.write(f"list_name: \"{task.get('list_name')}\"\n")

        linked_tasks = task.get("linked_tasks", [])
        if linked_tasks:
            f.write("linked_tasks:\n")
            for linked_task in linked_tasks:
                f.write(f"  - id: {linked_task.get('id')}\n")
                f.write(f"    name: \"{linked_task.get('name')}\"\n")

        f.write("---\n\n")

        # Conteúdo da tarefa
        f.write(f"# {task.get('name')}\n")
        f.write(f"{task.get('description')}\n")

file_tasks_id = os.listdir(env.DATA_DIR / "tasks")
active_task_file_paths = [f"{task.get('id')}.md" for task in formatted_tasks]

for file in file_tasks_id:
    if file not in active_task_file_paths:
        os.remove(env.DATA_DIR / "tasks" / file)
