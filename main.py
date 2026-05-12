from fastapi import FastAPI
import router, models
import dashboard_router
from database import engine
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ClassicModels REST API",
    description="A REST API for managing the ClassicModels database",
    version="1.0.0"
)

models.Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app.include_router(dashboard_router.router) # Include the dashboard router first to ensure its endpoints are registered before the customers router
app.include_router(router.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)