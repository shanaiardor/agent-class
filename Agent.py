from abc import ABC, abstractmethod
from typing import Optional

from Config import Config
from HelloAgentsLLM import HelloAgentsLLM
from Message import Message


class Agent(ABC):
    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history: list[Message] = []

    @abstractmethod
    def run(self, input_text: str, max_tool_iterations: int = 3, **kwargs) -> str:
        """ 运行 agent
        :param max_tool_iterations:
        """
        pass

    def add_message(self, message: Message):
        """ 添加消息到历史记录 """
        self._history.append(message)

    def clear_history(self):
        """ 清除历史记录 """
        self._history.clear()

    def get_history(self):
        """ 获取历史记录 """
        return self._history.copy()

    def __str__(self):
        return f"Agent(name={self.name}, provider={self.llm.provider})"
