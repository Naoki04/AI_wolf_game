import json
import random

# 新しいルームを作成した際の関数(部屋IDの発行とゲーム管理DBへの登録)
def new_room(data):
    n_mem = data["n_mem"]
    owner_id = data["owner_id"]
    # 部屋IDの発行
    room_id = random_number = random.randint(100000, 999999)
    
    ## yet: 本来はDynamoDB上でかぶりがないか確認する
    ## yet: Dynamoに新しいゲームを登録する処理
    
    # レスポンスの作成
    response = {
                'statusCode': 200,
                'body': json.dumps({
                    "room_id": room_id
                    })
                }
    return response
                

# 既存の部屋にユーザーが入室する際の処理
def join_room(data):
    room_id = data["room_id"]
    user_id = data["user_id"]
    
    # データベースに追加する処理(溢れる場合, 部屋がない場合はエラー返す)
    
    # レスポンスの作成
    response = {
                'statusCode': 200,
                }
    return response
    

def lambda_handler(event, context):
    # モード, データの抽出    
    mode = event["mode"]
    data = event["data"]
    print("mode: ", mode)
    print("data: ", data)
    
    if mode == "new_room":
        res = new_room(data)
    elif mode == "join_room":
        res = join_room(data)
    
    return res

    
