from typing import Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Replace with your actual settings import
from .base import settings

# Global variable to hold the database engine
_engine = None
SessionLocal = None

# Function to initialize the database connection and create tables
async def init_database_connection(app: FastAPI) -> None:
    """
    Initializes the database connection and creates tables.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        None
    """
    global _engine, SessionLocal

    # Create the database engine with the specified settings
    _engine = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        echo=True,  # Optional: Enable logging of SQL queries
        future=True,  # Optional: Use the latest SQLAlchemy features
    )

    # Create a configured "Session" class
    SessionLocal = sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Store the engine in the FastAPI app state for later use
    app.state._db = _engine

    # Create all tables defined in the SQLModel metadata
    async with _engine.begin() as conn:
        # Run the synchronous SQLModel.metadata.create_all function using the
        # asynchronous connection
        await conn.run_sync(SQLModel.metadata.create_all)

# Function to create a startup handler for the FastAPI app


def create_start_app_handler(app: FastAPI) -> Callable:
    """
    Creates a startup handler for the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        Callable: The startup handler function.
    """

    async def start_app() -> None:
        """
        Initializes the database connection and creates tables at startup.

        Args:
            None

        Returns:
            None
        """

        # Initialize the database connection
        await init_database_connection(app)

    return start_app

# Function to create a shutdown handler for the FastAPI app
def create_stop_app_handler(app: FastAPI) -> Callable:
    """
    Creates a shutdown handler for the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.

    Returns:
        Callable: The shutdown handler function.
    """

    async def stop_app() -> None:
        """
        Disposes of the database connection at shutdown.

        Args:
            None

        Returns:
            None
        """

        # Check if the database connection exists
        if app.state._db:
            # Dispose of the database connection
            await app.state._db.dispose()

    return stop_app

# Dependency to get the database session
async def get_db():
    async with SessionLocal() as session:
        yield session
