import chromadb
from sentence_transformers import SentenceTransformer #

class RAGPipeline:
    def __init__(self, collection_name="study_notes"):
        # initialize embedding model
        print("Loading embedding model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # initialize ChromaDB
        self.client = chromadb.PersistentClient(path="./chroma_db") # initialize data base
        self.collection = self.client.get_or_create_collection( # set collection
            name=collection_name
        )
        print("RAG pipeline ready!")

    def add_document(self, text, doc_name):
        # split text into chunks
        chunks = self.split_into_chunks(text, chunk_size=500)
        
        # embed each chunk and store
        for i, chunk in enumerate(chunks):
            embedding = self.embedder.encode(chunk).tolist()
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"{doc_name}_chunk_{i}"]
            )
        
        print(f"Added {len(chunks)} chunks from {doc_name}")
        return len(chunks)

    def split_into_chunks(self, text, chunk_size=500):
        # split by words, group into chunks
        words = text.split() # large string of words
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            current_chunk.append(word)
            current_size += 1
            if current_size >= chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_size = 0

        # add remaining words
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def search_with_sources(self, query, n_results=3):
        # embed the query
        query_embedding = self.embedder.encode(query).tolist()
        
        # search for similar chunks
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        chunks = results['documents'][0]
        distances = results['distances'][0]
        
        # return just the text chunks
        return list(zip(chunks,distances))

    def get_context(self, query):
        chunks = self.search_with_sources(query)
        return "\n\n".join(chunks)