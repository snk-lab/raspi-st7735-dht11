# raspi-st7735-dht11
Connecting temperature and humidity to the Raspberry Pi and displaying it on a monitor

###### ラズパイにInstallするのにバージョン管理しつつIDE経由で行いたかったのでgithubを利用しました。  
なんの保障もしませんがちょっとだけでも誰かの役に立つかもしれないのでpublicにしました。  
あんまりPython知らないので間違いあるかも。

ラズパイにDH11の温度・湿度センサーを接続して1.8インチ TFTに一定間隔で表示、  
さらに外部APIを叩いて値を更新するってのをやります。  
※外部API接続はまだ未実装

####ST7735 1.8 TFT

|Screen Pin	| Raspberry Pi Pin |
----| ----
|GND	|Ground (pins 6, 9, 14, 20, 25, 30, 34 or 39)
|VCC	|5v Power (pins 2 or 4)
|SCL	|GPIO 11 (pin 23)
|SDA	|GPIO 10 (pin 19)
|RES	|GPIO 25 (pin 22)
|DC	|GPIO 24 (pin 18)
|CS	|GPIO 8 (pin 24)
|BL	|Not connected
BLはバックライト GPIO12などで制御可

####DHT11
|Screen Pin	| Raspberry Pi Pin |
----| ----
|GND -|Ground (pins 6, 9, 14, 20, 25, 30, 34 or 39)
|5V +|5v Power (pins 2 or 4)
|Output | GPIO4(GPLCK0)
3pinのモジュールインターフェースに付いてるタイプ

###### ラズパイ初期設定、SSH接続など終わっている事 
###### Raspberry pi のpythonが3系であることが前提


##### まずRaspiの設定を行う
`sudo raspi-config`
##### 必要なライブラリをインスト-ル
`sudo python -m pip install RPi.GPIO spidev Pillow numpy`  
`sudo python -m pip install st7735`  

######必要に応じてフォントやtimestamp系のライブラリなど

##### DHT11モジュール
`cd ~`  
`sudo git clone https://github.com/szazo/DHT11_Python.git`  
`cd DHT11_Python`  
`sudo pip install dht11`  
`sudo cp DHT11_Python/dh11 ./raspi-st7735-dh11`

必要なのはdh11の中身  
こちらを参考にさせていただきました。
https://www.souichi.club/raspberrypi/temperature-and-humidity/

これで動くはず

参考
`pip install git+https://github.com/Yoshiki443/weather_parameters`  
気象関連の計算ライブラリ