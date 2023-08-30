import requests
import json

# 送信するJSONデータ

# new room
data = {
    "mode": "new_room",
    "data": {
        "n_mem": 5, 
        "owner_id": "dahi11e32" 
        }
}

"""
#join room
data = {
            "mode": "join_room",
            "data": {
                "room_id": 290912,
                "user_id": "aahi11a12"
            }
        }
"""
        
# APIエンドポイント
url = ""

# JSONデータを含むPOSTリクエストを送信
response = requests.post(url, json=data)

# レスポンスを表示
print(response.status_code)  # ステータスコード
print(response.json())       # レスポンスのJSONデータ
