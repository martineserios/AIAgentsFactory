from ai_agents.base import Agent
from app.backend.core.logger import logger


class SoftwareEngineerAgent(Agent):
    def __init__(self):
        super().__init__("Software Engineer", "software development")

    async def process(self, input_data: dict) -> dict:
        logger.info(f"Software Engineer processing: {input_data}")
        if "code_review" in input_data:
            result = {"result": "Code review completed. Suggestions: Improve error handling."}
        elif "architecture" in input_data:
            result = {"result": "Recommended architecture: Microservices with Docker."}
        else:
            result = {"result": "I can help with code reviews and architecture design."}
        logger.info(f"Software Engineer response: {result}")
        return result