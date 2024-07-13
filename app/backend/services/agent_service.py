from ai_agents.orchestrator import Orchestrator

from app.backend.core.logger import logger
from app.backend.models.pydantic_models import (DiscussionResponse,
                                                KnowledgeUpdateResponse,
                                                ProcessResponse)


class AgentService:
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator

    async def process_request(self, query: str) -> ProcessResponse:
        try:
            result = await self.orchestrator.process_request({"query": query})
            return ProcessResponse(
                query=query,
                rag_response=result["rag_response"],
                agent_responses=[
                    {"agent_name": k, "response": v}
                    for k, v in result["agent_responses"].items()
                ] # type: ignore
            )
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            raise

    async def facilitate_discussion(self, topic: str) -> DiscussionResponse:
        try:
            result = await self.orchestrator.facilitate_discussion(topic)
            return DiscussionResponse(
                topic=topic,
                rag_context=result["rag_context"],
                discussion=[
                    {"agent_name": list(item.keys())[0], "response": list(item.values())[0]}
                    for item in result["discussion"]
                ] # type: ignore
            )
        except Exception as e:
            logger.error(f"Error facilitating discussion: {str(e)}")
            raise

    async def update_knowledge(self, content: str, metadata: dict) -> KnowledgeUpdateResponse:
        try:
            result = await self.orchestrator.update_knowledge({
                "content": content,
                "metadata": metadata
            })
            return KnowledgeUpdateResponse(**result)
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
            raise