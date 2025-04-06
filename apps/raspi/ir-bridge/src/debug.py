import module.devicedriver
import homehub.raspi.src.module.cli_controller
import module.cmd4_client
import module.gpt_client

if __name__ == "__main__":
    bulb = module.devicedriver.ClRs2()

    print("全部の値：",bulb.get_status())  # 実行したい関数だけ呼び出す
    print("特定の値：",bulb.get_status("brightness"))

    bulb.brightness(0)

    print("全部の値：",bulb.get_status())  # 実行したい関数だけ呼び出す
    print("特定の値：",bulb.get_status("brightness"))
