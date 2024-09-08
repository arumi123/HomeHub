# Facilities for individuals

## コンセプト
設備は、空間のためではなく、
個人の意図を汲み取り、先回りして動く設備を実現する

## 要求
- 利用者が、home appから、設備を操作できること
- 利用者の発話の意図を汲み取り、設備が自動で動くこと
- 利用者の動きを読み取り、設備が自動で動くこと
- 上記を機能の高い保守性を保つこと

## 要件
### 利用者が、home appから、設備を操作できること
#### 配置図
#### シーケンス図
#### 非機能要件
- homebridgeからの連続的なコマンド実行を、実行環境スペックに応じて、待つことができること


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

