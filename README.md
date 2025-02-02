# 文章校正AIツール

## 概要
このツールは、AIを活用して文章を校正するための簡単なWebアプリケーションです。特定の送信相手に適した文章表現を生成することを目的としています。友人、親戚、上司といった異なる対象に応じた校正結果を簡単に得ることができます。

## 主な機能
- **送信相手に応じた校正**: "友人", "親戚", "上司"といったプリセットを利用可能。
- **わかりやすい入力欄**: 入力欄に文章を記入し、ボタンを押すだけで校正結果が表示されます。
- **校正結果のコピーと使用**: 校正された文章を簡単にコピーして利用可能。

## 使用技術
- **バックエンド**: Flaskを使用し、AIによる校正ロジックをサポート。
- **フロントエンド**: HTML, CSS, JavaScriptを用いて直感的なUIを構築。
- **生成AI API**: OpenAI GPT-4oを活用して高品質な校正結果を生成。

## 必要条件
- Python 3.12以降
- Flask
- OpenAIのAPIキー
- 必要なPythonライブラリは`requirements.txt`に記載されています。

## インストールと実行
1. リポジトリをクローンします。
   ```bash
   git clone https://github.com/KD-J15/AI-Text-Editing-Tools.git
   cd AI-Text-Editing-Tools
   ```
2. 必要なライブラリをインストールします。
   ```bash
   pip install -r requirements.txt
   ```
3. OpenAIのAPIキーを`.env`ファイルに設定します。
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
4. アプリを起動します。
   ```bash
   flask run
   ```
5. ブラウザで以下のURLを開きます。
   ```
   http://127.0.0.1:5000
   ```

## ファイル構成
```
├── app.py             # Flaskアプリケーションのメインスクリプト
├── templates
│   └── index.html     # フロントエンドのHTMLテンプレート
├── static
│   ├── css
│   │   └── styles.css # フロントエンドのスタイルシート
│   └── js
│       └── script.js  # フロントエンドのJavaScript
├── .env               # OpenAI APIキーを格納する環境ファイル
└── requirements.txt   # 必要なPythonライブラリ
```

## 使用方法
1. アプリケーションを起動し、ブラウザでアクセスします。
2. **送信相手**の欄に「友人」「親戚」「上司」などを入力します。
3. 校正したい文章を入力し、「検査」ボタンを押します。
4. 校正結果が表示されます。

## 注意事項
- OpenAIのAPIキーが必要です。
- 校正結果はAIのモデルに依存しており、完全ではない場合があります。