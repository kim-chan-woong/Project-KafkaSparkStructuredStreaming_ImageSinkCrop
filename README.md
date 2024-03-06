# Image Crop & Save Ftp Spark Steraming Project
 
<br>
 
Kafka Topic에 전송되는 인코딩 된 이미지, 메타데이터를 받아, Crop하여 FTP 서버에 저장하는 Spark Streaming 입니다. 
 
 
<br><br>
 
# 로직
1. 이전 Spark Streaming을 통해 이미지 Meta 데이터 저장이 완료되면 img-topic-02-test 토픽에 데이터가 전송됩니다.
 
2. img-topic-02-test 토픽 내 인코딩 된 이미지를 디코딩 합니다.
 
3. 디코딩 된 이미지를 Crop합니다.
 
4. Crop 한 이미지를 FTP 특정 경로에 저장합니다.
 
5. 저장 경로는 이전 이미지 Meta 저장 Spark Streaming 작업이 끝난 후 전송된 kafka 메시지 내 save_path를 사용합니다.

