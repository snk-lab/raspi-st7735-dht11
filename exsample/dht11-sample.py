# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 09:17:11 2019
RaspberryPi Zero and 3 B+
温度、湿度センサーのテスト
@author: Souichirou Kikuchi
"""

import RPi.GPIO as GPIO
from time import sleep
import dht11  # 温湿度センサーモジュール

TEMP_SENSOR_PIN = 4  # 温湿度センサーのピンの番号
INTERVAL = 10  # 監視間隔（秒）
RETRY_TIME = 2  # dht11から値が取得できなかった時のリトライまので秒数
MAX_RETRY = 20  # dht11から温湿度が取得できなかった時の最大リトライ回数


class EnvSensorClass:  # 温湿度センサークラス
    def __init__(self):
        pass

    def GetTemp(self):  # 温湿度を取得
        instance = dht11.DHT11(pin=TEMP_SENSOR_PIN)
        retry_count = 0
        while True:  # MAX_RETRY回まで繰り返す
            retry_count += 1
            result = instance.read()
            if result.is_valid():  # 取得できたら温度と湿度を返す
                return result.temperature, result.humidity
            elif retry_count >= MAX_RETRY:
                return 99.9, 99.9  # MAX_RETRYを過ぎても取得できなかった時に温湿度99.9を返す
            sleep(RETRY_TIME)


GPIO.setwarnings(False)  # GPIO.cleanup()をしなかった時のメッセージを非表示にする
GPIO.setmode(GPIO.BCM)  # ピンをGPIOの番号で指定

# main
try:
    if __name__ == "__main__":
        env = EnvSensorClass()
        while True:
            temp, hum = env.GetTemp()  # 温湿度を取得
            print("温度 = ", temp, " 湿度 = ", hum, "％")
            sleep(INTERVAL)
except KeyboardInterrupt:
    pass
GPIO.cleanup()


