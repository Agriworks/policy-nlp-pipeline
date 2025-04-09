from dataclasses import dataclass
from typing import List, Tuple
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.pipelines import pipeline
from transformers.models.auto.modeling_auto import AutoModelForTokenClassification

from policy_pipeline.llm import get_azure_llm_client
from policy_pipeline.parameters import AZURE_DEPLOYMENT_NAME

tokenizer = AutoTokenizer.from_pretrained("gauravnuti/agro-ner")
model = AutoModelForTokenClassification.from_pretrained("gauravnuti/agro-ner")
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")


@dataclass
class NERResults():
    raw_entities: List[Tuple[str, str]]
    entity_text_relationship: str



def generate_ner(text: str) -> NERResults:
    if not ner_pipeline:
        raise Exception("⚠️ NER model not loaded")
    
    entities = ner_pipeline(text)

    if entities:
        entity_text = "\n".join([f"- {e['word']} ({e['entity_group']})" for e in entities])
    else:
        entity_text = "No entities found."

    prompt = (
        f"Text: {text}\n\n"
        f"Entities:\n{entity_text}\n\n"
        "Give a precise summary focusing on the relationships between the entities."
    )

    client = get_azure_llm_client()

    response = client.chat.completions.create(
            model=AZURE_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
    processed_output= response.choices[0].message.content.strip()

    return NERResults(
        raw_entities=[(e['word'], e['entity_group']) for e in entities],
        entity_text_relationship=processed_output
    )


def generate_summary(text: str, ner_results: NERResults) -> str:
    # TODO: @praneeth - create the chain of thought to generate the summary using the text and the ner results
    entities = ner_results.raw_entities
    entity_text_relationship = ner_results.entity_text_relationship
    prompt=f"""
    Generate a summary of the text based on entities relationship and make it brief and concise
    Entities: {entities}
    Entity Relationships:{entity_text_relationship}
    
    Summary:
    """
    client = get_azure_llm_client()
    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    summary= response.choices[0].message.content.strip()
    return summary





