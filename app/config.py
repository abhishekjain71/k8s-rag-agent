""" Centralized Pydantic-validation application settings. """

import os
from urllib.parse import quote, urlunsplit
from dotenv import load_dotenv
load_dotenv()
from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings():
    """ 
    Load and validate environment variables from '.env'
    
    """
    
   
    
     # --- JINA AI (embeddings + reranker) ---
    JINA_API_KEY = os.getenv("JINA_API_KEY")
    GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
    QDRANT_URL= os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY= os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION= "Enterprise-RAG"
    
    GROQ_API_KEY= os.getenv("GROQ_API_KEY")
    GROQ_MODEL= "llama-3.3-70b-versatile"
    GROQ_FALLBACK_API_KEY= os.getenv("GROQ_FALLBACK_API_KEY")
    
    PORTKEY_API_KEY= os.getenv("PORTKEY_API_KEY")
    PORTKEY_CONFIG_SLUG= os.getenv("PORTKEY_CONFIG_SLUG")
    GROQ_SLUG= "rag1"       # <-- ye add karo, Portkey virtual key ID
    GEMINI_SLUG= "rag2"    # <-- agar Gemini bhi Portkey se route ho raha hai
    
    
settings= Settings()


