import RPi.GPIO as GPIO
import time
from picamera2 import Picamera2
import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime #現在時刻を取得するため
from PIL import Image
import os

class CallBack:
    def __init__(self):
        #GPIO6入力、プルアップに設定
        pin = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
        
        GPIO.remove_event_detect(pin)
        #割り込みイベント設定
        GPIO.add_event_detect(pin, GPIO.FALLING, bouncetime=1000)
        
        #コールバック関数登録
        GPIO.add_event_callback(pin, self.my_callback_one)
        #GPIO.add_event_callback(pin, self.my_callback_two)

        #Picamera2の初期化
        self.picam2 = Picamera2()
        self.picam2.stop()
        print("INIT DONE")

    def my_callback_one(self, channel):
        #画像のリストを初期化
        images = []

        
        #カメラの設定　（解像度は必要に応じて変更）
        config = self.picam2.create_still_configuration({"size": (640, 480)})
        self.picam2.configure(config)

        #カメラを起動
        self.picam2.start()

        time.sleep(2)

        #print("set ok")

        for i in range(60):

            #画像のキャプチャ
            image = self.picam2.capture_array()

            #ファイルの名前を時間にする
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            images.append({'image': image, 'timestamp': timestamp})

            #１秒あける
            time.sleep(1)

            #print(i)
        
        #カメラを止める
        self.picam2.stop()

        for image in images:
            np.save(f'{save_dir}/numpy/image_{image["timestamp"]}', image["image"])
            Image.fromarray(image['image']).save(f'{save_dir}/jpeg/image_{image["timestamp"]}.jpeg')


    # def my_callback_two(self, channel):
    #     print('Callback two')

    def callback_test(self):
        print("START")
        while True:
            time.sleep(1)

save_dir = '/home/pi/Pictures/' + datetime.now().strftime('%Y-%m-%d')
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    os.makedirs(save_dir + '/jpeg')
    os.makedirs(save_dir + '/numpy')

cb = CallBack()
cb.callback_test() #割り込みイベント待ち
