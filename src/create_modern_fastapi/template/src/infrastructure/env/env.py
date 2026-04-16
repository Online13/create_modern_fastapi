from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, SecretStr
from src.container import Container


class Settings(BaseSettings):
	# doc login
	login_docs_username: str = Field(min_length=3, default="admin")
	login_docs_password: SecretStr = Field(min_length=8)

	def get_login_docs_username(self) -> str:
		return self.login_docs_username

	def get_login_docs_password(self) -> str:
		return self.login_docs_password.get_secret_value()

	# database
	database_url: PostgresDsn
	database_test_url: PostgresDsn

	def get_database_url(self) -> str:
		return self.database_url.encoded_string()

	def get_database_test_url(self) -> str:
		return self.database_test_url.encoded_string()

	model_config = SettingsConfigDict(
		env_file=".env",
		extra="ignore",
	)


def setup_settings(settings: Settings):
	Container.set_settings(settings)
