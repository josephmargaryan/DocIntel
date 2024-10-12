# src/agents/ner_agent.py

from transformers import pipeline
from .base_agent import BaseAgent

class NERAgent(BaseAgent):
    def __init__(self, model_name='dslim/bert-base-NER'):
        self.ner_pipeline = pipeline("ner", model=model_name, grouped_entities=True)

    def execute(self, document):
        text = document.get_text()
        entities = self.ner_pipeline(text)
        person_names = [entity['word'] for entity in entities if entity['entity_group'] == 'PER']
        return person_names
