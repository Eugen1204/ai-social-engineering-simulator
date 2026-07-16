from fastapi import FastAPI
from social_engineering_simulator.presentation.api.health import router as health_router



def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Social Engineering Simulator API",
        version="0.1.0"
    )
    app.include_router(health_router)
    return app
