import sys
import psycopg

from pydantic import BaseModel 
from queuing.queue_connection import QueueConnection
from util.logging_util import logger



class TestModel(BaseModel):
    name: str
    age: int
    is_active: bool


class QueueProducer():
    def __init__(self, model_data=TestModel(name="John", age=30, is_active=True)) -> None:
        self.model_data = model_data

        
    def start(self):
        logger.info("Publisher started")

        # Connect to postgres database
        try:
            db_connection = psycopg.connect(
                dbname="test_db",
                user="test_user",
                password="test_password",
                host="localhost",
                port="5432"
            )
        except:
            logger.error("Error connecting to database")
            return
        queue = QueueConnection()
        body = self.model_data.model_dump_json()

        logger.info(f"Publishing message: {body}")
        try:
            queue.publish_message(body)
            print("Message published")
        except Exception as e:
            print(f"Error publishing message: {e}")



class QueueConsumer():
    pass


if __name__ == "__main__":
    op = None if len(sys.argv) == 1 else sys.argv[1]
    if op and op == "producer":
        logger.info("Starting publisher")
        QueueProducer().start()
    if op and op == "consumer":
        logger.info("Starting consumer")
        QueueConsumer().start()