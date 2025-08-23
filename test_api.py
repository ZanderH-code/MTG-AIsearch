import requests
import json

# 测试API
url = "http://localhost:8000/api/search"
data = {
    "query": "地落卡组的强力终端",
    "language": "zh"
}

try:
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
except Exception as e:
    print(f"错误: {e}")

