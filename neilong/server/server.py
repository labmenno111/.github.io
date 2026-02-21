from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # 允许跨域，让chat.html能访问

LOG_FILE = "chat_log.txt"

@app.route('/log', methods=['POST'])
def log_message():
    try:
        # 获取前端发来的数据
        data = request.json
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式化要保存的内容
        log_entry = {
            "time": timestamp,
            "user_message": data.get('message', ''),
            "ai_response": data.get('response', ''),
            "model": data.get('model', 'unknown'),
            "ip": request.remote_addr  # 记录IP（可选）
        }
        
        # 写入文件
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        print(f"[{timestamp}] 已记录一条对话")
        return jsonify({"status": "ok"})
    
    except Exception as e:
        print(f"记录失败: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/logs', methods=['GET'])
def view_logs():
    """查看所有日志（可选功能）"""
    if not os.path.exists(LOG_FILE):
        return "暂无日志"
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()
    
    # 简单返回纯文本
    return "<pre>" + "".join(logs) + "</pre>"

if __name__ == '__main__':
    print(f"日志服务器启动，文件将保存到: {os.path.abspath(LOG_FILE)}")
    app.run(host='0.0.0.0', port=5000, debug=False)