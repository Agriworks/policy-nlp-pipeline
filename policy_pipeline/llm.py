
from policy_pipeline.parameters import AZURE_API_ENDPOINT, AZURE_API_KEY, AZURE_DEPLOYMENT_NAME
from openai import AzureOpenAI

def get_azure_llm_client() -> AzureOpenAI:

    if not all([AZURE_API_KEY, AZURE_API_ENDPOINT, AZURE_DEPLOYMENT_NAME]):
        raise Exception("⚠️ Missing Azure OpenAI credentials in .env")
    else:
        client = AzureOpenAI(
            api_key=AZURE_API_KEY,
            api_version="2024-02-15-preview",
            azure_endpoint=AZURE_API_ENDPOINT,
            azure_deployment=AZURE_DEPLOYMENT_NAME,
        )

    return client
