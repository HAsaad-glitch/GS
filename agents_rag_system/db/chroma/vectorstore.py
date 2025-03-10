"""
ChromaDB vector store implementation with fallback to in-memory client.
Compatible with recent Chroma versions (>=0.6.x).
"""
from typing import Dict, Any, List, Optional
import os
from GS.agents_rag_system.config.config import RAGConfig
import chromadb
import chromadb.errors

from chromadb.utils import embedding_functions

try:
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    HAS_ST_EMBEDDING_FUNC = True
except ImportError:
    HAS_ST_EMBEDDING_FUNC = False

class ChromaVectorStore:
    """ChromaDB vector store implementation."""

    def __init__(self, config: RAGConfig):
        """Initialize the ChromaDB vector store."""
        self.config = config
        self.use_http_client = self.config.additional_params.get("use_http_client", False)
        self.use_in_memory = self.config.additional_params.get("use_in_memory", False)
        self.client = self._setup_client()
        self.embedding_function = self._setup_embedding_function()
        self.collection = self._get_or_create_collection()

    def _setup_client(self) -> chromadb.Client:
        """Set up the ChromaDB client."""
        if self.use_in_memory:
            print("Using in-memory ChromaDB client (no persistence)")
            return chromadb.Client()

        if self.use_http_client:
            from chromadb.config import Settings
            host = self.config.additional_params.get("chroma_host", "localhost")
            port = self.config.additional_params.get("chroma_port", 8000)
            ssl = self.config.additional_params.get("chroma_ssl", False)

            print(f"Connecting to ChromaDB via HTTP at {host}:{port} (SSL: {ssl})")

            try:
                client = chromadb.HttpClient(
                    host=host,
                    port=port,
                    ssl=ssl,
                    settings=Settings(anonymized_telemetry=False)
                )
                # Test connection
                client.heartbeat()
                print("Successfully connected to ChromaDB")
                return client
            except Exception as e:
                print(f"⚠️ Warning: HTTP client connection failed: {e}")
                print("Falling back to in-memory ChromaDB client (no persistence)")
                self.use_in_memory = True
                return chromadb.Client()

        # Default: Use local persistent client
        persist_directory = self.config.persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        return chromadb.PersistentClient(path=persist_directory)

    def _setup_embedding_function(self):
        """Set up the embedding function, fallback to custom if SentenceTransformerEmbeddingFunction isn't available."""
        if HAS_ST_EMBEDDING_FUNC:
            print("Using SentenceTransformerEmbeddingFunction from Chroma (if installed).")
            return SentenceTransformerEmbeddingFunction(model_name=self.config.embedding_model)

        print("SentenceTransformerEmbeddingFunction not found. Using a custom embedding function...")
        from sentence_transformers import SentenceTransformer

        class CustomSentenceTransformerEmbeddingFunction(embedding_functions.EmbeddingFunction):
            def __init__(self, model_name: str):
                self._model = SentenceTransformer(model_name)

            def __call__(self, texts: List[str]) -> List[List[float]]:
                return self._model.encode(texts).tolist()

        return CustomSentenceTransformerEmbeddingFunction(model_name=self.config.embedding_model)

    def _get_or_create_collection(self) -> chromadb.Collection:
        """Get or create a ChromaDB collection."""
        return self.client.get_or_create_collection(
            name=self.config.collection_name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        """Add documents to the vector store."""
        if not documents:
            return
        ids = [doc.get("id") for doc in documents]
        texts = [doc.get("text") for doc in documents]
        metadatas = [doc.get("metadata", {}) for doc in documents]

        try:
            self.collection.add(
                ids=ids,
                documents=texts,
                metadatas=metadatas
            )
        except Exception as e:
            print(f"Error adding documents: {e}")

    def query(self, query_text: str, n_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """Query the vector store for similar documents."""
        if not query_text.strip():
            return []
        n_results = n_results or self.config.similarity_top_k

        if self.collection.count() == 0:
            return []

        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
        except Exception as e:
            print(f"Query failed: {e}")
            return []

        documents = []
        if results.get('ids') and len(results['ids'][0]) > 0:
            for i in range(len(results['ids'][0])):
                documents.append({
                    "id": results['ids'][0][i],
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results.get('metadatas') else {},
                    "distance": results['distances'][0][i] if 'distances' in results else None,
                })
        return documents

    def delete_collection(self) -> None:
        """Delete the collection."""
        try:
            self.client.delete_collection(self.config.collection_name)
        except Exception as e:
            print(f"Error deleting collection: {e}")

    def get_collection_count(self) -> int:
        """Get the number of documents in the collection."""
        return self.collection.count()