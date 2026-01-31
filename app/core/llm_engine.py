# app/core/llm_engine.py
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# We can use Llama 3.1 or Mistral. Llama 3.1 is excellent.
REPO_ID = "meta-llama/Llama-3.1-8B-Instruct"

def get_llm():
    """
    Returns a ChatHuggingFace model that handles the formatting
    required by the free Hugging Face API.
    """
    sec_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not sec_key:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in .env file")

    # 1. Create the base endpoint
    endpoint = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        task="text-generation",
        max_new_tokens=1024,
        do_sample=False, # Deterministic for research
        huggingfacehub_api_token=sec_key,
    )

    # 2. Wrap it in ChatHuggingFace
    # This automatically adds the <|begin_of_text|> tokens needed
    chat_model = ChatHuggingFace(
        llm=endpoint,
        verbose=True
    )
    
    return chat_model