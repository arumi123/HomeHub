import sys
import os
import pathlib
import json
import requests
import math
import subprocess
import time
import threading

status = {
  "CurrentTemperature": 25,
  "SwingMode": 0,
  "RotationSpeed": 100,
  "TargetHeaterCoolerState": 2,
  "HeatingThresholdTemperature": 20,
  "CoolingThresholdTemperature": 27,
  "CurrentHeaterCoolerState": 3,
  "Active": 0
}

# 実行間隔を制御するためのグローバル変数
last_execution_time = 0
lock = threading.Lock()

# acDataHolderからエアコンの状態を読み取る。気温はCloudAPIから取得
def get_status():
  global status
  with open('/var/lib/homebridge/node_modules/acDataHolder.json', 'r') as f:
    contents = f.read()

  if contents == '':
    save_status()
  else:
    df = json.loads(contents)
    for key, item in df.items():
      status[key] = item

    save_status()

# 状態を変更し、statusを書き換える
def set_status():
  global status
  chara = sys.argv[3]
  value = float(sys.argv[4])

  if chara == 'HeatingThresholdTemperature':
    status['CurrentTemperature'] = status[chara]
    if value > 30:
      value = 30
    elif value < 16:
      value = 16
  elif chara == 'CoolingThresholdTemperature':
    status['CurrentTemperature'] = status[chara]
    if value > 30:
      value = 30
    elif value < 16:
      value = 16

  elif chara == 'RotationSpeed':
    if value < 10:
      value = 0
    elif value < 30:
      value = 20
    elif value < 50:
      value = 40
    elif value < 70:
      value = 60
    elif value < 90:
      value = 80
    else:
      value = 100

  value = math.ceil(value)

  if status[chara] != value:
    status[chara] = value

    if status['Active'] == 1:
      if status['TargetHeaterCoolerState'] == 1:
        status['CurrentHeaterCoolerState'] = 2
      elif status['TargetHeaterCoolerState'] == 2:
        status['CurrentHeaterCoolerState'] = 3
      else:
        status['CurrentHeaterCoolerState'] = 1
    else:
      status['CurrentHeaterCoolerState'] = 0

    save_status()
    #ac_signal.send(status, chara)
  try:
    combined_arg = sys.argv[3] + ":" + sys.argv[4]
    subprocess.run(['python3', 'irrp.py', "-p", "-g17", "-f", "codes", combined_arg])
  except:
    pass


# statusをacDataHolderに保存する
def save_status():
  global status
  with open('/var/lib/homebridge/node_modules/acDataHolder.json', 'w') as f:
    json.dump(status, f, indent=2)

# 実行を間隔1秒以内で制限するラッパー関数
def execute_with_delay(func):
  global last_execution_time
  with lock:
    current_time = time.time()
    time_since_last_execution = current_time - last_execution_time

    if time_since_last_execution < 1:
      time.sleep(1 - time_since_last_execution)

    func()
    last_execution_time = time.time()

if __name__ == "__main__":
  # statusを保存しておくファイルがなければ作る
  if not os.path.exists('/var/lib/homebridge/node_modules/acDataHolder.json'):
    cmd = pathlib.Path('/var/lib/homebridge/node_modules/acDataHolder.json')
    cmd.touch()

  execute_with_delay(get_status)

  if sys.argv[1] == 'Get':
    result = status[sys.argv[3]]
  elif sys.argv[1] == 'Set':
    execute_with_delay(set_status)
    result = sys.argv[4]

  print(result)
  sys.exit()