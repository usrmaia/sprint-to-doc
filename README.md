# sprint-to-doc

Sprint To Doc é uma ferramenta que converte tasks do ClickUp em documentação estruturada em Markdown, facilitando a organização e o acompanhamento de projetos. Ideal para atualizações na documentação de projetos ágeis após sprints/releases.

## Sobre o Projeto

Sua princial ferramento é o Agno, framework para criaçao de agentes de IAs personalizados.

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
pip install python-dotenv requests pydantic agno unstructured markdown sqlalchemy qdrant-client ollama fastembed google-genai openai
```

ou

```bash
pip install -r requirements.txt
```
