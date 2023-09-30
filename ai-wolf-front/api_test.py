import requests
import json

# 送信するJSONデータ
data = {
    "mode": "new_room",
    "data": {
        "n_mem": 5, #ゲームに参加する人数
        "owner_id": "dahi11e32"  #オーナーのユーザー識別子
        }
}

# ターゲットのAPIエンドポイントURL
url = "https://mw2awrc6fa.execute-api.ap-northeast-3.amazonaws.com/default/ai_wolf"

# JSONデータをPOSTリクエストで送信
response = requests.post(url, json=data)

# レスポンスを確認
if response.status_code == 200:
    # レスポンスのJSONデータを取得
    response_data = response.json()
    print("成功:", response_data)
else:
    print("エラー:", response.status_code)
    print(response.text)