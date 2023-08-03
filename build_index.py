#This script will incorporate Ray

import os, chromadb, logging, ray, time
from llama_index import SimpleDirectoryReader
import os, chromadb, openai
from dotenv import load_dotenv
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
from llama_index import download_loader
load_dotenv()
openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_embeddings():
    try:
        print("Loading data...") 
        documents = SimpleDirectoryReader('data').load_data()
        print("Data loaded.")
    except Exception as e:
        print("Error loading data: {e}")
    
    remote_db = chromadb.HttpClient(host="", port=8000)
    
    collection_name = "data-mini-1"
    collections = [col.name for col in remote_db.list_collections()]
    print(f"Collections: {collections}")
    
    embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
         )

    chroma_collection = remote_db.create_collection(collection_name)
   
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    
    print(f"Beginning the embedding for {collection_name}")
    start_time = time.time()
    VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=service_context, embed_model=embed_model
        )
    print("Embedding complete.")
    end_time = time.time()
    execution_time = end_time - start_time
    print("Total execution time:", execution_time)


def generate_or_return_embeddings():
    #Load files
    documents = SimpleDirectoryReader('data').load_data()
    
    #Define embedding model
    embed_model = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    )
    #Define service context - bundle of commonly used resources using during indexing/querying stage in pipeline
    service_context = ServiceContext.from_defaults(embed_model=embed_model) 

    #Connect to Chroma
    chroma_db = chromadb.HttpClient(host="", port=8000)
    #Name the collection
    collection_name = "data-mini-1"
    collections = [col.name for col in chroma_db.list_collections()]
    
    if collection_name in collections:
        print("Collection exists. Building index..")
        chroma_collection = chroma_db.get_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)
        return index    
    else:
        print("New collection. Generating embeddings then building index...")
        chroma_collection = chroma_db.create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        #Abstraction for storing Nodes, indices, and vectors
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, service_context=service_context, embed_model=embed_model
        )
        return index


def query_chroma(index, query):
    chat_engine = index.as_chat_engine()

    response = chat_engine.chat(
            f"""Given the context, answer the following question {query}. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
        """)
    return response