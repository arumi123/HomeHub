import sys
import os
import pathlib
import json
import requests
import math
import subprocess

status = {
  "CurrentTemperature": 25,
  # Minimum Value 0
  # Maximum Value 100
  # Step Value 0.1

  "SwingMode": 0,
  # 0 - "Swing disabled"
  # 1 - "Swing enabled"

  "RotationSpeed": 100,
  # Minimum Value: 0
  # Maximum Value: 100
  # Step Value: 1
  # Unit: percentage

  "TargetHeaterCoolerState": 2,
  # Valid Values
  # 0 - AUTO
  # 1 - HEAT
  # 2 - COOL

  "HeatingThresholdTemperature": 20,
  # Minimum Value: 0
  # Maximum Value: 25
  # Step Value: 0.1
  # Unit: celcius

  "CoolingThresholdTemperature": 27,
  # Minimum Value: 10
  # Maximum Value: 35
  # Step Value: 0.1
  # Unit: celcius

  "CurrentHeaterCoolerState": 3,
  # 0 - INACTIVE
  # 1 - IDLE
  # 2 - HEATING
  # 3 - COOLING

  "Active": 0
  # 0 - "Inactive"
  # 1 - "Active"
}

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

if __name__ == "__main__":
  print('\nHeaterCooler.py has been called\nHeaterCooler has been changed to this following: ', sys.argv[3], sys.argv[4])
  # statusを保存しておくファイルがなければ作る
  if os.path.exists('/var/lib/homebridge/node_modules/acDataHolder.json') == False:
    cmd = pathlib.Path('/var/lib/homebridge/node_modules/acDataHolder.json')
    cmd.touch()

  get_status()

  if sys.argv[1] == 'Get':
    result = status[sys.argv[3]]
  elif sys.argv[1] == 'Set':
    set_status()
    result = sys.argv[4]

  print(result)
  sys.exit()