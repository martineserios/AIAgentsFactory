from fastapi import FastAPI

from ai_agents.expert_agents.software_engineer import SoftwareEngineerAgent
from ai_agents.knowledge_base import KnowledgeBase
from ai_agents.orchestrator import Orchestrator
from ai_agents.rag import RAG
from app.backend.api.routes import router
from app.backend.core.logger import logger

app = FastAPI(title="AI Crew API")

# Initialize components
knowledge_base = KnowledgeBase()
rag = RAG(knowledge_base)
software_engineer = SoftwareEngineerAgent()
orchestrator = Orchestrator([software_engineer], rag)

# Include routers
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the FastAPI application")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the FastAPI application")