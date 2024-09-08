# Facilities for individuals

## コンセプト
設備は、空間のためではなく、個人のためにある。
個人の意図を汲み取り、先回りして動く設備を実現する

##要求
- 利用者の発話の意図を汲み取り、設備が自動で動くこと
- 利用者のiphoneのhomekit appから、設備を操作できること
- 利用者の動きを読み取り、設備が自動で動くこと

##要件


iosのホームキットから家電が操作できる

Raspi zero whを使うこと
自作赤外線送受信回路を使うこと



デベロップブランチ　1回目のプッシュ
デベロップブランチ　2回目のプッシュ
coolerブランチ一回目
coolerぶらんち2かいめ

エアコンは以下のデータを読み取った
停止ボタン　
"Active": 0

冷房ボタン　
"TargetHeaterCoolerState": 2

暖房ボタン
"TargetHeaterCoolerState": 1

暖房時の温度設定
"HeatingThresholdTemperature": 20,

冷房時の温度設定
"CoolingThresholdTemperature": 27,

