from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_agents.orchestrator import Orchestrator
from app.backend.core.logger import logger

router = APIRouter()

# We'll declare these models here, but in a larger project, 
# you might want to move them to a separate models.py file
class ProcessRequest(BaseModel):
    query: str

class DiscussionRequest(BaseModel):
    topic: str

class KnowledgeUpdateRequest(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

@router.post("/process")
async def process_request(request: ProcessRequest):
    try:
        orchestrator: Orchestrator = router.app.state.orchestrator
        result = await orchestrator.process_request({"query": request.query})
        return result
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/discuss")
async def discuss_topic(request: DiscussionRequest):
    try:
        orchestrator: Orchestrator = router.app.state.orchestrator
        result = await orchestrator.facilitate_discussion(request.topic)
        return result
    except Exception as e:
        logger.error(f"Error facilitating discussion: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/update_knowledge")
async def update_knowledge(request: KnowledgeUpdateRequest):
    try:
        orchestrator: Orchestrator = router.app.state.orchestrator
        result = await orchestrator.update_knowledge({
            "content": request.content,
            "metadata": request.metadata
        })
        return result
    except Exception as e:
        logger.error(f"Error updating knowledge base: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")