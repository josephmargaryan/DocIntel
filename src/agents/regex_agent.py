# src/agents/regex_agent.py

import re
from .base_agent import BaseAgent

class RegexAgent(BaseAgent):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def execute(self, document):
        text = document.get_text()
        matches = re.findall(self.pattern, text)
        return matches
