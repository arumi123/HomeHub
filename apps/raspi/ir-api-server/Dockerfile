# ベースイメージとしてPython 3.11を使用
FROM python:3.11-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    pigpio \
    pigpio-tools \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 既存のirrp.pyをコピー
COPY ../ir-bridge/src/module/irrp.py ./irrp.py

# アプリケーションコードをコピー
COPY . .

# データディレクトリを作成
RUN mkdir -p data

# ポート8000を公開
EXPOSE 8000

# アプリケーションを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 