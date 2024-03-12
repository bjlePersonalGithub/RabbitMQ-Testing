import pika
import os
import time

class QueueConnection(object):
    def __init__(self, hostname=None, user=None, password=None):

        if hostname is not None and hostname != "":
            self.hostname = hostname
        elif 'RABBITMQ_HOST' in os.environ:
            self.hostname = os.environ['RABBITMQ_HOST']
        else:    
            raise ValueError("RabbitMQ environment variable is missing")

        if user is not None and user != "":
            self.user = user
        elif 'RABBITMQ_USER' in os.environ:
            self.user = os.environ['RABBITMQ_USER']
        else:
            raise ValueError("RabbitMQ user environment variable is missing")
        
        if password is not None and password != "":
            self.password = password
        elif 'RABBITMQ_PASS' in os.environ:
            self.password = os.environ['RABBITMQ_PASS']
        else:
            raise ValueError("RabbitMQ password environment variable is missing")

    def get_credentials(self):
        return self.user, self.password

    def get_queue_hostname(self):
        return self.hostname
    
    def get_connection(self, max_retries=3, heartbeat=0):
        queue_hostname = self.get_queue_hostname()

        user, password = self.get_credentials()
        params = pika.ConnectionParameters(
            queue_hostname, 
            port=5672,
            credentials=pika.PlainCredentials(user, password),
            heartbeat=heartbeat
        )

        retries = 0
        connection = None
        while retries < max_retries:
            retries += 1
            try:
                connection = pika.BlockingConnection(params)
                break
            except Exception as e:
                print(f"Error connecting to RabbitMQ: {e}, retrying...")
                time.sleep(10)
        return connection
    
    def publish_message(self, body, queue_name="basic_queue"):
        connection = self.get_connection()
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='', routing_key=queue_name, body=body)
        print(f" [x] Sent {body}")
        channel.cancel()
        connection.close()
        return True