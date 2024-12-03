from dataclasses import dataclass, field
from functools import cached_property
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE: Final[str] = ".env"


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore", env_prefix="DB_")

    user: str = "postgres"
    password: str = "postgres"
    host: str = "127.0.0.1"
    port: int = 5432
    name: str = "postgres"

    @cached_property
    def uri(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
        )


class KafkaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore", env_prefix="KAFKA_")

    host: str = "127.0.0.1"
    port: int = 29092
    log_topic: str = "log"
    log_batch_size: int = 50
    log_seconds_interval: int = 10

    @cached_property
    def uri(self) -> str:
        return f"{self.host}:{self.port}"


@dataclass
class MainConfig:
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    kafka: KafkaConfig = field(default_factory=KafkaConfig)


main_config: Final[MainConfig] = MainConfig()
