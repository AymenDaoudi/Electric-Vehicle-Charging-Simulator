import logging
from pyspark.sql.functions import from_json, col
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, MapType, IntegerType
import os
from charging_events_stream_processor import ingest_charging_events_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
CHARGING_EVENTS_TOPIC = os.getenv('CHARGING_EVENTS_TOPIC', 'charging_events')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
REPOSITORY = os.getenv("LAKEFS_REPOSITORY", "charging-data")
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'http://minio:9000')
LAKEFS_ENDPOINT = os.getenv("LAKEFS_ENDPOINT", "http://lakefs:8000")
LAKEFS_ACCESS_KEY = os.getenv("LAKEFS_ACCESS_KEY", "AKIAJBWUDLDFGJY36X3Q")
LAKEFS_SECRET_KEY = os.getenv("LAKEFS_SECRET_KEY", "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")

schema = StructType([
    StructField("session_id", StringType(), True),
    StructField("session_number", IntegerType(), True),
    StructField("station_id", StringType(), True),
    StructField("ev_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("payload", MapType(StringType(), StringType()), True)
])



logger.info("Starting Spark Streaming Job")

# Initialize Spark with Kafka packages
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

logger.info("Spark Session Created")  

try:
    ingest_charging_events_data(spark, schema)
    logger.info("Queries Ended")

except Exception as e:
    logger.error(f"An error occurred: {str(e)}")
    spark.stop()