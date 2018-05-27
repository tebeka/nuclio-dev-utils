# Multiple Processors with Kafka

## Run Kafka

	./kafka_producer.py --run-docker

This will create a topic called "franz" with 7 partitions

## Running Processors

	./run_processor.py --count 3

* This will run 3 processors. Each one has admin interface listening on 808{id} (id=1..3)
* We're currently using processor built from 1b88ea6
* Python handler listens on "franz" topic on partition {id}

## Sending Messages

	./kafka_producer.py


This will send messages with the body "Message {id}" endlessly
