from fastapi import FastAPI
from social_engineering_simulator.presentation.api.v1.health import router as health_router



def create_app() -> FastAPI:
    app = FastAPI(
        title="social_engineering_simulator",
        version="1.0.0"
    )
    app.include_router(health_router)
    return app
