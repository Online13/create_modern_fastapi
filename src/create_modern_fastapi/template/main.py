from src.infrastructure.env.env import Settings, setup_settings
from src.infrastructure.persistence.database.database import setup_database
from src.presentation.app import create_app

settings = Settings()  # type: ignore
setup_settings(settings)

database_url = settings.get_database_url()
setup_database(database_url)

app = create_app()
