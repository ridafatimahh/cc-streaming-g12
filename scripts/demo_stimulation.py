import time
import random
import sys

def print_log(component, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{component}] {message}")

def simulate_inference():
    # Simulate loading
    print("Initializing System...")
    time.sleep(1)
    print_log("ZOOKEEPER", "Server started on port 2181")
    time.sleep(1)
    print_log("KAFKA", "Broker ID 1 started on port 9092")
    time.sleep(1)
    print_log("FLINK", "JobManager connected to Kafka Source")
    print_log("TF-SERVING", "Model 'my_model' loaded successfully (Version: 1)")
    print("-" * 60)
    print("SYSTEM LIVE - WAITING FOR STREAM...")
    print("-" * 60)
    time.sleep(2)

    event_id = 100
    mean = 0.0
    
    try:
        while True:
            # 1. Generate Data (Producer Logic)
            if event_id > 115:
                mean = 5.0 # DRIFT HAPPENS
                if event_id == 116:
                    print("\n>>> [PRODUCER] INJECTING CONCEPT DRIFT (Mean Shift) <<<\n")
            
            features = [round(random.gauss(mean, 1.0), 2) for _ in range(4)]
            data = {'id': event_id, 'ts': time.time(), 'features': features}
            
            # 2. Simulate Processing (Flink Logic)
            prediction = 0 if mean < 2.0 else 1
            confidence = round(random.uniform(0.85, 0.99), 2)
            
            # 3. Drift Detection Logic
            drift_score = sum(features) / 4.0
            status = "NORMAL"
            
            log_color = ""
            if drift_score > 3.0:
                status = "DRIFT_DETECTED"
                log_color = "!!!" 

            # Print the log line
            print(f"[FLINK-PROCESSOR] EventID:{event_id} | Features:{features} | Pred:{prediction} | Status:{status} {log_color}")
            
            if status == "DRIFT_DETECTED" and event_id == 116:
                 print_log("DRIFT-MODULE", "WARNING: Statistical distribution changed! Flagging for retraining...")

            time.sleep(1.0) # 1 second delay to look like real-time
            event_id += 1

    except KeyboardInterrupt:
        print("\nStopping Demo...")

if __name__ == "__main__":
    simulate_inference()
