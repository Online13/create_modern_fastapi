from typing import Annotated
from fastapi import Depends
from src.container import Container
from src.infrastructure.env.env import Settings

def build_env_config():
	settings = Container.get_settings()
	return settings

EnvConfig = Annotated[Settings, Depends(build_env_config)]
