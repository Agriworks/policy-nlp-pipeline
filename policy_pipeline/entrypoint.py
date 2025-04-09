from dataclasses import dataclass
from multiprocessing import process
from pathlib import Path
import re
from typing import List
from wsgiref import validate

import pandas
from tqdm import tqdm
from policy_pipeline.parameters import DEFAULT_OUTPUT_DIR
from policy_pipeline.pdf_extraction import extract_text
from policy_pipeline.summarization_pipeline import generate_ner, generate_summary
from policy_pipeline.utils import validate_model_with_displacy
from PyPDF2 import PdfReader
from typing import Optional




@dataclass
class SummarizationPipelineResults():
    chunk_text: str
    chunk_number: int
    relationship_summary: str
    summary: str
    # TODO: Add the result fields @praneeth
    classification_label:Optional[str]= None
    confidence_Score: Optional[float] = None



def run_summarization_pipeline():

    output_dir: Path = DEFAULT_OUTPUT_DIR
    # Create the output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True)


    # Step 1 - Extract text from PDF files into paragraphs chunks
    reader = PdfReader("./DFI_Volume_14.pdf")

    chunks = []

    for page in reader.pages:

        raw_text = page.extract_text()
        split_text = raw_text.split("\n\n")
        for para in split_text:
            chunks.append(para.strip())


    print(f"Extracted {len(chunks)} chunks from the PDF.")
    # Dump the chunks to a file
    with open(output_dir / "chunks.txt", "w") as f:
        for chunk in chunks:
            f.write(chunk + "\n\n")


    overall_results = []

    # Step 2 - Process each chunk with pipeline functions
    for chunk in tqdm(chunks, desc="Processing Chunks", unit="chunk"):
        ner_result = generate_ner(chunk)

        summary = generate_summary(chunk, ner_result)
        result = SummarizationPipelineResults(
            chunk_text=chunk,
            chunk_number=chunks.index(chunk),
            relationship_summary=ner_result.entity_text_relationship,
            summary=summary,
            # TODO: @praneeth How do I pass the entity information here ?
            # classification_label=ner_result.raw_entities[0],
            # confidence_Score=ner_result.entity_text_relationship
        )
        
        overall_results.append(result)

    # Step 3 - Export results to Excel

    output_df = pandas.DataFrame([{
        "Text (chunks)": d.chunk_text,
        "NER Tags": ", ".join([f"{e[0]} ({e[1]})" for e in d.raw_entities]),
        "Relationships": d.entity_text_relationship,
        "Summary": d.summary
    } for d in overall_results])
    output_df.to_excel(output_dir / "output_agri_ner_analysis.xlsx", index=False, engine="openpyxl")
    print(f"Results exported to {output_dir / 'output_agri_ner_analysis.xlsx'}")
    


def run_policy_pipeline(
    # pdf_file_paths: List[Path], output_dir: Path = Path("./output")
):

    output_dir: Path = DEFAULT_OUTPUT_DIR
    # Create the output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Test the utils once:

    test_sentences = [
        "The government has increased funding allocations for small farmers to boost income stability.",
        "Efforts to improve habitat connectivity have enhanced species richness in rural landscapes.",
        "Ensuring food affordability and availability remains a priority for global nutrition security.",
        "Carbon sequestration in regenerative farming helps mitigate climate change effects.",
        "Soil fertility and nutrient balance are essential for sustainable farming.",
        "Irrigation efficiency plays a vital role in groundwater recharge and water conservation.",
        "Precision agriculture techniques use AI-powered irrigation for improved efficiency.",
        "Integrated pest management and agroforestry are key agroecological practices.",
        "Wage fairness and labor rights are crucial for rural employment in agriculture.",
        "Fair trade practices ensure that small farmers receive equitable prices.",
        "Farmer training programs improve knowledge transfer in agricultural communities.",
        "Infrastructure development in rural areas improves connectivity for farmers.",
        "Humane treatment of livestock ensures sustainable livestock management.",
        "Bioenergy and solar-powered irrigation reduce the carbon footprint of agriculture.",
        "Biological control of pests helps reduce dependence on chemical pesticides.",
        "Subsidy frameworks influence land reform policies and agricultural governance.",
        "Food labeling regulations and organic certification promote sustainable consumption."
    ]

    validate_model_with_displacy(test_sentences, model_path=Path("./model_cache/improved_agri_ner"), output_dir=output_dir)

    # validate_model_with_displacy(test_sentences, model_path=Path("./model_cache/Agri_ruler_model"))

    return


    for pdf_file_path in pdf_file_paths:
        print(f"Processing {pdf_file_path}")
        # Do something with the PDF file
        extracted_text = extract_text(pdf_file_path)
