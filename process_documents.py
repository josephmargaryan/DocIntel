# process_documents.py

import os
from tqdm import tqdm
from src.pipelines.pipeline import DocumentProcessingPipeline
from src.agents.text_extraction_agent import TextExtractionAgent
from src.agents.regex_agent import RegexAgent
from src.agents.qa_agent import QuestionAnsweringAgent
from src.agents.summarization_agent import SummarizationAgent
from src.agents.ner_agent import NERAgent
from src.agents.table_extraction_agent import TableExtractionAgent
from src.document import Document
from src.utils.logging import Logger

def process_documents(
    input_dir: str,
    output_dir: str = 'output_results',
    use_text: bool = True,
    use_summarization: bool = True,
    use_qa: bool = True,
    use_regex: bool = True,
    use_ner: bool = True,
    use_table: bool = True,
    question: str = "What is the main topic of the document?",
    regex_pattern: str = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'  # Example pattern for names
):
    """
    Process documents in the input directory using specified agents.

    Parameters:
    - input_dir (str): Directory containing input documents.
    - output_dir (str): Directory to save output results.
    - use_text (bool): Whether to extract text.
    - use_summarization (bool): Whether to perform summarization.
    - use_qa (bool): Whether to perform question answering.
    - use_regex (bool): Whether to perform regex search.
    - use_ner (bool): Whether to perform named entity recognition.
    - use_table (bool): Whether to extract tables from PDFs.
    - question (str): Question to ask in question answering.
    - regex_pattern (str): Regex pattern to search for.

    Returns:
    None
    """

    # Initialize logger
    logger = Logger(name='DocumentProcessorLogger')

    # Initialize the processing pipeline
    pipeline = DocumentProcessingPipeline()

    # Output directory
    os.makedirs(output_dir, exist_ok=True)

    # Supported file extensions
    supported_extensions = ('.pdf', '.docx', '.png', '.jpg', '.jpeg')

    # Get a list of all files in the input directory
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)]

    if not files:
        logger.info('No supported files found in the input directory.')
        print('No supported files found in the input directory.')
        return

    # Initialize agents based on user input
    agents = {}
    if use_text:
        agents['text_agent'] = TextExtractionAgent(logger=logger)
    if use_summarization:
        agents['summarization_agent'] = SummarizationAgent(model_name='facebook/bart-large-cnn')
    if use_qa:
        agents['qa_agent'] = QuestionAnsweringAgent(model_name='deepset/roberta-base-squad2')
    if use_regex:
        agents['regex_agent'] = RegexAgent(pattern=regex_pattern)
    if use_ner:
        agents['ner_agent'] = NERAgent()
    if use_table:
        agents['table_agent'] = TableExtractionAgent(logger=logger)

    # Process each file with tqdm progress bar
    for file_name in tqdm(files, desc='Processing documents'):
        try:
            file_path = os.path.join(input_dir, file_name)
            logger.info(f'Processing document: {file_name}')

            # Process the document
            document = pipeline.process(file_path)
            logger.info('Document processed successfully.')

            # Create a subfolder in output_results for this document
            # Sanitize the file name to create a valid folder name
            folder_name = os.path.splitext(file_name)[0]
            folder_name = ''.join(c for c in folder_name if c.isalnum() or c in (' ', '_', '-')).rstrip()
            document_output_dir = os.path.join(output_dir, folder_name)
            os.makedirs(document_output_dir, exist_ok=True)

            # Extract text
            if use_text:
                extracted_text = agents['text_agent'].execute(document)
                logger.info('Text extracted.')

                # Save extracted text to a file
                text_file_path = os.path.join(document_output_dir, 'extracted_text.txt')
                with open(text_file_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                logger.info(f'Extracted text saved to {text_file_path}')
            else:
                extracted_text = None

            # Summarize text
            if use_summarization and extracted_text:
                summary = agents['summarization_agent'].execute(document)
                logger.info('Text summarized.')

                # Save summary to a file
                summary_file_path = os.path.join(document_output_dir, 'summary.txt')
                with open(summary_file_path, 'w', encoding='utf-8') as f:
                    f.write(summary)
                logger.info(f'Summary saved to {summary_file_path}')
            else:
                summary = None

            # Perform question answering
            if use_qa and summary:
                temp_doc = Document(summary)
                answer = agents['qa_agent'].execute(temp_doc, question)
                logger.info('Question Answering executed.')

                # Save QA result to a file
                qa_file_path = os.path.join(document_output_dir, 'qa_result.txt')
                with open(qa_file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Question: {question}\nAnswer: {answer}")
                logger.info(f'QA result saved to {qa_file_path}')

            # Extract tables (only for PDFs)
            if use_table and file_path.lower().endswith('.pdf'):
                tables = agents['table_agent'].execute(document)
                logger.info(f'Tables extracted: {len(tables)}')

                # Save extracted tables to files
                for table_info in tables:
                    page_number = table_info['page']
                    table_number = table_info['table_number']
                    table_data = table_info['data']
                    table_file_path = os.path.join(document_output_dir, f'table_page{page_number}_table{table_number}.csv')

                    # Save table data as CSV
                    import csv
                    with open(table_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        for row in table_data:
                            writer.writerow(row)
                    logger.info(f'Table saved to {table_file_path}')
            elif use_table:
                logger.info('No tables extracted (not a PDF file).')

            # Perform regex search
            if use_regex and extracted_text:
                matches = agents['regex_agent'].execute(document)
                logger.info('Regex search executed.')

                # Save regex matches to a file
                regex_file_path = os.path.join(document_output_dir, 'regex_matches.txt')
                with open(regex_file_path, 'w', encoding='utf-8') as f:
                    for match in matches:
                        f.write(match + '\n')
                logger.info(f'Regex matches saved to {regex_file_path}')

            # Perform Named Entity Recognition
            if use_ner and extracted_text:
                person_names = agents['ner_agent'].execute(document)
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

    print("All documents processed. Results are saved in the output directory.")

# Example usage:
if __name__ == '__main__':
    process_documents(
        input_dir='input_documents',
        output_dir='output_results',
        use_text=True,
        use_summarization=True,
        use_qa=True,
        use_regex=True,
        use_ner=True,
        use_table=True,
        question="What is the main topic of the document?",
        regex_pattern=r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    )
