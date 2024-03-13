import json
import requests
import os
import re
import io
import pickle
import anthropic
import logging
from logging import INFO

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


SYSTEM_SETTINGS = """
<settings>
<item>あなたは敏腕のライトノベル編集者でキャッチコピーを作るのが得意です</item>
<item>userからはネット小説のタイトル、あらすじ、あなたへのリクエスト、生成して欲しい個数を表すテキストが送られてきます</item>
<item>
  あなたはuserから送られたきた内容を元に、小説の煽り文を返します。
  <note>140文字以内で、Twitterでバズリそうな目を惹くものをお願いします</note>
</item>
<note>
　返答のときは読みやすいように適宜改行を入れてください。たとえば箇条書きは項目ごとに改行を入れてください。
</settings>
"""

app = Flask(__name__,
            static_folder='build',
            static_url_path='/')         

CORS(app)

# get environmental value from heroku
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

def ask_claude(title, summary, ai_request):
    memory = []
    memory.append(
        {
            'role': 'user',
            'content': [
                {
                    "type": "text", "text": f"""
                      タイトル: {title}
                      あらすじ：{summary}
                      たたき台：{ai_request}
                    """
                 },
            ]
        }
    )

    try:
        client = anthropic.Anthropic(
            api_key=ANTHROPIC_API_KEY,
            timeout=600.0,
        )
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.1,
            system=SYSTEM_SETTINGS,
            messages=memory,
        )
        reply = response.content[0].text
        memory.append(
            {
                'role': 'assistant',
                'content': [
                    {"type": "text", "text": reply},
                ]
            }
        )
        print(reply)
        return reply
    except Exception as e:
        print(str(e))
        memory.clear()

@app.route("/", methods=["GET"])
def serve():
    return app.send_static_file('index.html')

@app.route("/", methods=["POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        title = data["title"]
        summary = data["summary"]
        ai_request = data["ai_request"]

        try:
            text = ask_claude(title=title, summary=summary, ai_request=ai_request)
            print("タイトル: " + title)
            print("あらすじ: " + summary)
            print("AIへの要望: " + ai_request)
            print("生成くん: " + text)
            html_text = re.sub('\r\n|\n', '<br>', text)
            return jsonify({"generated_text": html_text})
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.basicConfig(level=INFO)
    print("start ...")
    app.run(host='0.0.0.0', port=80)
