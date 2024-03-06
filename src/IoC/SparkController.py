from src.IoC.Model.SparkModel import *
from src.DI.config import ConfigMaster

class SparkController(SparkModel):

    def __init__(self):
        super().__init__()

    def sparkStarter(self):

        # 스파크 스트리밍 용 세션 생성
        spark = super().createSession(ConfigMaster.get_spark_structured_streaming_app_id())
        # 스파크 전처리 용 세션 생성
        adhoc_spark = super().createSession(f"{ConfigMaster.get_spark_structured_streaming_app_id()}_ADHOC")

        # 카프카 스트리밍 세션 생성
        kafka_read_streaming = super().kafka_read_stream_session(spark)

        # 토픽 json 파싱
        kafka_json_parsed = super().kafka_json_value_parser(kafka_read_streaming)

        # 카프카 스트리밍 시작
        super().kafka_streaming_starter(kafka_json_parsed, adhoc_spark)

