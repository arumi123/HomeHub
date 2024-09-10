import openai

# OpenAI API キーを設定
openai.api_key = "your-openai-api-key"

# GPT-4に定義する関数（coolerheater.shの制御）
functions = [
    {
        "name": "control_temperature_system",
        "description": "Control the temperature system to cooler, heater, or off mode with a target temperature.",
        "parameters": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["cooler", "heater", "off"],
                    "description": "The mode of the system: cooler, heater, or off."
                },
                "temperature": {
                    "type": "integer",
                    "description": "The target temperature to set."
                }
            },
            "required": ["mode", "temperature"]
        }
    }
]

# ユーザーからのプロンプト
user_prompt = input("Enter your command (e.g., 'cooler 22', 'heater 25', 'off'): ")

# GPT-4 モデルを呼び出して function calling を行う
response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    functions=functions,
    function_call="auto"  # GPTに自動で適切な関数呼び出しをさせる
)

# 関数呼び出しの結果を取得
function_call = response['choices'][0]['message']['function_call']
print("GPT is calling the function: ", function_call['name'])
print("With arguments: ", function_call['arguments'])

# JSONの引数をパース
import json
arguments = json.loads(function_call['arguments'])

# coolerheater.sh に引数を渡して実行
import subprocess

def control_temperature_system(mode, temperature):
    try:
        result = subprocess.run(['./coolerheater.sh', mode, str(temperature)], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# GPTによって決定されたモードと温度を coolerheater.sh に送信
result = control_temperature_system(arguments['mode'], arguments['temperature'])
print(result)