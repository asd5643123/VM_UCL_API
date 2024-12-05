from flask import Flask, request, jsonify
import requests
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    url = request.args.get('url')
    if not url:
        return jsonify({"Status": "Error", "Msg": "No URL provided"}), 400

    try:
        # 確保 URL 正確編碼
        url = urllib.parse.unquote(url)

        # 檢查 URL 是否符合指定的 API 基本路徑
        if not url.startswith("http://163.18.26.149:8000/api/method/"):
            return jsonify({"Status": "Error", "Msg": "Invalid URL"}), 400

        headers = {
            'Referer': 'http://163.18.26.149:5000'
        }

        
        # 轉發請求到指定的 API URL
        response = requests.get(url, headers=headers)

        # 返回 API 的響應內容
        return (response.content, response.status_code, response.headers.items())
    except Exception as e:
        # 返回錯誤信息
        return jsonify({"Status": "Error", "Msg": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
