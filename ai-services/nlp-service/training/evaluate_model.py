"""
evaluate_model.py
-----------------
Evaluates the custom-trained Indian PII NER model against testing data.
Calculates Precision, Recall, and F1-score per entity type.
"""

import spacy
from spacy.scorer import Scorer
from spacy.training import Example
from training_data import generate_training_data
import os
import json

def evaluate(model_path: str, test_data: list):
    """
    Evaluate precision, recall, and F1 score for the given NER model and test data.
    """
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}. Please train it first.")
        return None

    print(f"Loading model from {model_path}...")
    nlp = spacy.load(model_path)
    
    print(f"Evaluating on {len(test_data)} test examples...")

    examples = []
    for text, ann in test_data:
        # Create a document from the text
        doc = nlp.make_doc(text)
        # Create a spaCy Example object which aligns the predicted doc with the gold standard
        example = Example.from_dict(doc, ann)
        examples.append(example)

    # Use Scorer to compute metrics
    scorer = Scorer()
    scores = nlp.evaluate(examples)

    # Extract relevant metrics
    results = {
        "overall": {
            "precision": scores.get("ents_p", 0.0),
            "recall": scores.get("ents_r", 0.0),
            "f1": scores.get("ents_f", 0.0)
        },
        "per_entity": scores.get("ents_per_type", {})
    }

    return results

def print_evaluation_report(results: dict):
    if not results:
        return

    print("\n" + "="*50)
    print("MODEL EVALUATION REPORT")
    print("="*50)

    print("\nOVERALL METRICS:")
    print(f"  Precision: {results['overall']['precision']:.4f}")
    print(f"  Recall:    {results['overall']['recall']:.4f}")
    print(f"  F1-Score:  {results['overall']['f1']:.4f}")

    print("\nPER-ENTITY METRICS:")
    print(f"  {'Entity Type':<15} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10}")
    print("  " + "-"*55)
    
    for entity, metrics in sorted(results["per_entity"].items()):
        p = metrics.get('p', 0.0)
        r = metrics.get('r', 0.0)
        f = metrics.get('f', 0.0)
        print(f"  {entity:<15} | {p:<10.4f} | {r:<10.4f} | {f:<10.4f}")
        
    print("="*50 + "\n")

if __name__ == "__main__":
    # Generate fresh "unseen" test data using a different seed
    print("Generating unseen test dataset for evaluation...")
    test_data = generate_training_data(examples_per_type=5, include_negatives=True, include_multi=True, seed=999)
    
    model_path = "../model/custom_indian_pii"
    
    results = evaluate(model_path, test_data)
    
    if results:
        print_evaluation_report(results)
        
        # Save report
        report_path = "evaluation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Saved detailed metrics to {report_path}")
