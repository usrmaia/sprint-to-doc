from src.config.env import env

match env.USE_LLM_MODEL:
    case "gemini":
        from agno.models.google import Gemini

        model = Gemini(id=env.GEMINI_MODEL, api_key=env.GEMINI_API_KEY)
    case "ollama":
        from agno.models.ollama import Ollama

        model = Ollama(id=env.OLLAMA_MODEL, host=env.OLLAMA_BASE_URL)
    case "openai":
        from agno.models.openai.responses import OpenAIResponses

        model = OpenAIResponses(id=env.OPENAI_MODEL, api_key=env.OPENAI_API_KEY)

from agno.embedder.ollama import OllamaEmbedder

embedder = OllamaEmbedder(
    id=env.EMBEDDING_MODEL,
    host=env.OLLAMA_BASE_URL,
    dimensions=env.EMBEDDING_DIMENSION,
)
