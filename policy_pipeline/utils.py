from pathlib import Path
from typing import List
import spacy
from spacy import displacy

def validate_model_with_displacy(test_sentences: List[str], model_path: Path, output_dir: Path) -> None:
    """Tests the trained NER model on a list of sentences with Displacy visualization.

    Args:
        test_sentences (List[str]): List of sentences to test the model on.
        model_path (Path, optional): Path of the model . Defaults to Path("/content/drive/MyDrive/improved_agri_ner").
    """
    nlp = spacy.load(model_path)

    for sentence in test_sentences:
        doc = nlp(sentence)
        print("\nTest Sentence:", sentence)
        print("Extracted Entities:")
        for ent in doc.ents:
            print(f"{ent.text} --> {ent.label_}")
        print("-" * 50)
        # Visualize with Displacy
        html = displacy.render(doc, style="ent", page=True) # 

        # Save the visualization to a file
        output_file = output_dir / f"{sentence[:10]}_displacy.html"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html)
    return
