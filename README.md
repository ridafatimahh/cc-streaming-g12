# Real-time Inference on Streams with Drift Detection

## Group 12 - AIML and Analytics Services

### Project Overview
This project implements a real-time machine learning pipeline that ingests streaming data, performs feature transformation using **Apache Flink**, and sends data to **TensorFlow Serving** for inference. It includes a drift detection module to identify concept drift and flag the model for offline retraining.

### Architecture
1.  **Data Source**: Python-based stream producer (Kafka).
2.  **Stream Processing**: Apache Flink (DataStream API).
3.  **Model Serving**: TensorFlow Serving (Docker container).
4.  **Drift Detection**: Online statistical monitoring.

### Prerequisites
* Docker & Docker Compose
* Python 3.8+

### How to Run
1.  Start the services:
    ```bash
    docker-compose up -d
    ```
2.  Run the data generator:
    ```bash
    python src/producer/main.py
    ```
