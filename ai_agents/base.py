from abc import ABC, abstractmethod

from app.backend.core.logger import logger


class Agent(ABC):
    def __init__(self, name: str, expertise: str):
        self.name = name
        self.expertise = expertise
        logger.info(f"Initialized {self.expertise} agent: {self.name}")

    @abstractmethod
    async def process(self, input_data: dict) -> dict:
        pass

    async def communicate(self, message: dict) -> dict:
        logger.debug(f"{self.name} received communication: {message}")
        response = {"status": "received", "message": f"Message received by {self.name}"}
        logger.debug(f"{self.name} responding with: {response}")
        return response