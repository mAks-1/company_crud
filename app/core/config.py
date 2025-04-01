from pydantic import BaseModel, PostgresDsn
from pydantic.v1 import BaseSettings


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DBConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 20


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
