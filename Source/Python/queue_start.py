import sys
import psycopg
import os
import time


from pydantic import BaseModel 
from queuing.queue_connection import QueueConnection
from util.logging_util import logger
from dotenv import load_dotenv


class TestModel(BaseModel):
    name: str
    age: int
    is_active: bool


class QueueProducer():
    def __init__(self, model_data=TestModel(name="John", age=30, is_active=True)) -> None:
        self.model_data = model_data

        
    def start(self):
        logger.info("Publisher started")

        #Load environment variables into variables
        if os.environ.get("DATABASE_NAME") is None:
            logger.error("DATABASE_NAME environment variable is missing")
            return
        if os.environ.get("DATABASE_USER") is None:
            logger.error("DATABASE_HOST environment variable is missing")
            return
        if os.environ.get("DATABASE_PASSWORD") is None:
            logger.error("DATABASE_PASSWORD environment variable is missing")
            return
        if os.environ.get("DATABASE_HOST") is None:
            logger.error("DATABASE_HOST environment variable is missing")
            return
        
        database_name = os.environ.get("DATABASE_NAME")
        database_user = os.environ.get("DATABASE_USER")
        database_pass = os.environ.get("DATABASE_PASSWORD")
        database_host = os.environ.get("DATABASE_HOST")
        # Connect to postgres database
        try:
            logger.info("Connecting to database")
            db_connection = psycopg.connect(
                dbname=database_name,
                user=database_user,
                password=database_pass,
                host=database_host,
                port="5432"
            )
            cur = db_connection.cursor()
            db_connection.commit()
            cur.close()
            db_connection.close()
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
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

    if os.environ.get('APPLICATION_ENV') == 'development':
        logger.info("Running in development environment")
        load_dotenv()

    op = None if len(sys.argv) == 1 else sys.argv[1]
    if op and op == "producer":
        logger.info("Starting publisher")
        QueueProducer().start()
    if op and op == "consumer":
        logger.info("Starting consumer")
        QueueConsumer().start()