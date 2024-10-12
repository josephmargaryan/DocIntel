# test.py

import os
import tqdm
from src.pipelines.pipeline import DocumentProcessingPipeline
from src.agents.text_extraction_agent import TextExtractionAgent
from src.agents.qa_agent import QuestionAnsweringAgent
from src.agents.regex_agent import RegexAgent
from src.agents.summarization_agent import SummarizationAgent
from src.agents.ner_agent import NERAgent
from src.document import Document
from src.utils.logging import Logger

# Initialize logger
logger = Logger(name='BatchProcessingLogger')

# Initialize the processing pipeline
pipeline = DocumentProcessingPipeline()

# Path to the directory containing your documents
input_dir = 'input_documents'  # Update this to your input directory

# Output directory
output_dir = 'output_results'
os.makedirs(output_dir, exist_ok=True)

# Supported file extensions
supported_extensions = ('.pdf', '.docx', '.png', '.jpg', '.jpeg')

# Get a list of all files in the input directory
files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)]

# Process each file
for file_name in tqdm(files, desc="processing files"):
    try:
        file_path = os.path.join(input_dir, file_name)
        logger.info(f'Processing document: {file_name}')

        # Process the document
        document = pipeline.process(file_path)
        logger.info('Document processed successfully.')

        # Initialize agents
        text_agent = TextExtractionAgent(logger=logger)
        qa_agent = QuestionAnsweringAgent(model_name='deepset/roberta-base-squad2')
        regex_agent = RegexAgent(pattern=r'\b[A-Z][a-z]+ [A-Z][a-z]+\b')  # Example pattern for names
        summarization_agent = SummarizationAgent(model_name='facebook/bart-large-cnn')
        ner_agent = NERAgent()

        # Extract text
        extracted_text = text_agent.execute(document)
        logger.info('Text extracted.')

        # Create a subfolder in output_results for this document
        # Sanitize the file name to create a valid folder name
        folder_name = os.path.splitext(file_name)[0]
        folder_name = ''.join(c for c in folder_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        document_output_dir = os.path.join(output_dir, folder_name)
        os.makedirs(document_output_dir, exist_ok=True)

        # Save extracted text to a file
        text_file_path = os.path.join(document_output_dir, 'extracted_text.txt')
        with open(text_file_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        logger.info(f'Extracted text saved to {text_file_path}')

        # Summarize text
        summary = summarization_agent.execute(document)
        logger.info('Text summarized.')

        # Save summary to a file
        summary_file_path = os.path.join(document_output_dir, 'summary.txt')
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        logger.info(f'Summary saved to {summary_file_path}')

        # Perform question answering using the summary
        question = "What is the main topic of the document?"
        temp_doc = Document(summary)
        answer = qa_agent.execute(temp_doc, question)
        logger.info('Question Answering executed.')

        # Save QA result to a file
        qa_file_path = os.path.join(document_output_dir, 'qa_result.txt')
        with open(qa_file_path, 'w', encoding='utf-8') as f:
            f.write(f"Question: {question}\nAnswer: {answer}")
        logger.info(f'QA result saved to {qa_file_path}')

        # Perform regex search
        matches = regex_agent.execute(document)
        logger.info('Regex search executed.')

        # Save regex matches to a file
        regex_file_path = os.path.join(document_output_dir, 'regex_matches.txt')
        with open(regex_file_path, 'w', encoding='utf-8') as f:
            for match in matches:
                f.write(match + '\n')
        logger.info(f'Regex matches saved to {regex_file_path}')

        # Perform Named Entity Recognition
        person_names = ner_agent.execute(document)
        logger.info('Named Entity Recognition executed.')

        # Save person names to a file
        ner_file_path = os.path.join(document_output_dir, 'person_names.txt')
        with open(ner_file_path, 'w', encoding='utf-8') as f:
            for name in person_names:
                f.write(name + '\n')
        logger.info(f'Person names saved to {ner_file_path}')

        logger.info(f'Processing of {file_name} completed successfully.')

    except Exception as e:
        logger.info(f'An error occurred while processing {file_name}: {e}')
        print(f'An error occurred while processing {file_name}: {e}')

print("All documents processed. Results are saved in the 'output_results' folder.")
