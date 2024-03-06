"""
# 의존성 주입으로 해당 processor 함수에서 전처리를 발생합니다.
# df 는 kafka topic 에서 받아온 json 데이터를 dataframe 화 한 변수 입니다.

"""


from src.DI.Util.Preprocessor import *


def microBatchProcessor(df, batch_id, spark):
    """
    # 스파크 스트리밍 DI 함수
    """

    """ 익스큐터에 흩어져있는 데이터프레임을 드라이버로 가져옵니다. """
    rowData = df.collect()

    """ 데이터가 존재할 시 실행됩니다. """
    if len(rowData) != 0:
        """ ftp 로그인 합니다. """
        Preprocessor.ftp_login()

        """ 데이터프레임의 각 행 단위로 로직이 실행됩니다. """
        for row in rowData:

            imgName = row['file_name']
            createTime = row['create_time']
            savePath = row['save_path']
            imgValue = row['image']

            try:
                """ 인코딩된 이미지 파일을 디코딩합니다. """
                img_bytes_array = Preprocessor.kafka_value_extractor(imgName, imgValue)

                """ 디코딩된 이미지 파일을 croping 합니다. """
                crop_byte_array = Preprocessor.croping_image(img_bytes_array)


                """ ftp를 통해 croping 이미지 파일을 업로드합니다. """
                Preprocessor.image_saver(savePath, imgName, crop_byte_array)

            except Exception as e:
                print(e)

        """ ftp 로그아웃 합니다. """
        Preprocessor.ftp_logout()







