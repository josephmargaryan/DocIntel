# Document Intelligence Pipeline

This project implements a Document Intelligence Pipeline capable of extracting text from documents, summarizing them, performing question-answering, named entity recognition (NER), and regex-based pattern matching. It leverages advanced NLP models from HuggingFace Transformers and spaCy to process and analyze text data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Test Script](#running-the-test-script)
- [Agents](#agents)
  - [TextExtractionAgent](#textextractionagent)
  - [SummarizationAgent](#summarizationagent)
  - [QuestionAnsweringAgent](#questionansweringagent)
  - [NERAgent](#neragent)
  - [RegexAgent](#regexagent)
- [Dependencies](#dependencies)
- [Notes](#notes)
- [License](#license)

## Features

- **Text Extraction**: Extracts text from PDF, DOCX, and image files.
- **Summarization**: Summarizes extracted text using state-of-the-art models.
- **Question Answering**: Answers questions based on the text or its summary.
- **Named Entity Recognition**: Extracts named entities, specifically person names.
- **Regex Matching**: Finds patterns in text using regular expressions.
- **Modular Design**: Easily extendable with additional agents and functionalities.


## Installation

### Prerequisites

- Python 3.8 or higher
- Git (to clone the repository)
- Virtual environment tool (optional but recommended)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/josephmargaryan/DocIntel.git
   cd DocIntel
   ```
2. **Download Spcay**
    ```bash
   python -m spacy download en_core_web_sm
   sudo apt-get install tesseract-ocr
   brew install tesseract
   ```
### Contact
joe.2010@live.dk


