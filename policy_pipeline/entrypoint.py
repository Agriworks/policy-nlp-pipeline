from pathlib import Path
from typing import List
from wsgiref import validate
from policy_pipeline.pdf_extraction import extract_text
from policy_pipeline.utils import validate_model_with_displacy


def run_policy_pipeline(
    # pdf_file_paths: List[Path], output_dir: Path = Path("./output")
):

    output_dir: Path = Path("./output")
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
