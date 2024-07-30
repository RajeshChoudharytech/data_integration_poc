
from fastapi import FastAPI
from app.config.logging import setup_logging

from app.api.router import api_router
from app.config.base import settings
from app.config.db import create_start_app_handler, create_stop_app_handler


def include_router(application):
    application.include_router(api_router, prefix=settings.API_PREFIX)


def include_event_handlers(application):
    application.add_event_handler(
        "startup", create_start_app_handler(application))
    application.add_event_handler(
        "shutdown", create_stop_app_handler(application))
    

def get_application() -> FastAPI:
    """
        Initiates the FastAPI application by including all the required handlers.
        Includes
            - Middleware
            - Exception Handlers
            - Router
            - Event Handlers
                In the event handlers we are connecting to the redis DB.
    :return:
        application(FastAPI)
    """
    application = FastAPI(title=settings.PROJECT_NAME,
                          debug=settings.DEBUG,
                          )
    setup_logging()
    include_router(application)
    include_event_handlers(application)
    return application

app = get_application()

@app.get("/health-check")
async def health_check():
    return {'health-check': "success"}

