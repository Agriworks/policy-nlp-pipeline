
import os
from pathlib import Path

# Azure OpenAI credential
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "Enter your key here")
AZURE_API_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "Enter your endpoint here")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "Enter your deployment name here")

DEFAULT_OUTPUT_DIR = Path("./output")