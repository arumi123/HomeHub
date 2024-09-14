import openai
import json
import subprocess
import os

# ローカルの環境変数からAPIを取得する
openai.api_key = os.getenv("OPENAI_API_KEY")

# APIキーが取得できなかった場合のエラーメッセージ
if openai.api_key is None:
    print("Error: API key not found in environment variables.")
    exit(1)

# GPT-4に定義する関数（HearterColler.pyの制御）
tools = [
    {
        "type": "function",
        "function": {
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
                "required": ["mode", "temperature"],
                "additionalProperties": False,
            }
        }
    }
]

# ユーザーからのプロンプト
user_prompt = input("Enter your command (e.g., 'cooler 22', 'heater 25', 'off'): ")

# GPTに、「　どのようにふるまって欲しいのか・これまでのGPTの回答・ユーザの入力　」を送る
messages = [
    {"role": "system", "content": "あなたは家電を操作してくれる人です。日本語で返答してください"},
    {"role": "user", "content": user_prompt}
]

# GPT-4 モデルを呼び出して function calling を行う
response = openai.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages = messages,
    tools=tools,
    tool_choice="auto"
)
print(response)

# 関数呼び出しの結果を取得
#function_call = response['choices'][0]['message']['function_call']
#print("GPT is calling the function: ", function_call['name'])
#print("With arguments: ", function_call['arguments'])

tool_call = response.choices[0].message.tool_calls[0]
print(tool_call)
mode = json.loads(tool_call['function']['arguments']['mode']) 
roomtemprature = json.loads(tool_call['function']['arguments']['temprature']) 
print(mode)
print(roomtemprature)
#order_id = arguments.get('order_id')

# Call the get_delivery_date function with the extracted order_id
delivery_date = get_delivery_date(order_id)

# JSONの引数をパース
arguments = json.loads(function_call['arguments'])

# HeaterCooler.py に引数を渡して実行
def control_temperature_system(mode, temperature):
    try:
        result = subprocess.run(['./HeaterCooler.py', mode, str(temperature)], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

# GPTによって決定されたモードと温度を coolerheater.sh に送信
result = control_temperature_system(arguments['mode'], arguments['temperature'])
print(result)
