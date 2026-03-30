"""Database initialization module."""
from sqlmodel import SQLModel, create_engine, Session
from src.config import settings
from src.logging_config import get_logger
from sqlalchemy import text


logger = get_logger(__name__)


def init_database() -> None:
    """
    Initialize database and create all tables.

    Creates a SQLAlchemy engine from the database URL in settings
    and creates all SQLModel tables.
    """
    try:
        # Create engine from database URL in settings
        engine = create_engine(
            settings.database_url,
            echo=settings.database_echo,
            future=True,
        )

        logger.info("database_engine_created", url=settings.database_url)

        # Create all tables defined in SQLModel models
        SQLModel.metadata.create_all(engine)
        logger.info("database_tables_created")

        # Test connection
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            logger.info("database_connection_verified")

    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))
        raise


def get_engine():
    """Get database engine instance."""
    return create_engine(
        settings.database_url,
        echo=settings.database_echo,
        future=True,
    )


def get_session():
    """Get database session for dependency injection."""
    engine = get_engine()
    with Session(engine) as session:
        yield session

