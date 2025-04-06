import json
import os
from time import sleep

class Devicefactory:
    @staticmethod
    def create_device(device_type, category):
        if category == "LightBulb":
            if device_type == "RE0207":
                return Re0207()
            elif device_type == "CL-RS2":
                return ClRs2()
        elif category == "HeaterCooler":
            if device_type == "PanasonicAC":
                return PanasonicAC()
        raise ValueError(f"Unsupported device type: {device_type}")

# Deviceクラス
class Device:
    def __init__(self):
        pass

    def get_status(self,attribute=None):
        # devicedriver.pyのあるディレクトリに移動
        os.chdir(os.path.dirname(__file__))

        # JSONファイルを読み込む
        try:
            with open("devicestate.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print("Failed to load device information from devicestate.json:", e)
            return None

        # クラス名が一致するデバイス情報をdevice_status変数に代入する
        class_name = self.__class__.__name__
        device_status = None
        for device in data.get("device", []):
            if device.get("class_name") == class_name:
                device_status = device
                break

        # attributeに指定がある場合は、その値をreturn
        if attribute:
            return device_status.get(attribute, None)
        else:
            return device_status
        
    def write_status(self, attribute, value):
        # devicedriver.pyのあるディレクトリに移動
        os.chdir(os.path.dirname(__file__))

        # JSONファイルを読み込む
        try:
            with open("devicestate.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print("Failed to load device information from devicestate.json:", e)
            return None

        # クラス名が一致するデバイス情報をdevice_status変数に代入する
        class_name = self.__class__.__name__
        device_status = None
        for device in data.get("device", []):
            if device.get("class_name") == class_name:
                device_status = device
                break
        
        print(device_status)

        if device_status is None:
            print("No device information found for class", class_name)
            return None

        # attributeの値を更新
        device_status[attribute] = value

        # JSONファイルに書き込む
        try:
            with open("devicestate.json", 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Failed to write device information to devicestate.json:", e)
            return None

# LightBulbドライバの抽象クラス
class LightBulb(Device):
    def brightness(self, bright):
        pass

    def colortemp(self,temp):
        pass

# シーリングライトのRE0207(CH1)のLightBulbドライバ
class Re0207(LightBulb):
    def brightness(self, bright):
        # brightが0~100の間にない場合はエラーを返し、0に設定する
        if not (0 <= getstatus(self,brightness) <= 100):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 100.")
        

        
        # 設定値を更新
        try:
            state = self.getstate()
            self.current_mode = state.get("mode", "off")
        except:
            self.current_mode = "off"

        if bright == 0:
            self.change_mode("off")
        elif 1 <= bright <= 9:
            self.change_mode("nightmode")
        else:
            self.change_mode("on")
            self.change_bright((bright // 10) - 1)
            
    def colortemp(self, temp):
        # tempが0~5の間にない場合はエラーを返す
        if not (0 <= temp <= 5):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 5.")
        
    
    def change_mode(self,mode):
        mode_sequence = ["on","night","off"]
        current_index = mode_sequence.index(self.current_mode)
        target_index = mode_sequence.index(mode)

        while current_index != target_index:
            current_index = (current_index + 1) % len(mode_sequence)
            self.current_mode = mode_sequence[current_index]
            print(f"Changing mode to {self.current_mode}")
            # リモコン操作のロジックをここに追加
            sleep(0.5)

    def change_brightness(self, target_brightness):
        if not (0 <= target_brightness <= 9):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 9.")
        
        current_brightness = self.brightness
        step = 1 if target_brightness > current_brightness else -1
        
        while current_brightness != target_brightness:
            current_brightness += step
            self.brightness = current_brightness
            print(f"Changing brightness to {current_brightness}")
            # リモコン操作のロジックをここに追加
            sleep(0.5)

    def change_colortemp(self,target_colortemp):
        if not (0 <= temp <= 5):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 5.")

# シーリングライトのCL-RS2のLightBulbドライバ
class ClRs2(LightBulb):
    def brightness(self, target_brightness):
        # brightが0~100の間にない場合は、エラーを返し、値0を代入する
        if not (0 <= self.get_status("brightness")  <= 100):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 100.")
            self.setstatus("brightness",0)
            
        # 場合分けして赤外線を送信
        # if target_brightness == 0:
        #     # 電源をオフにするコマンド
        #     self.change_mode("off")
        #     self.write_status("brightness",target_brightness)

        # elif 1 <= target_brightness <= 5:
        #     # 常夜灯とつけるコマンド
        #     self.change_mode("nightmode")
        #     self.write_status("brightness",target_brightness)

        # elif 6 <= target_brightness <= 10:
        #     # 明るさ1
        #     self.change_mode("on")
        #     self.change_brightness(1)
        #     self.write_status("brightness",target_brightness)

        # elif 11 <= target_brightness <= 20:
        #     # 明るさ2
        #     self.change_mode("on")
        #     self.change_brightness(2)
        #     self.write_status("brightness",target_brightness)

        # elif 21 <= target_brightness <= 30:
        #     # 明るさ3
        #     self.change_mode("on")
        #     self.change_brightness(3)
        #     self.write_status("brightness",target_brightness)

        # elif 31 <= target_brightness <= 40:
        #     # 明るさ4
        #     self.change_mode("on")
        #     self.change_brightness(4)
        #     self.write_status("brightness",target_brightness)

        # elif 41 <= target_brightness <= 50:
        #     # 明るさ5
        #     self.change_mode("on")
        #     self.change_brightness(5)
        #     self.write_status("brightness",target_brightness)

        # elif 51 <= target_brightness <= 60:
        #     # 明るさ6
        #     self.change_mode("on")
        #     self.change_brightness(6)
        #     self.write_status("brightness",target_brightness)

        # elif 61 <= target_brightness <= 70:
        #     # 明るさ7
        #     self.change_mode("on")
        #     self.change_brightness(7)
        #     self.write_status("brightness",target_brightness)

        # elif 71 <= target_brightness <= 80:
        #     # 明るさ8
        #     self.change_mode("on")
        #     self.change_brightness(8)
        #     self.write_status("brightness",target_brightness)

        # elif 81 <= target_brightness <= 90:
        #     # 明るさ9
        #     self.change_mode("on")
        #     self.change_brightness(9)
        #     self.write_status("brightness",target_brightness)

        # elif 91 <= target_brightness <= 100:
        #     # 明るさ10
        #     self.change_mode("on")
        #     self.change_brightness(10)
        #     self.write_status("brightness",target_brightness)

        if target_brightness == 0:
            # 電源オフ
            self.change_mode("off")
            self.write_status("brightness",target_brightness)

        elif 1 <= target_brightness <= 9:
            # 常夜灯
            self.change_mode("nightmode")
            self.write_status("brightness",target_brightness)

        else:
            # 電源オン 明るさの変更
            self.change_mode("on")
            self.change_brightness((target_brightness // 10) - 1)
            self.write_status("brightness",target_brightness)
            print("明るさを",((target_brightness // 10) - 1),"に変えた")
            
    def colortemp(self, temp):
        # tempが0~5の間にない場合はエラーを返す
        if not (0 <= temp <= 5):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 5.")
        
    
    def change_mode(self,target_mode):
        # 現在のモードを推測
        if self.get_status("brightness") == 0 :
            current_mode = "off"
        elif 1 <= self.get_status("brightness") <= 9 :
            current_mode = "nightmode"
        else:
            current_mode = "on"

        # モードの流れを定義
        mode_sequence = ["on","nightmode","off"]

        # 現在のモードと変更するモードとの差の分だけ、ボタンを押す
        current_index = mode_sequence.index(current_mode)
        target_index = mode_sequence.index(target_mode)

        while current_index != target_index:
            current_index = (current_index + 1) % len(mode_sequence)
            self.current_mode = mode_sequence[current_index]
            print(f"Changing mode to {self.current_mode}")
            # リモコン操作のロジックをここに追加
            sleep(0.5)

    def change_brightness(self, target_brightness):
        # 規定外の数値が引数に来た場合処理
        if not (0 <= target_brightness <= 9):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 9.")

        now_brightness = (self.get_status("brightness") // 10) - 1

        while target_brightness != now_brightness:
            if target_brightness > now_brightness:
                # 明るくするリモコン操作ロジック
                print("一段階明るくした")
                now_brightness += 1
                sleep(0.4)

            else:
                # 暗くするリモコン操作ロジック
                print("一段階暗くした")
                now_brightness -= 1
                sleep(0.4)
            
    def change_colortemp(self,target_colortemp):
        if not (0 <= temp <= 5):
            raise ValueError("Invalid brightness value. Please specify a value between 0 and 5.")

# HeaterCoolerドライバの抽象クラス
class HeaterCooler:
    def __init__(self):
        pass

    def getstate(self):
        pass

    def mode(self,mode):
        pass

    def temp(self,temp):
        pass

# PanasonicACのHeaterCoolerドライバ
class PanasonicAC:
    def __init__(self):
        pass

    def getstate(self):
        pass

    def mode(self,mode):
        # 現在の温度をjsonから取得
        # 現在の温度とターゲットのモードを送るロジックを追加
        pass

    def temp(self,temp):
        # 現在のモードを取得
        # 現在のモードとターゲットの温度を送るロジックを追加
        pass

# 赤外線送受信ドライバの抽象クラス
class Ir:
    def __init__(self):
        pass

    def send(self,code):
        pass

    def receive(self):
        pass

# raspizeroと独自赤外線送受信回路の赤外線送受信ドライバの実装クラス
class IrRaspizero:
    def __init__(self):
        pass

    def send(self,code):
        pass

    def receive(self):
        pass

class Cmd4client:
    def __init__(self):
        pass
