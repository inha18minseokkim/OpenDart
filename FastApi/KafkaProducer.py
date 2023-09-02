from kafka import KafkaProducer
from json import dumps
import os
from loguru import logger
KAFKA_SERVER = os.environ['KAFKA_SERVER']
KAFKA_PORT = int(os.environ['KAFKA_PORT'])
logger.debug(KAFKA_SERVER)
logger.debug(KAFKA_PORT)
producer = KafkaProducer(acks = 0, compression_type='gzip',
                         bootstrap_servers=[f'{KAFKA_SERVER}:{KAFKA_PORT}']
                         ,value_serializer=lambda x : dumps(x).encode('utf-8'))
async def sendKafkaMessage(topic: str, data: dict):
    data_str = str(data)
    data_str = data_str.replace("'",'"')
    logger.debug(data_str)
    producer.send(topic,value=data_str)
    producer.flush()

if __name__ == "__main__":
    import asyncio
    asyncio.run(sendKafkaMessage("push", {"method": "sendMessage", "msg": "muyaho" + "\nkafka발송"}))