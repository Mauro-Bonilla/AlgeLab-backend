from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Base settings for the application

    This settings are used to configure all the aplication.
    Enviroment specific settings will override this settings.
    """

    # Project Settings metadata
    PROJECT_NAME: str = "AlgeLab FastAPI"
    PROJECT_DESCRIPTION: str = (
        "An open source project for learning linear algebra through multimedia learning."
    )
    PROJECT_VERSION: str = "0.1.0"

    # Debug mode
    DEBUG: bool = False

    API_PREFIX: str = "/api"

    # Database URL

    database_url: str

    class Config:
        env_file = ".env"
