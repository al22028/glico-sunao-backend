# glico-sunao-backend

## Servers

| STAGE | Swagger                               | BASE_URL                         |
| ----- | ------------------------------------- | :------------------------------- |
| local | <http://localhost:3333/local/swagger> | <http://localhost:3333/local/v1> |

## 環境構築

- [nodenv](https://github.com/nodenv/nodenv)
- [pyenv](https://github.com/pyenv/pyenv)
- [Docker](https://www.docker.com/ja-jp/)

| Runtime | Version |
| ------- | ------- |
| Python  | 3.11.6  |
| Node    | 20.9.0  |

```bash
nodenv install 20.9.0
pyenv install 3.11.6
```

## Installation

`poetry`がインストールされていない場合

```bash
pip install poetry
poetry config virtualenvs.in-project true
```

### 依存関係のインストール

```bash
npm install
poetry install
poetry shell # 仮想環境のシェルを起動
```

## Task runnner

タスクランナーとしていくつかのスクリプトをエイリアスとして登録しています

| Runtime | Task         | Command       | Description                    |
| ------- | ------------ | ------------- | ------------------------------ |
| Python  | テスト       | `task test`   | Pytestのテストを実行します     |
| Python  | フォーマット | `task format` | black formatterを実行します    |
| Python  | リント       | `task lint`   | ruffでlintを実行します         |
| Node    | 開発         | `npm run dev` | 開発用のサーバーを立ち上げます |

## Branch

基本的には [Git-flow](https://qiita.com/KosukeSone/items/514dd24828b485c69a05 "Git-flowって何？") です

### Branch naming rule

| ブランチ名                   | 説明             | 補足 |
| ---------------------------- | ---------------- | ---- |
| main                         | 最新リリース     |      |
| dev/main                     | 開発用最新       |      |
| hotfix/{モジュール名}/{主題} |                  |      |
| sandbox/{なんでも}           | テストコードなど |      |

### Branch rule

- 作業は各最新ブランチから分岐させる
- 作業ブランチはマージ後に削除
- できるだけレビューする(誰かにしてもらう)
- ビルドやデプロイなどは別途検討

### Commit message

Please refer to the following template for the commit message.

```plaintext
🐞 バグとパフォーマンス
#🐛 :bug: バグ修正
#🚑 :ambulance: 重大なバグの修正
#🚀 :rocket: パフォーマンス改善
#💻 コードの品質とスタイル
#👍 :+1: 機能改善
#♻️ :recycle: リファクタリング
#👕 :shirt: Lintエラーの修正やコードスタイルの修正

🎨 UI/UXとデザイン
#✨ :sparkles: 新しい機能を追加
#🎨 :art: デザイン変更のみ

🛠️ 開発ツールと設定
#🚧 :construction: WIP (Work in Progress)
#⚙ :gear: config変更
#📦 :package: 新しい依存関係追加
#🆙 :up: 依存パッケージなどのアップデート

📝 ドキュメントとコメント
#📝 :memo: 文言修正
#📚 :books: ドキュメント
#💡 :bulb: 新しいアイデアやコメント追加

🛡️ セキュリティ
#👮 :op: セキュリティ関連の改善

🧪 テストとCI
#💚 :green_heart: テストやCIの修正・改善

🗂️ ファイルとフォルダ操作
#📂 :file_folder: フォルダの操作
#🚚 :truck: ファイル移動

📊 ログとトラッキング
#💢 :anger: コンフリクト
#🔊 :loud_sound: ログ追加
#🔇 :mute: ログ削除
#📈 :chart_with_upwards_trend: アナリティクスやトラッキングコード追加

💡 その他
#🧐 :monocle_face: コードのリーディングや疑問
#🍻 :beers: 書いているときに楽しかったコード
#🙈 :see_no_evil: .gitignore追加
#🛠️ :hammer_and_wrench: バグ修正や基本的な問題解決
```
