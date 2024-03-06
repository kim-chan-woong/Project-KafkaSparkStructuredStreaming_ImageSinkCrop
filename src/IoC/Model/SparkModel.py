from src.DI.MicroBatchProcessor import microBatchProcessor
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import from_json
from src.DI.VO.SchemaRegistry import *
from src.DI.config import ConfigMaster


class SparkModel:

    """
    # kafka 관련 옵션

    # BOOTSTRAP_SERVERS : Kafka cluster 주소
    # SINK_TOPIC_NAME : Sink 할 토픽 이름
    # CHECKPOINT_LOCATION : Kafka offset 저장될 경로
    # GROUP_ID : Spark Consumer group 이름
    # STARTING_OFFSETS : Kafka read offset 위치
    # SINK_MAX_OFFSETS_PER_TRIGGER : 한 오프셋당 기록할 메시지 수
    # FAIL_ON_DATA_LOSS : 토픽이나 오프셋을 찾을 수 없을 경우 쿼리 실패 유무 (defaultL true, 컨슈머 그룹 리밸런싱 대비 false)

    """
    BOOTSTRAP_SERVERS = ConfigMaster.get_kafka_sink_cluster()
    SINK_TOPIC_NAME = ConfigMaster.get_kafka_sink_topic()
    CHECKPOINT_LOCATION = ConfigMaster.get_kafka_checkpoint_location()
    GROUP_ID = ConfigMaster.get_kafka_group_id()
    STARTING_OFFSETS = ConfigMaster.get_starting_offset()
    SINK_MAX_OFFSETS_PER_TRIGGER = ConfigMaster.get_sink_max_offsets_per_trigger()
    FAIL_ON_DATA_LOSS = "false"

    def createSession(self, app_name) -> SparkSession:
        """
        # Spark session 선언
        # return : pyspark.sql.SparkSession
        """
        return SparkSession.builder \
                .appName(app_name).getOrCreate()


    def kafka_read_stream_session(self, spark: SparkSession) -> DataFrame:
        """
        # kafka 의 지정된 클러스터, 토픽에서 stream 을 실시간으로 읽어오는 함수
        """
        return spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.BOOTSTRAP_SERVERS) \
            .option("subscribe", self.SINK_TOPIC_NAME) \
            .option("startingOffsets", self.STARTING_OFFSETS) \
            .option("kafka.group.id", self.GROUP_ID) \
            .option("failOnDataLoss", self.FAIL_ON_DATA_LOSS) \
            .option("maxOffsetsPerTrigger", self.SINK_MAX_OFFSETS_PER_TRIGGER) \
            .load()


    def kafka_json_value_parser(self, spark: DataFrame) -> DataFrame:
        """
        # kafka 에서 읽어온 json value 를 테이블화 시키는 함수
        """

        return spark.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", SchemaRegistry.kafka_sink_schema()).alias("data")) \
            .select("data.*")


    def kafka_streaming_starter(self, spark:DataFrame, preproces_session:SparkSession):
        """
        # 카프카 스트리밍 실행 함수 
        """
        query = spark \
            .writeStream \
            .outputMode("append") \
            .foreachBatch(lambda df, batch_id : microBatchProcessor(df, batch_id, preproces_session)) \
            .option("checkpointLocation", self.CHECKPOINT_LOCATION) \
            .start()

        
        query.awaitTermination()

