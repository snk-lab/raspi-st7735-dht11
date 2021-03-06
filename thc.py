import RPi.GPIO as GPIO
import dht11  # 温湿度センサーモジュール
import ST7735
import textwrap
import datetime
# import wxparams as wx
from zoneinfo import ZoneInfo
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# ST7735 Config
disp = ST7735.ST7735(
    port=0,
    cs=0,
    dc=24,
    backlight=19,
    rst=25,
    width=128,
    height=160,
    rotation=90,
    invert=False
)


# Const
TEMP_SENSOR_PIN = 4  # 温湿度センサーのピンの番号
INTERVAL = 10  # 監視間隔（秒）
RETRY_TIME = 2  # dht11から値が取得できなかった時のリトライまので秒数
MAX_RETRY = 20  # dht11から温湿度が取得できなかった時の最大リトライ回数
# font = ImageFont.load_default()
JP_FONT = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
EN_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(JP_FONT, 18)  # 通常フォント
time_font = ImageFont.truetype(JP_FONT, 14)  # 日時フォント
made_font = ImageFont.truetype(JP_FONT, 12)  # Made By
MADE_BY = "Made by SnkLab."
DIFF_JST_FROM_UTC = 9
TIME_COLOR = (200, 200, 200)  # 時間フォントカラー
TMP_COLOR = (255, 228, 196)  # 温度フォントカラー
HUM_COLOR = (135, 206, 250)  # 湿度フォントカラー(相対湿度）
AHUM_COLOR = (64, 224, 208)  # 絶対湿度フォントカラー
WIDTH = disp.width  # ディスプレイ幅
HEIGHT = disp.height  # ディスプレイ高さ



# 温湿度を取得
def get_temp():
    instance = dht11.DHT11(pin=TEMP_SENSOR_PIN)
    retry_count = 0
    # MAX_RETRY回まで繰り返す
    while True:
        retry_count += 1
        result = instance.read()
        # 取得できたら温度と湿度を返す
        if result.is_valid():
            return result.temperature, result.humidity
        # MAX_RETRYを過ぎても取得できなかった時に温湿度99.9を返す
        elif retry_count >= MAX_RETRY:
            return 99.9, 99.9
        sleep(RETRY_TIME)


# text line draw
def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height

# 絶対湿度算出
def get_absolute_humidity(temp, hum):
    Psat = 6.1078 * pow(10, 7.5 * temp / (temp + 237.3))
    # saturated water amount
    Gsat = 217 * Psat / (temp + 273.15)
    # absolute humidity
    # ah=wx.Absolute_Humidity(temp,hum)
    return Gsat * hum / 100

# now datetime
def get_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)


GPIO.setwarnings(False)  # GPIO.cleanup()をしなかった時のメッセージを非表示にする
GPIO.setmode(GPIO.BCM)  # ピンをGPIOの番号で指定

# main
try:
    if __name__ == "__main__":
        while True:
            print('Start processing')
            # 温湿度を取得
            temp, hum = get_temp()
            # 絶対湿度取得
            Gabs = get_absolute_humidity(temp, hum)
            # print("温度 = ", temp, " 湿度 = ", hum, "％")
            tmp_str = u"温度 = " + str(temp) + u"℃"
            hum_str = u"湿度 = " + str(hum) + u"％"
            ah_str = u"絶対湿度 = " + str(round(Gabs, 2)) + u"g/m3"

            # 描画Start
            img = Image.new('RGB', (WIDTH, HEIGHT))
            now = get_now()
            day_str = now.strftime('%Y年%-m月%-d日')
            time_str = now.strftime('%H:%M')
            draw_multiple_line_text(img, time_str, time_font, TIME_COLOR, 0)
            draw_multiple_line_text(img, tmp_str, font, TMP_COLOR, 20)
            draw_multiple_line_text(img, hum_str, font, HUM_COLOR, 40)
            draw_multiple_line_text(img, ah_str, time_font, AHUM_COLOR, 60)
            draw_multiple_line_text(img, day_str, time_font, TIME_COLOR, 80)
            draw_multiple_line_text(img, MADE_BY, made_font, TIME_COLOR, 100)
            # display!
            disp.display(img)
            sleep(INTERVAL)
except KeyboardInterrupt:
    pass
GPIO.cleanup()
