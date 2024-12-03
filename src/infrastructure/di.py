from functools import lru_cache
from typing import Final

from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container
from dishka.integrations import fastapi as fastapi_dishka
from faststream.kafka import KafkaBroker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.application.protocols.log import ILogMessageReader, ILogMessageSaver
from src.application.protocols.tariff import ITariffReader, ITariffSaver
from src.application.protocols.transaction_context import ITransactionContext
from src.application.scenarios.calculate_insurence import CalculateInsuranse
from src.application.scenarios.tariff_service import TariffService
from src.config import DatabaseConfig, KafkaConfig, MainConfig, main_config
from src.infrastructure.persistence.database import (
    async_engine_factory,
    async_session_factory,
    async_sessionmaker_factory,
)
from src.infrastructure.kafka_logger.broker import kafka_broker_factory
from src.infrastructure.persistence.repositories.log import SqlalchemyLogMessageRepository
from src.infrastructure.persistence.repositories.tariff import SqlalchemyTariffRepository
from src.infrastructure.persistence.transaction_context import (
    SqlalchemyTransactionContext,
    transaction_context_factory,
)


def config_provider() -> Provider:
    provider = Provider(scope=Scope.APP)
    provider.provide(lambda: main_config.db, provides=DatabaseConfig)
    provider.provide(lambda: main_config.kafka, provides=KafkaConfig)

    return provider


def sqlalchemy_provider() -> Provider:
    provider = Provider()
    provider.provide(async_engine_factory, provides=AsyncEngine, scope=Scope.APP)
    provider.provide(
        async_sessionmaker_factory, provides=async_sessionmaker[AsyncSession], scope=Scope.APP
    )
    provider.provide(async_session_factory, provides=AsyncSession, scope=Scope.REQUEST)

    return provider


def persistence_provider() -> Provider:
    provider = Provider()
    provider.provide(
        transaction_context_factory,
        provides=AnyOf[ITransactionContext, SqlalchemyTransactionContext],
        scope=Scope.REQUEST,
    )
    provider.provide(
        SqlalchemyTariffRepository,
        provides=AnyOf[ITariffReader, ITariffSaver, SqlalchemyTariffRepository],
        scope=Scope.REQUEST,
    )
    provider.provide(
        SqlalchemyLogMessageRepository,
        provides=AnyOf[ILogMessageReader, ILogMessageSaver, SqlalchemyLogMessageRepository],
        scope=Scope.REQUEST,
    )

    return provider


def kafka_log_provider() -> Provider:
    provider = Provider()
    provider.provide(kafka_broker_factory, provides=KafkaBroker, scope=Scope.APP)

    return provider


def application_cases_provider() -> Provider:
    provider = Provider()
    provider.provide(TariffService, scope=Scope.REQUEST)
    provider.provide(CalculateInsuranse, scope=Scope.REQUEST)

    return provider


def setup_providers() -> list[Provider]:
    providers = [
        config_provider(),
        sqlalchemy_provider(),
        persistence_provider(),
        application_cases_provider(),
        kafka_log_provider(),
        fastapi_dishka.FastapiProvider(),
    ]

    return providers


@lru_cache(1)
def create_container() -> AsyncContainer:
    providers = setup_providers()
    container = make_async_container(*providers, context={MainConfig: main_config})

    return container


container: Final[AsyncContainer] = create_container()
