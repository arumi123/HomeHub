# HomeHubプロジェクト
このプロジェクトとは、賢いリモコンを作成するプロジェクトです。

## できること
- iphoneのhomeappから家電を操作できます。
- 自然言語を使って家電を操作できます。
- IoTコアを使って部屋の状況の解析をできます(未実装)

## 特徴
- ラズパイと自作で組んだ回路によって、安価にあらゆるリモコンに対応できました。
- OpenAI APIを使ったため、高い自然言語処理性能があります。
- AWS との連携をしたため、複数の部屋に増やすことにも対応するなど高い拡張性を備えています。
- IaCの考え方に基づき、teraform,dockerを使用することで、デプロイを容易にしています。

## ドキュメント
以下のリンクから、プロジェクトに関する詳細なドキュメントにアクセスできます。

- [要求仕様書](docs/requirements.md)  
  プロジェクトの要求仕様をまとめた文書です。

- [アーキテクチャドキュメント](docs/architecture.md)  
  システムの全体構造やコンポーネント間の関係を示した文書です。

- [APIリファレンス](docs/api_reference.md)  
  APIエンドポイントやその使用方法を詳述した文書です。

- [コントリビュータガイド](docs/contributing.md)  
   プロジェクトに貢献するためのガイドラインを提供した文書です。

## 使用方法(raspiのみで実現する機能を使う場合)
raspizeroに下記手順でdokcerをインストールします

必要なパッケージのインストール:
~~~bash
sudo apt update
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
~~~

Docker の GPG キーを追加:
~~~bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
~~~

リポジトリを追加:
~~~bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
~~~

Docker のインストール:
~~~bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
~~~

動作確認:
~~~bash
sudo docker run hello-world
~~~

hello-world コンテナが正しく動作すれば、Docker はインストール完了です。
出力例:
~~~bash
Hello from Docker!
This message shows that your installation appears to be working correctly.
~~~

Docker をsudo なしで使用するために、現在のユーザーを docker グループに追加。

bash
コードをコピーする
sudo usermod -aG docker $USER
変更を反映 (ログアウト & 再ログイン):

現在のターミナルを閉じて再ログインします。
確認:

bash
コードをコピーする
docker run hello-world
4. Docker Compose のインストール
最新版の Docker Compose をインストール
Compose バイナリをダウンロード:

bash
コードをコピーする
sudo curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
実行権限を付与:

bash
コードをコピーする
sudo chmod +x /usr/local/bin/docker-compose
動作確認:

bash
コードをコピーする
docker-compose --version
出力例:

plaintext
コードをコピーする
Docker Compose version v2.x.x

## 使用方法(raspi+awsを使用する機能も使う場合)
control