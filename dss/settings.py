from pydantic import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    allowed_origins: list[str]
    database_name: str
    database_user: str
    database_password: str
    database_host: str
    database_port: int
    database_driver: str

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.database_driver,
            username=self.database_user,
            password=self.database_password,
            database=self.database_name,
            host=self.database_host,
            port=self.database_port,
        )


settings = Settings()
