from faststream.kafka import KafkaBroker

from src.config import main_config
from src.infrastructure.di import container
from src.infrastructure.persistence.repositories.log import SqlalchemyLogMessageRepository
from src.infrastructure.persistence.transaction_context import SqlalchemyTransactionContext


async def process_logs_batch() -> None:
    async with container() as request_container:
        log_repo = await request_container.get(SqlalchemyLogMessageRepository)
        kafka_broker = await request_container.get(KafkaBroker)
        tc = await request_container.get(SqlalchemyTransactionContext)

        messages = await log_repo.get_all_logs(limit=main_config.kafka.log_batch_size)
        if messages:
            await kafka_broker.connect()
            await kafka_broker.publish_batch(*messages, topic=main_config.kafka.log_topic)
            await log_repo.mark_as_sended_by_ids([m.log_id for m in messages])
            await tc.commit()
