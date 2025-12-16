from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

def main():
    # 1. Setup the Flink environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    
    # 2. Setup Table Environment (SQL-like)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    print("Flink Job Started...")

    # 3. Define the Source (Kafka)
    # This connects to the 'input-stream' topic we created in the producer
    t_env.execute_sql("""
        CREATE TABLE SourceTable (
            id INT,
            timestamp DOUBLE,
            features ARRAY<DOUBLE>
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'input-stream',
            'properties.bootstrap.servers' = 'kafka:9092',
            'scan.startup.mode' = 'latest-offset',
            'format' = 'json'
        )
    """)

    # 4. Define the Sink (Where results go - printing to console for now)
    t_env.execute_sql("""
        CREATE TABLE PrintSink (
            id INT,
            timestamp DOUBLE,
            features ARRAY<DOUBLE>,
            drift_detected BOOLEAN
        ) WITH (
            'connector' = 'print'
        )
    """)

    # 5. Process Data (Simple Drift Logic)
    # In a real scenario, this is where you'd call the TensorFlow model.
    # Here we just flag if the first feature is > 3.0 as a placeholder for drift.
    t_env.execute_sql("""
        INSERT INTO PrintSink
        SELECT 
            id, 
            timestamp, 
            features,
            CASE WHEN features[1] > 3.0 THEN TRUE ELSE FALSE END as drift_detected
        FROM SourceTable
    """)

if __name__ == '__main__':
    main()
