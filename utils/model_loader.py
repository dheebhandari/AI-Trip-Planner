import os
from typing import Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from dotenv import load_dotenv


# Load .env variables
load_dotenv()


class ConfigLoader:
    def __init__(self):
        print("Loading config...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):

    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        # Auto load config after init
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        Load and return Groq LLM
        """
        print("LLM loading...")
        print("Using provider: Groq")

        # Get API key
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            raise ValueError("❌ GROQ_API_KEY not found in environment variables")

        # Get model name from config
        model_name = self.config["llm"]["groq"]["model_name"]

        print(f"Loading model: {model_name}")

        # Create LLM
        llm = ChatGroq(
            model=model_name,
            api_key=groq_api_key
        )

        return llm
