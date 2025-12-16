import time
import json
import random
import numpy as np
from kafka import KafkaProducer

# Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'input-stream'

def get_producer():
    try:
        return KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
    except Exception as e:
        print(f"Error connecting to Kafka: {e}")
        return None

def generate_data(stream_id):
    # Simulate normal data: Gaussian distribution mean=0, std=1
    # Simulate DRIFT: Shift mean to 5.0 after stream_id > 100
    mean = 0.0
    if stream_id > 100:
        mean = 5.0  # DRIFT HAPPENS HERE
        print(f"--- SIMULATING DRIFT (Mean shifted to {mean}) ---")
    
    # Create a vector of 4 random features
    features = np.random.normal(loc=mean, scale=1.0, size=4).tolist()
    
    return {
        'id': stream_id,
        'timestamp': time.time(),
        'features': features
    }

if __name__ == "__main__":
    print("Starting Data Producer...")
    producer = get_producer()
    
    if not producer:
        print("Could not connect to Kafka. Make sure Docker is running.")
        exit(1)

    i = 0
    try:
        while True:
            data = generate_data(i)
            producer.send(TOPIC_NAME, value=data)
            print(f"Sent: {data}")
            time.sleep(1) # Send 1 record per second
            i += 1
    except KeyboardInterrupt:
        print("Stopping producer...")
        producer.close()
