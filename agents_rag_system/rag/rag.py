"""
RAG (Retrieval Augmented Generation) implementation.
"""
from typing import Dict, Any, List, Optional, Union, Callable
import os
import hashlib
from pathlib import Path
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader, 
    PyPDFLoader, 
    UnstructuredFileLoader
)
from GS.agents_rag_system.config.config import RAGConfig
from GS.agents_rag_system.db.chroma.vectorstore import ChromaVectorStore

class DocumentProcessor:
    """Document processor for loading and splitting documents."""
    
    def __init__(self, config: RAGConfig):
        """Initialize the document processor."""
        self.config = config
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
        )
    
    def load_document(self, file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        """
        Load a document from the file path.
        
        Args:
            file_path: Path to the document.
            
        Returns:
            List of document chunks.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine the loader based on file extension
        if file_path.suffix.lower() == '.pdf':
            loader = PyPDFLoader(str(file_path))
        else:
            # Use UnstructuredFileLoader for most document types
            try:
                loader = UnstructuredFileLoader(str(file_path))
            except:
                # Fallback to text loader
                loader = TextLoader(str(file_path))
        
        # Load the document
        documents = loader.load()
        
        # Split the document into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Convert the chunks to the format expected by ChromaVectorStore
        result = []
        for i, chunk in enumerate(chunks):
            # Generate a unique ID for each chunk
            doc_id = self._generate_doc_id(file_path, i)
            
            # Add the chunk to the result
            result.append({
                "id": doc_id,
                "text": chunk.page_content,
                "metadata": {
                    **chunk.metadata,
                    "chunk_index": i,
                    "source": str(file_path),
                }
            })
        
        return result
    
    def load_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Load a text string.
        
        Args:
            text: Text to load.
            metadata: Metadata for the text.
            
        Returns:
            List of document chunks.
        """
        # Split the text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Convert the chunks to the format expected by ChromaVectorStore
        result = []
        for i, chunk in enumerate(chunks):
            # Generate a unique ID for each chunk
            doc_id = str(uuid.uuid4())
            
            # Add the chunk to the result
            result.append({
                "id": doc_id,
                "text": chunk,
                "metadata": {
                    **(metadata or {}),
                    "chunk_index": i,
                }
            })
        
        return result
    
    def _generate_doc_id(self, file_path: Path, chunk_index: int) -> str:
        """
        Generate a document ID from the file path and chunk index.
        
        Args:
            file_path: Path to the document.
            chunk_index: Index of the chunk.
            
        Returns:
            Document ID.
        """
        file_hash = hashlib.md5(str(file_path).encode()).hexdigest()
        return f"{file_hash}_{chunk_index}"


class RAG:
    """RAG (Retrieval Augmented Generation) implementation."""
    
    def __init__(self, config: RAGConfig):
        """Initialize the RAG component."""
        self.config = config
        self.vector_store = ChromaVectorStore(config)
        self.document_processor = DocumentProcessor(config)
    
    def add_document(self, file_path: Union[str, Path]) -> None:
        """
        Add a document to the RAG component.
        
        Args:
            file_path: Path to the document.
        """
        chunks = self.document_processor.load_document(file_path)
        self.vector_store.add_documents(chunks)
    
    def add_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a text string to the RAG component.
        
        Args:
            text: Text to add.
            metadata: Metadata for the text.
        """
        chunks = self.document_processor.load_text(text, metadata)
        self.vector_store.add_documents(chunks)
    
    def query(self, query: str, n_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Query the RAG component.
        
        Args:
            query: Query text.
            n_results: Number of results to return.
            
        Returns:
            List of relevant documents.
        """
        return self.vector_store.query(query, n_results)
    
    def augment_prompt(self, prompt: str, query: str, n_results: Optional[int] = None) -> str:
        """
        Augment a prompt with retrieved documents.
        
        Args:
            prompt: Original prompt.
            query: Query to use for retrieval.
            n_results: Number of results to return.
            
        Returns:
            Augmented prompt.
        """
        documents = self.query(query, n_results)
        
        # Format the retrieved documents
        context = "\n\n".join([f"[Document {i+1}]\n{doc['text']}" for i, doc in enumerate(documents)])
        
        # Augment the prompt with the context
        augmented_prompt = f"""
{prompt}

Here is some relevant context that might help you:

{context}

Please use this context to inform your response.
"""
        
        return augmented_prompt
    
    def clear(self) -> None:
        """Clear the RAG component."""
        self.vector_store.delete_collection()
        # Recreate the collection
        self.vector_store = ChromaVectorStore(self.config) 