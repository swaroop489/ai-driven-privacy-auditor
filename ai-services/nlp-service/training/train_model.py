"""
train_model.py
--------------
Trains a custom spaCy NER model for Indian PII detection using synthetic training data.

Process:
1. Loads base model (`en_core_web_sm`) to retain base English language features
2. Adds custom Indian PII entity labels
3. Generates training dataset from `training_data.py`
4. Fine-tunes the NER component using mini-batches and dropout to prevent overfitting
5. Saves model directly to `../model/custom_indian_pii/`
"""

import spacy
from spacy.training.example import Example
import random
import os
import warnings
from pathlib import Path
from training_data import generate_training_data

# Suppress typical spaCy training warnings
warnings.filterwarnings("ignore")

def train_ner_model(
    model_name: str = "en_core_web_sm",
    output_dir: str = "../model/custom_indian_pii",
    iterations: int = 15
):
    """
    Fine-tunes the spaCy NER model with custom Indian PII entities.
    """
    print(f"Step 1: Loading base model '{model_name}'...")
    try:
        nlp = spacy.load(model_name)
    except OSError:
        print(f"Base model '{model_name}' not found. Downloading...")
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)

    # Check if NER pipeline exists, if not create it
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    print("Step 2: Generating synthetic training dataset...")
    # Generate a large dataset for training. ~20 examples * 10 types + multi + negatives
    TRAIN_DATA = generate_training_data(examples_per_type=20, include_negatives=True, include_multi=True, seed=42)
    print(f"Generated {len(TRAIN_DATA)} annotated examples.")

    print("Step 3: Adding custom entity labels to NER pipeline...")
    # Add our new labels so they aren't ignored
    for text, annotations in TRAIN_DATA:
        for ent in annotations.get("entities", []):
            ner.add_label(ent[2])

    print("Step 4: Preparing for fine-tuning...")
    # Disable other pipelines (like parser, tagger) to only train NER
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    # ONLY training NER
    with nlp.disable_pipes(*unaffected_pipes):
        
        # Resume training (create optimizer for the existing weights)
        optimizer = nlp.resume_training()
        
        # Batch size strategy
        batch_sizes = spacy.util.compounding(4.0, 32.0, 1.001)

        print(f"Step 5: Training loop started ({iterations} iterations)...")
        for itn in range(iterations):
            random.shuffle(TRAIN_DATA)
            losses = {}

            # Create batches
            batches = spacy.util.minibatch(TRAIN_DATA, size=batch_sizes)

            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    try:
                        example = Example.from_dict(doc, annotations)
                        examples.append(example)
                    except ValueError as e:
                        # Exception can occur if entity boundaries aren't aligned to spaCy tokens
                        # We skip malformed examples gracefully
                        continue
                
                if examples:
                    # Update model
                    nlp.update(
                        examples,
                        drop=0.35,      # Dropout rate to prevent overfitting
                        sgd=optimizer,  # Ensure optimizer is passed
                        losses=losses
                    )
            
            print(f"  Iteration {itn + 1:02d}/{iterations}  -> Loss: {losses.get('ner', 0.0):.2f}")

    print("\nStep 6: Saving model...")
    # Ensure output directory exists
    output_path = Path(output_dir)
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)
    
    nlp.to_disk(output_path)
    print(f"Success! Model saved to: {output_path.absolute()}")
    
    # Test the loaded model to verify it saved correctly
    print("\nQuick Verification:")
    print("--------------------")
    test_nlp = spacy.load(output_path)
    test_text = "My Aadhar number is 1234 5678 9012 and PAN is ABCDE1234F. Email rahul@gmail.com"
    print(f"Text: {test_text}")
    doc = test_nlp(test_text)
    for ent in doc.ents:
        print(f"Found: {ent.text} [{ent.label_}]")

if __name__ == "__main__":
    print("=" * 50)
    print("CUSTOM INDIAN PII - NER MODEL TRAINING")
    print("=" * 50)
    train_ner_model()
