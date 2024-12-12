from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

# .env ファイルの内容を読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# Flaskアプリの初期化
app = Flask(__name__)

client = OpenAI(api_key=api_key)

PRESET_PROMPTS = {
    "friend": "以下の文章を友人に送るメッセージとして、適切なカジュアルな形式に校正してください。",
    "relative": "以下の文章を親戚に送るメッセージとして、適切な丁寧な形式に校正してください。",
    "boss": "以下の文章を上司に送るメールとして、適切で礼儀正しい形式に校正してください。"
}

CHARACTER_LIMIT = 1000  # 字数制限

def proofread_text(input_text, preset, recipient):
    """
    校正を行うための関数
    :param input_text: 校正対象の文章
    :param preset: 使用するプロンプトのプリセット
    :param recipient: 送信相手の指定
    :return: 校正結果と修正点
    """
    if len(input_text) > CHARACTER_LIMIT:
        raise ValueError(f"Input text exceeds the character limit of {CHARACTER_LIMIT}.")

    if preset not in PRESET_PROMPTS:
        raise ValueError("Invalid preset selected.")

    system_prompt = (
        f"送信相手: {recipient}\n"
        f"{PRESET_PROMPTS[preset]}\n"
        "また、以下のように修正箇所とその理由を簡潔に説明してください:\n"
        "- 修正箇所と修正理由: 文法エラーの修正、不適切な表現の改善など。"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7
    )

    # 校正結果と修正点を抽出
    proofread_result = response.choices[0].message.content
    corrections = "修正箇所: 以下のように修正しました\n" + proofread_result
    return proofread_result, corrections

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/proofread', methods=['POST'])
def proofread_endpoint():
    """
    校正エンドポイント
    """
    data = request.get_json()
    if not data or 'text' not in data or 'preset' not in data or 'recipient' not in data:
        return jsonify({"error": "Invalid input. Please provide 'text', 'preset', and 'recipient' in JSON format."}), 400

    input_text = data['text']
    preset = data['preset']
    recipient = data['recipient']
    try:
        result, corrections = proofread_text(input_text, preset, recipient)
        return jsonify({"result": result, "corrections": corrections})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()