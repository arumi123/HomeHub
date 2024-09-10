import sys

# コマンドライン引数の取得
arg1 = sys.argv[1] if len(sys.argv) > 1 else None
arg2 = sys.argv[2] if len(sys.argv) > 2 else None

# 引数を出力
print(f"First argument: {arg1}")
print(f"Second argument: {arg2}")
