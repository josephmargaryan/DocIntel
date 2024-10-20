# src/agents/qa_agent.py

from transformers import pipeline
from .base_agent import BaseAgent


class QuestionAnsweringAgent(BaseAgent):
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        self.qa_pipeline = pipeline(
            "question-answering", model=model_name, tokenizer=model_name
        )

    def execute(self, document, question: str):
        context = document.get_text()
        # Ensure context is within model's max length
        max_context_length = 512  # Adjust based on the model
        if len(context.split()) > max_context_length:
            context = " ".join(context.split()[:max_context_length])
        result = self.qa_pipeline(question=question, context=context)
        return result["answer"]
