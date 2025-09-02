# sprint-to-doc

Sprint To Doc é uma ferramenta que converte tasks do ClickUp em documentação estruturada em Markdown, facilitando a organização e o acompanhamento de projetos. Ideal para atualizações na documentação de projetos ágeis após sprints/releases.

## Sobre o Projeto

Sua princial ferramento é o Agno, framework para criaçao de agentes de IAs personalizados.

| [Agno](https://docs.agno.com/) | [Ollama](https://ollama.com/) | [Qdrant](https://qdrant.tech/) | [Python](https://www.python.org/) | [Docker](https://www.docker.com/) | [FastAPI](https://fastapi.tiangolo.com/)
|:--:|:--:|:--:|:--:|:--:|:--:|
| ![Agno](https://avatars.githubusercontent.com/u/104874993?s=200&v=4)| ![Ollama](https://avatars.githubusercontent.com/u/151674099?s=200&v=4) | ![Qdrant](https://avatars.githubusercontent.com/u/73504361?s=200&v=4) | ![Python](https://avatars.githubusercontent.com/u/1525981?s=200&v=4) | ![Docker](https://avatars.githubusercontent.com/u/5429470?s=200&v=4) | ![FastAPI](https://avatars.githubusercontent.com/u/156354296?s=200&v=4) |

## Estrutura


[clickup.py](./clickup.py): responsável por gerenciar a integração com a API do ClickUp. Captura as tasks concluídas que possuem a tag `agent` e salva em um markdown formatado para servir como base de conhecimento.

```python
url = f"https://api.clickup.com/api/v2/list/{_list.get('id')}/task?tags[]=agent&include_markdown_description=true&include_closed=true&statuses[]=concluído"
res_tasks = session.get(url)
```

```python
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
```
**📋 Descrição:**

```markdown
---
id: <id>
list_name: <list_name>
linked_tasks:
  - id: <linked_task_id>
    name: <linked_task_name>
---

# OG-XX - Título
**📋 Descrição:**
```

[agents.py](./agents.py): responsável por gerenciar a criação dos agentes de IA personalizados. São dois agentes: task_agent e file_agent. O primeiro é responsável por capturar, processar e tratar as tasks do ClickUp por meio da base de conhecimento e/ou API do ClickUp, enquanto o segundo lida com o armazenamento e atualização das documentações geradas.

```python
msg = "Baseando-se na task 'OG-19 - Visualizar perfil do paciente' que possui o task_id '86aa2d9fh'. Crie a documentação de requisitos."

task_content = task_agent.run(msg).content
print("task_res.content:\n", task_content)

file_content = file_agent.run(task_content).content
print("file_res.content:\n", file_content)
```

[model.py](./src/model.py): responsável por gerenciar os modelos de IA utilizados pelos agentes. Podem ser utilizando Ollama, Gemini ou OpenAI, basta especificar qual modelo utilizar em:

```
USE_LLM_MODEL=ollama | gemini | openai
```

## Comandos

### Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows
```

### Criar arquivo requirements.txt

```bash
pip freeze > requirements.txt
```

### Instalar dependências

```bash
pip install python-dotenv requests pydantic agno unstructured markdown sqlalchemy qdrant-client ollama fastembed google-genai openai uvicorn 'fastapi[standard]'
```

ou

```bash
pip install -r requirements.txt
```
