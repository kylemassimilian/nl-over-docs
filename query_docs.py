import os, chromadb, openai
from chromadb.config import Settings
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

def index_chroma():
    
    chroma_client = chromadb.HttpClient(host="3.208.86.57", port=8000)


    chroma_collection = chroma_client.get_collection("Investments")

