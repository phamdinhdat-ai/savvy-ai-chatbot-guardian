
from typing import List, Tuple, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer

class RAGEngine:
    """
    Retrieval Augmented Generation engine that retrieves relevant content
    to enhance LLM responses.
    """
    
    def __init__(self):
        # Initialize the embedding model for semantic search
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Initialize ChromaDB as our vector store
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="knowledge_base",
            metadata={"description": "Knowledge base for the AI chatbot"}
        )
        
        # In a real implementation, we would load documents here
        self._load_documents()
    
    def _load_documents(self):
        """Load and index documents into the vector database"""
        # This is a simplified example. In a real implementation,
        # you would load documents from files, databases, APIs, etc.
        documents = [
            "RAG (Retrieval Augmented Generation) is a technique that enhances LLM responses by first retrieving relevant information.",
            "Guardrails provide safety mechanisms for LLM outputs to prevent harmful content.",
            "Kubernetes is an open-source platform for managing containerized workloads and services.",
            "Docker containers package up code and all its dependencies so the application runs quickly and reliably.",
            "Python is a high-level, interpreted programming language known for its readability and versatility.",
            # Add more documents here
        ]
        
        # Generate embeddings and add to collection
        embeddings = self.embedding_model.encode(documents)
        
        # Add documents to the collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
    
    def retrieve(self, query: str, top_k: int = 3) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Retrieve relevant documents based on the query.
        
        Args:
            query: The user's query string
            top_k: Number of documents to retrieve
            
        Returns:
            Tuple containing:
                - Combined context string
                - List of source information dictionaries
        """
        # Embed the query
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Perform the search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Extract the documents and metadata
        retrieved_docs = results['documents'][0]
        doc_ids = results['ids'][0]
        
        # Prepare source information
        sources = [
            {"id": doc_id, "content": doc[:100] + "..."}
            for doc_id, doc in zip(doc_ids, retrieved_docs)
        ]
        
        # Combine the retrieved documents into a context
        context = "\n\n".join(retrieved_docs)
        
        return context, sources
