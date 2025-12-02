NLP Microservice — /ai-services/nlp-service
```


nlp-service/
├── app.py                          # FastAPI app
├── requirements.txt
├── Dockerfile
├── README.md
│
├── model/
│   ├── tokenizer.json
│   └── nlp_model.pkl               # Saved NER model
│
├── utils/
│   ├── preprocess.py               # Text cleanup before NER
│   ├── entity_extraction.py        # NER + regex hybrid extraction
│   └── response_formatter.py
│
├── routes/
│   └── detect.py                   # /predict endpoint
│
└── tests/
    ├── sample_texts.txt
    └── test_entities.py
```

OCR Microservice — /ai-services/ocr-service
```
ocr-service/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
│
├── utils/
│   ├── ocr_engine.py               # Tesseract or Google Vision
│   ├── text_cleaner.py
│   ├── detect_pii.py               # Post-OCR regex check
│   └── response_formatter.py
│
├── routes/
│   └── ocr.py                      # /ocr endpoint
│
└── tests/
    └── test_images/
        ├── id_sample.jpg
        └── text_doc.png



```




