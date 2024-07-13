from typing import Any, Dict, List

from pydantic import BaseModel


class ProcessRequest(BaseModel):
    query: str

class DiscussionRequest(BaseModel):
    topic: str

class KnowledgeUpdateRequest(BaseModel):
    content: str
    metadata: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    agent_name: str
    response: str

class ProcessResponse(BaseModel):
    query: str
    rag_response: Dict[str, Any]
    agent_responses: List[AgentResponse]

class DiscussionResponse(BaseModel):
    topic: str
    rag_context: Dict[str, Any]
    discussion: List[AgentResponse]

class KnowledgeUpdateResponse(BaseModel):
    status: str
    message: str