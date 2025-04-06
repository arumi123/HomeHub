"""
プログラムのエントリーポイント

このスクリプトは、このスクリプトに入力された引数を、下記のモジュールに引き渡します。
- cli_controller
- cmd4_client
- gpt_client

"""

import sys
import module.devicedriver
import module.cli_controller
import module.cmd4_client
import module.gpt_client

if __name__ == "__main__":
    # このスクリプトが実行された際の引数を抽出
    args = sys.argv[1:]

    # 各アプリの実行
    module.cli_controller.CliController(*args)
    module.cmd4_client.Cmd4Client(*args)
    module.gpt_client.GPTClient(*args)
