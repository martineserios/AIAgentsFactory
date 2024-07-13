from fastapi import FastAPI

from app.backend.api.routes import router
from app.backend.core.config import settings
from app.backend.core.logger import logger
from app.backend.services.ai_agents.expert_agents.software_engineer import \
    SoftwareEngineerAgent
from app.backend.services.ai_agents.knowledge_base import KnowledgeBase
from app.backend.services.ai_agents.orchestrator import Orchestrator
from app.backend.services.ai_agents.rag import RAG

app = FastAPI(title= f"{settings.APP_NAME} API")

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