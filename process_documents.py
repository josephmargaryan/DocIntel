import os
from tqdm import tqdm
import pandas as pd
from src.pipelines.pipeline import DocumentProcessingPipeline
from src.agents.text_extraction_agent import TextExtractionAgent
from src.agents.regex_agent import RegexAgent
from src.agents.qa_agent import QuestionAnsweringAgent
from src.agents.summarization_agent import SummarizationAgent
from src.agents.ner_agent import NERAgent
from src.agents.table_extraction_agent import TableExtractionAgent
from src.agents.formula_extraction_agent import (
    FormulaExtractionAgent,
) 
from src.document import Document
from src.utils.logging import Logger


def process_documents(
    input_dir: str,
    output_dir: str = "output_results",
    use_text: bool = True,
    use_summarization: bool = True,
    use_qa: bool = True,
    use_regex: bool = True,
    use_ner: bool = True,
    use_table: bool = True,
    use_formula_extraction: bool = True,  # New parameter
    concatenate_text: bool = False,  # New parameter for concatenation
    question: str = "What is the main topic of the document?",
    regex_pattern: str = r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",  # Example pattern for names
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
    - use_formula_extraction (bool): Whether to extract formulas and LaTeX code.
    - concatenate_text (bool): Whether to concatenate all extracted text into one file.
    - question (str): Question to ask in question answering.
    - regex_pattern (str): Regex pattern to search for.

    Returns:
    None
    """

    # Initialize logger
    logger = Logger(name="DocumentProcessorLogger")

    # Initialize the processing pipeline
    pipeline = DocumentProcessingPipeline()

    # Output directory
    os.makedirs(output_dir, exist_ok=True)

    # Supported file extensions
    supported_extensions = (".pdf", ".docx", ".png", ".jpg", ".jpeg", ".xlsx")

    # Get a list of all files in the input directory
    files = [
        f for f in os.listdir(input_dir) if f.lower().endswith(supported_extensions)
    ]

    if not files:
        logger.info("No supported files found in the input directory.")
        print("No supported files found in the input directory.")
        return

    # Initialize agents based on user input
    agents = {}
    if use_text:
        agents["text_agent"] = TextExtractionAgent(logger=logger)
    if use_summarization:
        agents["summarization_agent"] = SummarizationAgent(
            model_name="facebook/bart-large-cnn"
        )
    if use_qa:
        agents["qa_agent"] = QuestionAnsweringAgent(
            model_name="deepset/roberta-base-squad2"
        )
    if use_regex:
        agents["regex_agent"] = RegexAgent(pattern=regex_pattern)
    if use_ner:
        agents["ner_agent"] = NERAgent()
    if use_table:
        agents["table_agent"] = TableExtractionAgent(logger=logger)
    if use_formula_extraction:
        agents["formula_agent"] = FormulaExtractionAgent(logger=logger)

    # Store extracted texts for concatenation
    all_extracted_texts = []

    # Process each file with tqdm progress bar
    for file_name in tqdm(files, desc="Processing documents"):
        try:
            file_path = os.path.join(input_dir, file_name)
            logger.info(f"Processing document: {file_name}")

            # Process the document
            document = pipeline.process(file_path)
            logger.info("Document processed successfully.")

            # Create a subfolder in output_results for this document
            folder_name = os.path.splitext(file_name)[0]
            folder_name = "".join(
                c for c in folder_name if c.isalnum() or c in (" ", "_", "-")
            ).rstrip()
            document_output_dir = os.path.join(output_dir, folder_name)
            os.makedirs(document_output_dir, exist_ok=True)

            # Extract text (for non-Excel documents)
            if use_text:
                extracted_text = agents["text_agent"].execute(document)
                logger.info("Text extracted.")

                # Save extracted text to a file
                text_file_path = os.path.join(document_output_dir, "extracted_text.txt")
                with open(text_file_path, "w", encoding="utf-8") as f:
                    f.write(extracted_text)
                logger.info(f"Extracted text saved to {text_file_path}")

                # Collect extracted text for concatenation
                if concatenate_text:
                    all_extracted_texts.append(extracted_text)

        except Exception as e:
            logger.info(f"An error occurred while processing {file_name}: {e}")
            print(f"An error occurred while processing {file_name}: {e}")

    # Concatenate all extracted texts into one file
    if concatenate_text and all_extracted_texts:
        concatenated_file_path = os.path.join(output_dir, "concatenated_text.txt")
        with open(concatenated_file_path, "w", encoding="utf-8") as f:
            for text in all_extracted_texts:
                f.write(text + "\n\n")  # Add new lines between documents
        logger.info(
            f"All extracted texts concatenated and saved to {concatenated_file_path}"
        )

    print("All documents processed. Results are saved in the output directory.")


if __name__ == "__main__":
    process_documents(
        input_dir="input_documents",
        output_dir="output_results",
        use_text=True,
        use_summarization=False,
        use_qa=False,
        use_regex=False,
        use_ner=False,
        use_table=False,
        use_formula_extraction=False,  # Enable formula extraction
        concatenate_text=True,  # Concatenate all extracted texts
        question="What is the main topic of the document?",
        regex_pattern=r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    )
