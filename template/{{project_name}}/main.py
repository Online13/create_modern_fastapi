from src.config import settings
from src.infrastructure.database.database import Database
from src.presentation.app import App
from src.infrastructure.database.models import *


database = Database(database_url=settings.database_url)

app = App(database=database)
app.setup_api()