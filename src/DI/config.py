class ConfigMaster():
    # sink kafka
    __KAFKA_SINK_TOPIC = "img-topic-02-test"
    __KAFKA_SINK_CLUSTER = "mast01:9092, mast02:9092, mast03:9092"
    __KAFKA_CHECKPOINT_LOCATION = "/user/spark/image/checkpoint/image_sink_crop/APP_01_TEST"
    __KAFKA_GROUP_ID = "IMAGE_SINK_CROP_GROUP_TEST"
    __SPARK_STRUCTURED_STREAMING_APP_ID = "IMAGE_SINK_CROP_01_TEST"
    __KAFKA_STARTING_OFFSETS = "earliest"
    # __KAFKA_STARTING_OFFSETS = "latest"
    __SINK_MAX_OFFSETS_PER_TRIGGER = 50
    # °ª ¼¼ÆÃ
    __FTP_HOST = ""
    __FTP_USER = ""
    __FTP_PASSWORD = ""

    # applying class method
    # sink kakfa getter
    @classmethod
    def get_kafka_sink_topic(cls):
        return cls.__KAFKA_SINK_TOPIC

    @classmethod
    def get_kafka_sink_cluster(cls):
        return cls.__KAFKA_SINK_CLUSTER

    @classmethod
    def get_kafka_checkpoint_location(cls):
        return cls.__KAFKA_CHECKPOINT_LOCATION

    @classmethod
    def get_kafka_group_id(cls):
        return cls.__KAFKA_GROUP_ID

    @classmethod
    def get_spark_structured_streaming_app_id(cls):
        return cls.__SPARK_STRUCTURED_STREAMING_APP_ID

    @classmethod
    def get_starting_offset(cls):
        return cls.__KAFKA_STARTING_OFFSETS

    @classmethod
    def get_sink_max_offsets_per_trigger(cls):
        return cls.__SINK_MAX_OFFSETS_PER_TRIGGER

    @classmethod
    def get_ftp_host(cls):
        return cls.__FTP_HOST

    @classmethod
    def get_ftp_user(cls):
        return cls.__FTP_USER

    @classmethod
    def get_ftp_password(cls):
        return cls.__FTP_PASSWORD
