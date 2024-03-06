import traceback
from PIL import Image
import io
import base64
from ftplib import FTP
from ftplib import error_perm
from src.DI.config import ConfigMaster
from io import BytesIO

class Preprocessor():

    """ FTP 세션을 생성합니다. """
    ftp = FTP()

    @classmethod
    def kafka_value_extractor(cls, imgName: str, imgValue: str) -> io.BytesIO:
        """
        # 파일명과 인코딩 상태의 이미지 파일을 입력값으로 받습니다.
        # 입력받은 값을 디코딩하여 리턴합니다.
        """

        try:
            """ 입력받은 문자열 형태의 인코딩된 이미지를 디코딩합니다. str -> io.BytesIO """
            imageBytes = base64.b64decode(imgValue)

            """ 디코딩된 이미지를 바이트배열에 담습니다. """
            img_bytes_array = io.BytesIO()
            img_bytes_array.write(imageBytes)
            img_bytes_array.seek(0)

            return img_bytes_array

        except:
            traceback.print_exc()
            print("IMG decoding error. file is: " + imgName)




    @classmethod
    def ftp_login(cls):
        """ FTP에 연결합니다. """
        cls.ftp.connect(ConfigMaster.get_ftp_host())
        cls.ftp.login(ConfigMaster.get_ftp_user(), ConfigMaster.get_ftp_password())

    @classmethod
    def ftp_logout(cls):
        """ FTP 연결을 종료합니다. """
        cls.ftp.close()

    @classmethod
    def ftp_mkdir(cls, imgDirPath: str):
        """ 저장 경로를 생성합니다. """

        try:
            cls.ftp.mkd(imgDirPath)

        except Exception as e:
            None






    @classmethod
    def image_saver(cls, save_path: str, imgName: str, crop_byte_array: io.BytesIO):
        """
        # 파일명, 파일 저장 경로, 디코딩 상태의 이미지 파일을 입력값으로 받습니다.
        # FTP로 업로드합니다.
        """

        if save_path.strip()[-1] != "/":
            save_path = save_path + "/"

        """ 저장 경로를 생성합니다. """
        imgDirPath = f"{save_path}CROP/"
        cls.ftp_mkdir(imgDirPath)

        try:

            """ 저장될 경로 및 파일 명입니다. """
            imgUploadPath = imgDirPath + imgName


            """ FTP를 통해 업로드 합니다. """
            cls.ftp.storbinary(f'STOR {imgUploadPath}', crop_byte_array)


        except:
            traceback.print_exc()
            print("IMG save failed or broken file saved is: " + imgName)




    @classmethod
    def croping_image(cls, img_bytes_array: io.BytesIO) -> io.BytesIO:
        """
        # Image crop 함수
        # FTP 사용 시 Memory 에서 작업 후 file 저장
        # return list
        """

        open_img_file = open_image(Image.open(img_bytes_array))

        """ 이미지 crop 처리합니다. """
        crop = "사업 소스 마스킹"
        crop_image = Image.fromarray(crop)

        """ Crop Numpy 배열 이미지 Byte 처리합니다. """
        crop_image_byte_array = BytesIO()
        crop_image.save(crop_image_byte_array, format='JPEG')
        crop_image_byte_array.seek(0)

        return crop_image_byte_array



