# from agno.document.chunking.semantic import SemanticChunking Not Working
from agno.document.chunking.document import DocumentChunking
from agno.document.reader.markdown_reader import MarkdownReader
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.vectordb.qdrant import Qdrant
from agno.vectordb.search import SearchType

from src.config.env import env
from src.model import embedder

chunking_strategy = DocumentChunking(
    chunk_size=env.CHUNK_SIZE,
    overlap=env.CHUNK_OVERLAP,
)

reader = MarkdownReader(
    chunk_size=env.CHUNK_SIZE,
    chunking_strategy=chunking_strategy,
)

vector_db = Qdrant(
    collection=env.VECTOR_DB_COLLECTION,
    url=env.QDRANT_URL,
    embedder=embedder,
    search_type=SearchType.hybrid,
)

if env.VECTOR_DB_RECREATE:
    vector_db.delete()
    vector_db.create()

knowledge = MarkdownKnowledgeBase(
    reader=reader,
    vector_db=vector_db,
    num_documents=env.NUM_DOCUMENTS,
    chunking_strategy=chunking_strategy,
    path=env.DATA_DIR / "tasks",
)

knowledge.load()

db_file = env.DATA_DIR / "data.db"

storage = SqliteStorage(
    table_name="agent_sessions",
    db_file=db_file,
)

memory_db = SqliteMemoryDb(table_name="memory", db_file=db_file)

memory = Memory(db=memory_db, debug_mode=env.DEBUG)
