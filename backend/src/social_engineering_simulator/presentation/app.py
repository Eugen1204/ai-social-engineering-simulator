from fastapi import FastAPI
from social_engineering_simulator.presentation.api.health import router as health_router
from social_engineering_simulator.presentation.api.v1.excrption_handlers import register_exception_handlers
from social_engineering_simulator.presentation.api.v1.routers.organization import router as organization_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Social Engineering Simulator API",
        version="0.1.0"
    )
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(organization_router)
    return app
