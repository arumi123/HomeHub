import json

# JSONファイルを読み込む
with open("devicestate.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

# deviceリストからdevice_nameがCL-RS2のオブジェクトを見つける
brightness_value = None
for device in data.get("device", []):
    if device.get("device_name") == "CL-RS2":
        brightness_value = device.get("brightness")
        break

# brightness値を表示
if brightness_value is not None:
    print(f"Brightness of CL-RS2: {brightness_value}")
else:
    print("Device with name CL-RS2 not found.")