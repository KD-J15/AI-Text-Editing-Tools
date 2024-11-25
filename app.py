from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

# 環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# OpenAI APIのクライアントを作成
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/correct', methods=['POST'])
def correct():
    data = request.json
    text_to_correct = data.get("text", "")
    
    # 文章校正のためのプロンプト（統合版）
    prompt = f"""
    以下の文章について、以下の観点で校正を行い、必要に応じて修正してください。

    1. 文法エラーの指摘と修正  
    2. 不適切な表現の改善  
    3. スペルミスの修正  
    4. 論理の飛躍や整合性の欠如の指摘と修正案の提示  
    5. 読みやすさ向上のための文の構造や表現の改善  
    6. 指定されたテーマや文脈に適しているかの確認と必要な修正  

    【文章】  
    {text_to_correct}
    """

    try:
        # GPT-4oモデルを使って文章を校正
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        corrected_text = completion.choices[0].message['content']
        return jsonify({"corrected_text": corrected_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
