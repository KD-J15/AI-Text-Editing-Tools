from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

# Flaskアプリケーションの初期化
app = Flask(__name__)

# テンプレートと静的ファイルのフォルダ設定
app.template_folder = 'templates'
app.static_folder = 'static'

# .env ファイルの内容を読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# セキュリティ設定
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# リクエストレート制限の設定

# APIキーの確認
if not api_key:
    raise RuntimeError("Missing OpenAI API Key in environment variables")

client = OpenAI(api_key=api_key)

# 校正プロンプト
PRESET_PROMPTS = {
    "friend": "以下の文章を友人に送るメッセージとして、適切なカジュアルな形式に校正してください。",
    "relative": "以下の文章を親戚に送るメッセージとして、適切な丁寧な形式に校正してください。",
    "boss": "以下の文章を上司に送るメールとして、適切で礼儀正しい形式に校正してください。"
}

# 入力バリデーション関数
def validate_input(input_text, preset, recipient):
    if not input_text or len(input_text) > 1000:
        raise ValueError("Input text must be between 1 and 1000 characters.")
    if re.search(r"[<>]", input_text):
        raise ValueError("Input text contains invalid characters.")
    if preset not in PRESET_PROMPTS:
        raise ValueError("Invalid preset selected.")
    if not recipient or len(recipient) > 50:
        raise ValueError("Recipient must be a non-empty string and less than 50 characters.")

# 校正を行う関数
def proofread_text(input_text, preset, recipient):
    system_prompt = f"送信相手: {recipient}\n{PRESET_PROMPTS[preset]}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7
    )

    # 校正結果を抽出
    proofread_result = response.choices[0].message.content
    return proofread_result

# ホームページのルート
@app.route('/')
def home():
    return render_template('index.html')

# 校正エンドポイント
@app.route('/proofread', methods=['POST'])
def proofread_endpoint():
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'preset' not in data or 'recipient' not in data:
            return jsonify({"error": "Invalid input. Please provide 'text', 'preset', and 'recipient' in JSON format."}), 400

        input_text = data['text']
        preset = data['preset']
        recipient = data['recipient']

        # 入力バリデーション
        validate_input(input_text, preset, recipient)

        # 校正処理
        result = proofread_text(input_text, preset, recipient)
        return jsonify({"result": result})

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500

# エラー処理

if __name__ == "__main__":
    app.run(debug=False)
