from typing import Dict, List

from ai_agents.base import Agent
from ai_agents.rag import RAG
from app.backend.core.logger import logger


class Orchestrator:
    def __init__(self, agents: List[Agent], rag: RAG):
        self.agents = agents
        self.rag = rag
        logger.info(f"Orchestrator initialized with {len(agents)} agents and RAG system")

    async def process_request(self, request: Dict) -> Dict:
        logger.info(f"Processing request: {request}")
        
        # First, use RAG to retrieve relevant information
        rag_response = await self.rag.process(request.get('query', ''))
        
        # Then, pass the augmented information to the agents
        results = {}
        for agent in self.agents:
            logger.debug(f"Delegating to agent: {agent.name}")
            augmented_request = {**request, 'rag_info': rag_response}
            agent_result = await agent.process(augmented_request)
            results[agent.expertise] = agent_result
        
        aggregated_result = {
            "rag_response": rag_response,
            "agent_responses": results
        }
        logger.info(f"Aggregated result: {aggregated_result}")
        return aggregated_result

    async def facilitate_discussion(self, topic: str) -> Dict:
        logger.info(f"Facilitating discussion on topic: {topic}")
        
        # Use RAG to provide context for the discussion
        rag_context = await self.rag.process(topic)
        
        discussion = []
        for agent in self.agents:
            logger.debug(f"Getting input from agent: {agent.name}")
            response = await agent.communicate({"topic": topic, "context": rag_context})
            discussion.append({agent.name: response})
        
        result = {"rag_context": rag_context, "discussion": discussion}
        logger.info(f"Discussion result: {result}")
        return result

    async def update_knowledge(self, new_info: Dict) -> Dict:
        return await self.rag.update_knowledge(new_info)