# RabbitMQ-Testing

# How to run file locally
```sh
    #Rebuilds app image
    docker-compose build pubcon
    #Starts up app and rabbitmq server
    docker-compose -p pubcon up -d --remove-orphans
```