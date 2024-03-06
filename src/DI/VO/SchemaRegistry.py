from pyspark.sql.types import StructType, StructField, StringType

class SchemaRegistry():

    @staticmethod
    def kafka_sink_schema():
        # Schema 정의
        return StructType([
            StructField("file_name", StringType()),
            StructField("create_time", StringType()),
            StructField("save_path", StringType()),
            StructField("image", StringType()),
        ])