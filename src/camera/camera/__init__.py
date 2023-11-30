import runpy
import cv2
import mysql.connector
import numpy as np
import logging
from ultralytics import YOLO
import pandas as pd
import time

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler and set formatter
log_path = log_path = r'C:\Station\CameraTestLog.txt'
file_handler = logging.FileHandler(log_path)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)

# connect db
mydb = mysql.connector.connect(
    host="192.168.0.28",
    user="akilli_mikrofon_db",
    password="seZmZcO36LkXJQ76*",
    port="3306",
    database="PAS_ADVANCED"
)

mycursorHdmi = mydb.cursor()
mycursorHdmi1 = mydb.cursor()
mycursorHdmi2 = mydb.cursor()
mycursorHdmi3 = mydb.cursor()
mycursorSatellite = mydb.cursor()

stationCode = 0

# dosya yolu
file_path = r'c:\Station\stationCode.txt'

try:
    with open(file_path, "r") as file:
        for satir in file:
            stationCode = satir.strip()  # Her satırı işlemek için bu döngüyü kullanabilirsiniz

except FileNotFoundError:
    print("Dosya bulunamadı veya açılamadı.")

print("stationCode" + str(stationCode))
# logger.info("stationCode" + str(stationCode))


# function that execute hdmi1 query
# eger kayıt yoksa bildirir.
def resultHdmi1():
    mycursorHdmi1.execute(
        "select bHdmi1 from PAS_ADVANCED.DefSourceCameraTest where u32stationCode =" + str(stationCode))
    resultHdmi1 = mycursorHdmi1.fetchone()

    if resultHdmi1 is None:
        print("Hata: "+str(stationCode)+" istasyonuna ait hdmi1 kaydı bulunamadı.")
        logger.error("Hata: "+str(stationCode)+" istasyonuna ait hdmi1 kaydı bulunamadı.")
        return None
    else:
        return resultHdmi1[0]


# function that execute hdmi2 query
def resultHdmi2():
    resultHdmi2 = False
    mycursorHdmi2.execute(
        "select bHdmi2 from PAS_ADVANCED.DefSourceCameraTest where u32stationCode =" + str(stationCode))
    resultHdmi2 = mycursorHdmi2.fetchone()
    if resultHdmi2 is None:
        print("Hata: " + str(stationCode) + " istasyonuna ait hdmi2 kaydı bulunamadı.")
        logger.error("Hata: " + str(stationCode) + " istasyonuna ait hdmi2 kaydı bulunamadı.")
        return None
    else:
        return resultHdmi2[0]

# function that execute hdmi3 query
def resultHdmi3():
    resultHdmi3 = False
    mycursorHdmi3.execute(
        "select bHdmi3 from PAS_ADVANCED.DefSourceCameraTest where u32stationCode =" + str(stationCode))
    resultHdmi3 = mycursorHdmi3.fetchone()

    if resultHdmi3 is None:
        print("Hata: " + str(stationCode) + " istasyonuna ait hdmi3 kaydı bulunamadı.")
        logger.error("Hata: " + str(stationCode) + " istasyonuna ait hdmi3 kaydı bulunamadı.")
        return None
    else:
        return resultHdmi3[0]


# function that execute productid on hdmi
def hdmiProductId():
    hdmiProductId = False
    mycursorHdmi.execute(
        "select u32recProductId from PAS_ADVANCED.DefSourceCameraTest where u32stationCode =" + str(stationCode))
    hdmiProductId = mycursorHdmi.fetchone()[0]
    return hdmiProductId


# function that execute satellite trt query
def satelliteTrt():
    resultSatellite = False
    mycursorSatellite.execute(
        "select bSatelliteTrt from PAS_ADVANCED.DefSatellite where u32stationCode =" + str(stationCode))
    resultSatellite = mycursorSatellite.fetchone()

    if resultSatellite is None:
        print("Hata: " + str(stationCode) + " istasyonuna ait Satellite Trt kaydı bulunamadı.")
        logger.error("Hata: " + str(stationCode) + " istasyonuna ait Satellite Trt kaydı bulunamadı.")
        return None
    else:
        return resultSatellite[0]


# function that execute satellite show query
def satelliteShow():
    resultSatellite = False
    mycursorSatellite.execute(
        "select bSatelliteShow from PAS_ADVANCED.DefSatellite where u32stationCode =" + str(stationCode))
    resultSatellite = mycursorSatellite.fetchone()

    if resultSatellite is None:
        print("Hata: " + str(stationCode) + " istasyonuna ait Satellite Show kaydı bulunamadı.")
        logger.error("Hata: " + str(stationCode) + " istasyonuna ait Satellite Show kaydı bulunamadı.")
        return None
    else:
        return resultSatellite[0]


# function that execute productid on satellite
def satelliteProductId():
    satelliteProductId = False
    mycursorSatellite.execute(
        "select u32recProductId from PAS_ADVANCED.DefSatellite where u32stationCode =" + str(stationCode))
    satelliteProductId = mycursorSatellite.fetchone()[0]
    return satelliteProductId


# control camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
hasOpened = False

# if cap.isOpened() == True:
# logger.info('Camera worked successfully')
# else:
# logger.error('Camera does not work')

if cap.isOpened() == False:
    logger.error('Camera does not work')
    print('Camera does not work')

# logo file
model = YOLO('bestttt.pt')

# multithek logo
modelMulti = YOLO('multithek.pt')

# control function hdmi1
def hdmi1(controlCount):
    # while True:

    print("controlCount", controlCount)
    logger.info("controlCount for Hdmi1 : " + str(controlCount))

    # detect colors red and white
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([160, 155, 84], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    white_lower = np.array([0, 0, 200], np.uint8)
    white_upper = np.array([100, 0, 255], np.uint8)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    kernel = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    white_mask = cv2.dilate(white_mask, kernel)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

    # contours
    contoursRed, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursWhite, hierarchy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # detect red color
    def red_color():
        for pic, contour in enumerate(contoursRed):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                return "red"

    # detect white color
    def white_color():
        for pic, contour in enumerate(contoursWhite):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                return "white"

    resultHdmi1ProductId = hdmiProductId()

    time.sleep(2)

    # control hdmi1
    if (red_color() == "red" or white_color() == "white") and resultHdmi1() == 1:
        hdmi1query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi1Result='basarili' where u32recProductId = %s"""
        tuple1 = (resultHdmi1ProductId)
        mycursorHdmi1.execute(hdmi1query, (tuple1,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi1: Başarılı')
        print('Hdmi1: Başarılı')

    elif controlCount < 2:
        controlCount += 1
        hdmi1(controlCount)

    else:
        hdmi1query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi1Result='basarisiz' where u32recProductId = %s"""
        tuple1 = (resultHdmi1ProductId)
        mycursorHdmi1.execute(hdmi1query, (tuple1,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi1: Başarısız')
        print('Hdmi1: Başarısız')

    # update bHdmi1 = 0
    if resultHdmi1() == 1:
        hdmi1query = """update PAS_ADVANCED.DefSourceCameraTest set bHdmi1 = 0 where u32recProductId = %s"""
        mycursorHdmi1.execute(hdmi1query, (tuple1,))
        mydb.commit()
        logger.info('bHdmi1 = 0 ayarlandi')
        print("bHdmi1 = 0")


# control function hdmi2
def hdmi2(controlCount):
    print("controlCount", controlCount)
    logger.info("controlCount for Hdmi2 : " + str(controlCount))

    # while True:
    # detect colors red and white
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([160, 155, 84], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    white_lower = np.array([0, 0, 200], np.uint8)
    white_upper = np.array([100, 0, 255], np.uint8)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    kernel = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    white_mask = cv2.dilate(white_mask, kernel)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

    # contours
    contoursRed, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursWhite, hierarchy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # detect red color
    def red_color():
        for pic, contour in enumerate(contoursRed):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                return "red"

    # detect white color
    def white_color():
        for pic, contour in enumerate(contoursWhite):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                return "white"

    resultHdmi2ProductId = hdmiProductId()

    time.sleep(2)

    # control hdmi2
    if (red_color() == "red" or white_color() == "white") and resultHdmi2() == 1:
        hdmi2query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi2Result='basarili' where u32recProductId = %s"""
        tuple2 = (resultHdmi2ProductId)
        mycursorHdmi2.execute(hdmi2query, (tuple2,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi2: Başarılı')
        print('Hdmi2: Başarılı')

    elif controlCount < 2:
        controlCount += 1
        hdmi2(controlCount)

    else:
        hdmi2query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi2Result='basarisiz' where u32recProductId = %s"""
        tuple2 = (resultHdmi2ProductId)
        mycursorHdmi2.execute(hdmi2query, (tuple2,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi2: Başarısız')
        print('Hdmi2: Başarısız')

    # update bHdmi2 = 0
    if resultHdmi2() == 1:
        hdmi2query = """update PAS_ADVANCED.DefSourceCameraTest set bHdmi2 = 0 where u32recProductId = %s"""
        tuple2 = (resultHdmi2ProductId)
        mycursorHdmi2.execute(hdmi2query, (tuple2,))
        mydb.commit()
        logger.info('bHdmi2 = 0 ayarlandi')
        print("bHdmi2 = 0")

# control function hdmi3
def hdmi3(controlCount):
    print("controlCount", controlCount)
    logger.info("controlCount for Hdmi3 : " + str(controlCount))

    # while True:
    # detect colors red and white
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([160, 155, 84], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    white_lower = np.array([0, 0, 200], np.uint8)
    white_upper = np.array([100, 0, 255], np.uint8)

    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

    white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

    kernel = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernel)
    res_red = cv2.bitwise_and(frame, frame, mask=red_mask)

    white_mask = cv2.dilate(white_mask, kernel)
    res_white = cv2.bitwise_and(frame, frame, mask=white_mask)

    # contours
    contoursRed, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursWhite, hierarchy = cv2.findContours(white_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # detect red color
    def red_color():
        for pic, contour in enumerate(contoursRed):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(frame, "Red", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                return "red"

    # detect white color
    def white_color():
        for pic, contour in enumerate(contoursWhite):
            areaRed = cv2.contourArea(contour)
            if (areaRed > 300):
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(hsvFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, "White", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
                return "white"

    resultHdmi3ProductId = hdmiProductId()

    time.sleep(2)

    # control hdmi3
    if (red_color() == "red" or white_color() == "white") and resultHdmi3() == 1:
        hdmi3query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi3Result='basarili' where u32recProductId = %s"""
        tuple3 = (resultHdmi3ProductId)
        mycursorHdmi3.execute(hdmi3query, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi3: Başarılı')
        print('Hdmi3: Başarılı')

    elif controlCount < 2:
        controlCount += 1
        hdmi3(controlCount)

    else:
        hdmi3query = """update PAS_ADVANCED.RecCameraTestResult set sHdmi3Result='basarisiz' where u32recProductId = %s"""
        tuple3 = (resultHdmi3ProductId)
        mycursorHdmi3.execute(hdmi3query, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Hdmi3: Başarısız')
        print('Hdmi3: Başarısız')

    # update bHdmi3 = 0
    if resultHdmi3() == 1:
        hdmi3query = """update PAS_ADVANCED.DefSourceCameraTest set bHdmi3 = 0 where u32recProductId = %s"""
        tuple3 = (resultHdmi3ProductId)
        mycursorHdmi3.execute(hdmi3query, (tuple3,))
        mydb.commit()
        logger.info('bHdmi3 = 0 ayarlandi')
        print("bHdmi3 = 0")


# control function logo trt
def logoTrt(controlCount):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()

    logger.info("controlCount for Logo Trt: " + str(controlCount))

    def logoResult():
        print("logo Trt giris")
        results = model.predict(frame)

        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        print(px)
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if cv2.rectangle:
                print("logo")
                return "logo"

    resultSatelliteProductId = satelliteProductId()

    time.sleep(3)

    if logoResult() == "logo" and satelliteTrt() == 1:
        satellitequery = """update PAS_ADVANCED.RecSatelliteResult set sSatelliteTrtResult='basarili' where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Trt yayin basarili')
        print("Trt yayin basarili")
    elif controlCount < 3:
        controlCount += 1
        logoTrt(controlCount)
    else:
        satellitequery = """update PAS_ADVANCED.RecSatelliteResult set sSatelliteTrtResult='basarisiz' where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Trt yayin basarisiz')
        print("Trt yayin basarisiz")

    # update bSatelliteTrt = 0
    if satelliteTrt() == 1:
        satellitequery = """update PAS_ADVANCED.DefSatellite set bSatelliteTrt = 0 where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        logger.info('bSatelliteTrt = 0 ayarlandi')
        print("bSatelliteTrt = 0 ayarlandi")


# control function logo show
def logoShow(controlCount):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    ret, frame = cap.read()

    logger.info("controlCount for Logo Show: " + str(controlCount))

    def logoResult():
        print("logo Show giris")
        results = model.predict(frame)

        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        print(px)
        for index, row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if cv2.rectangle:
                print("logo")
                return "logo"

    resultSatelliteProductId = satelliteProductId()

    time.sleep(3)

    if logoResult() == "logo" and satelliteShow() == 1:
        satellitequery = """update PAS_ADVANCED.RecSatelliteResult set sSatelliteShowResult='basarili' where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Show yayin basarili')
        print("Show yayin basarili")
    elif controlCount < 3:
        controlCount += 1
        logoShow(controlCount)
    else:
        satellitequery = """update PAS_ADVANCED.RecSatelliteResult set sSatelliteShowResult='basarisiz' where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        time.sleep(5)
        logger.info('Show yayin basarisiz')
        print("Show yayin basarisiz")

    # update bSatelliteHow = 0
    if satelliteShow() == 1:
        satellitequery = """update PAS_ADVANCED.DefSatellite set bSatelliteShow = 0 where u32recProductId = %s"""
        tuple3 = (resultSatelliteProductId)
        mycursorSatellite.execute(satellitequery, (tuple3,))
        mydb.commit()
        logger.info('bSatelliteShow = 0 ayarlandi')
        print("bSatelliteShow = 0 ayarlandi")



# control hdmi1
while resultHdmi1() == 1:
    logger.info('Hdmi1 takili')
    print("hdmi1 takılı")

    controlCount = 0
    try:
        hdmi1(controlCount)
    except Exception as e:
        logger.error('Hdmi1 kontrol hatasi: Hdmi1 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz. ' + str(e))
        print("Hdmi1 kontrol hatasi: Hdmi1 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz.  " + str(e))
    time.sleep(5)

    if resultHdmi1() == 0:
        logger.info('Hdmi1 testi sonlandi')
        print("hdmi1 test sonlandi")
        # while True:
        # runpy.run_path('main.py', run_name='main')

# control hdmi2
while resultHdmi2() == 1:
    logger.info('Hdmi2 takili')
    print("hdmi2 takılı")

    controlCount = 0
    try:
        hdmi2(controlCount)
    except Exception as e:
        logger.error('Hdmi2 kontrol hatasi: Hdmi2 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz. ' + str(e))
        print("Hdmi2 kontrol hatasi: Hdmi2 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz.  " + str(e))

    time.sleep(5)

    if resultHdmi2() == 0:
        logger.info('Hdmi2 testi sonladi')
        print("hdmi2 test sonlandi")
    # while True:
    # runpy.run_path('main.py', run_name='main')

# control hdmi3
while resultHdmi3() == 1:
    logger.info('Hdmi3 takili')
    print("hdmi3 takılı")

    controlCount = 0

    try:
        hdmi3(controlCount)
    except Exception as e:
        logger.error('Hdmi3 kontrol hatasi: Hdmi3 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz.  ' + str(e))
        print("Hdmi3 kontrol hatasi: Hdmi3 testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz. " + str(e))

    time.sleep(5)

    if resultHdmi3() == 0:
        logger.info('Hdmi3 testi sonladi')
        print("hdmi3 test sonlandi")
    # while True:
    # runpy.run_path('main.py', run_name='main')


# control logo trt
while satelliteTrt() == 1:
    logger.info('Trt yayini basladi')
    print("Trt yayini basladi")

    controlCount = 0

    try:
        logoTrt(controlCount)
    except Exception as e:
        logger.error('Yayin kontrol hatasi: yayın testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz. ' + str(e))
        print("Yayin kontrol hatasi: yayın testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz." + str(e))

    time.sleep(5)
    if satelliteTrt() == 0:
        logger.info('Yayin testi sonlandi')
        print("yayin testi sonlandi")
        # while True:
        # runpy.run_path('main.py', run_name='main')

# control logo show
while satelliteShow() == 1:
    logger.info('Show yayini basladi')
    print("Show yayini basladi")

    controlCount = 0

    try:
        logoShow(controlCount)
    except Exception as e:
        logger.error('Yayin kontrol hatasi: yayın testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz. ' + str(e))
        print("Yayin kontrol hatasi: yayın testi başladı ama kameradan görüntü alınamıyor. Kamerayı kontrol ediniz." + str(e))

    time.sleep(5)
    if satelliteShow() == 0:
        logger.info('Yayin testi sonlandi')
        print("yayin testi sonlandi")
        # while True:
        # runpy.run_path('main.py', run_name='main')

# no cables are connected
if resultHdmi1() != 1 and resultHdmi2() != 1 and resultHdmi3() != 1 and satelliteTrt() != 1 and satelliteShow() != 1:
    try:
        # logger.error('program calismiyor hicbir kablo bagli degil')
        print("program çalışmıyor, hiçbir kablo bağlı değil")
        time.sleep(5)
        while True:
            runpy.run_path('main.py', run_name='main')
    except Exception as e:
        logger.error('Hata: ' + str(e))
        print("Hata: " + str(e))