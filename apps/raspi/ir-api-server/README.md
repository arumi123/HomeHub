# 赤外線操作APIサーバー

HomeKitアプリから接続できる赤外線操作APIサーバーです。

## 機能

- 赤外線コードの送信・記録
- デバイス（照明、エアコン）の制御
- RESTful API
- HomeKit連携対応

## アーキテクチャ

```
ir-api-server/
├── api/                    # API層
│   ├── routes/            # エンドポイント
│   └── dependencies.py    # 依存性注入
├── core/                  # ビジネスロジック層
│   ├── device_manager.py  # デバイス管理
│   └── state_manager.py   # 状態管理
├── devices/               # デバイス層
│   ├── ir_system.py      # 赤外線システム
│   └── controllers/      # デバイス制御
├── config/               # 設定管理
├── utils/               # ユーティリティ
└── main.py             # エントリーポイント
```

## 既存コードとの統合

このAPIサーバーは既存の`ir-bridge`プロジェクトのコードを活用しています：

- `irrp.py`: 赤外線送受信機能
- `devicedriver.py`: デバイス制御ロジック
- 状態管理機能

## 使用方法

### 1. 開発環境での実行

```bash
# 依存関係をインストール
pip install -r requirements.txt

# サーバーを起動
python main.py
```

### 2. Dockerでの実行

```bash
# コンテナをビルドして起動
docker-compose up --build
```

### 3. APIエンドポイント

#### デバイス操作
- `POST /devices/register/{device_id}` - デバイス登録
- `GET /devices/{device_id}/status` - デバイス状態取得
- `PUT /devices/{device_id}/status` - デバイス状態設定
- `POST /devices/{device_id}/command` - デバイスコマンド実行

#### 赤外線操作
- `POST /ir/send` - 赤外線コード送信
- `POST /ir/record` - 赤外線コード記録
- `GET /ir/codes` - 利用可能コード一覧
- `GET /ir/status` - 赤外線システム状態

#### ヘルスチェック
- `GET /health/` - 基本的なヘルスチェック
- `GET /health/detailed` - 詳細なヘルスチェック
- `GET /health/ready` - 準備完了チェック

## 設定

環境変数で設定可能：

- `IR_GPIO_PIN`: 赤外線送信GPIOピン（デフォルト: 17）
- `IR_FREQUENCY`: 赤外線周波数（デフォルト: 38.0）
- `LOG_LEVEL`: ログレベル（デフォルト: INFO）

## HomeKit連携

このAPIサーバーは既存のHomebridgeコンテナと連携して動作します：

1. HomebridgeがHomeKitからのコマンドを受信
2. HomebridgeがこのAPIサーバーにコマンドを送信
3. APIサーバーが赤外線コードを送信
4. 家電が操作される

## 開発

### テスト

```bash
# テストを実行
pytest tests/
```

### コード品質

```bash
# コードフォーマット
black .
# リント
flake8 .
```

## ライセンス

このプロジェクトは既存のHomeHubプロジェクトの一部です。 