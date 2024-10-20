# src/agents/base_agent.py

import abc
from ..document import Document


class BaseAgent(abc.ABC):
    @abc.abstractmethod
    def execute(self, document: Document):
        pass
