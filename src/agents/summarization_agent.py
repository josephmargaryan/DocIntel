# src/agents/summarization_agent.py

from transformers import pipeline
from .base_agent import BaseAgent


class SummarizationAgent(BaseAgent):
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline(
            "summarization", model=model_name, tokenizer=model_name
        )

    def execute(self, document, max_length=150, min_length=30):
        text = document.get_text()
        # Handle long texts by truncating if necessary
        max_input_length = 1024  # Model's maximum input length
        if len(text) > max_input_length:
            text = text[:max_input_length]
        summary = self.summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return summary[0]["summary_text"]
