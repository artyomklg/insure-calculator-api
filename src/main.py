from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka
from fastapi import FastAPI

from src.config import main_config
from src.infrastructure.di import container
from src.infrastructure.kafka_logger.log_scheduler import process_logs_batch
from src.presentation.webapi.handlers import setup_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        process_logs_batch, IntervalTrigger(seconds=main_config.kafka.log_seconds_interval)
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=True)
    await container.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Калькулятор страхования", docs_url=None, redoc_url=None, lifespan=lifespan)
    setup_fastapi_dishka(container, app)
    setup_handlers(app)
    return app
