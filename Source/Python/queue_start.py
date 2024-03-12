import sys
from pydantic import BaseModel 
from queuing.queue_connection import QueueConnection


class TestModel(BaseModel):
    name: str
    age: int
    is_active: bool


class QueueProducer():
    def __init__(self, model_data=TestModel(name="John", age=30, is_active=True)) -> None:
        self.model_data = model_data

        
    def start(self):
        print("Publisher started")
        queue = QueueConnection()
        body = self.model_data.model_dump_json()

        print(f"Publishing message: {body}")
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
        print("Starting publisher")
        QueueProducer().start()
    if op and op == "consumer":
        print("Starting consumer")
        QueueConsumer().start()