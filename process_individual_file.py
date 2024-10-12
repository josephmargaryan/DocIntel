# test.py

import os
from src.pipelines.pipeline import DocumentProcessingPipeline
from src.agents.text_extraction_agent import TextExtractionAgent
from src.agents.qa_agent import QuestionAnsweringAgent
from src.agents.regex_agent import RegexAgent
from src.agents.summarization_agent import SummarizationAgent
from src.agents.ner_agent import NERAgent
from src.document import Document
from src.utils.logging import Logger

# Initialize logger
logger = Logger(name='TestLogger')

# Initialize the processing pipeline
pipeline = DocumentProcessingPipeline()

# Path to your PDF document
pdf_path = 'profileHMM.pdf'

# Output directory
output_dir = 'output_results'
os.makedirs(output_dir, exist_ok=True)

# Process the document
try:
    document = pipeline.process(pdf_path)
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

    # Save extracted text to a file
    text_file_path = os.path.join(output_dir, 'extracted_text.txt')
    with open(text_file_path, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    logger.info(f'Extracted text saved to {text_file_path}')

    # Summarize text
    summary = summarization_agent.execute(document)
    logger.info('Text summarized.')

    # Save summary to a file
    summary_file_path = os.path.join(output_dir, 'summary.txt')
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    logger.info(f'Summary saved to {summary_file_path}')

    # Perform question answering using the summary
    question = "What is the main topic of the document?"
    temp_doc = Document(summary)
    answer = qa_agent.execute(temp_doc, question)
    logger.info('Question Answering executed.')

    # Save QA result to a file
    qa_file_path = os.path.join(output_dir, 'qa_result.txt')
    with open(qa_file_path, 'w', encoding='utf-8') as f:
        f.write(f"Question: {question}\nAnswer: {answer}")
    logger.info(f'QA result saved to {qa_file_path}')

    # Perform regex search
    matches = regex_agent.execute(document)
    logger.info('Regex search executed.')

    # Save regex matches to a file
    regex_file_path = os.path.join(output_dir, 'regex_matches.txt')
    with open(regex_file_path, 'w', encoding='utf-8') as f:
        for match in matches:
            f.write(match + '\n')
    logger.info(f'Regex matches saved to {regex_file_path}')

    # Perform Named Entity Recognition
    person_names = ner_agent.execute(document)
    logger.info('Named Entity Recognition executed.')

    # Save person names to a file
    ner_file_path = os.path.join(output_dir, 'person_names.txt')
    with open(ner_file_path, 'w', encoding='utf-8') as f:
        for name in person_names:
            f.write(name + '\n')
    logger.info(f'Person names saved to {ner_file_path}')

    print("All agents executed successfully. Results are saved in the 'output_results' folder.")

except Exception as e:
    logger.info(f'An error occurred: {e}')
    print(f'An error occurred: {e}')