import json
import data_function 


# 新しいルームを作成した際の関数(部屋IDの発行し,ゲーム管理DBへの登録)
def new_room(data):
    n_mem = data["n_mem"]
    owner_id = data["owner_id"]
    
    ## yet: 本来はDynamoDB上でかぶりがないか確認し, 登録する
    room_id, game_id = data_function.add_new_game(owner_id, n_mem)
    

    # レスポンスの作成
    response = {
                'statusCode': 200,
                'body': json.dumps({
                    "room_id": room_id,
                    "game_id": game_id,
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
                'body': json.dumps({
                    "message": "successfully done"
                    })
                }
    return response
    

def lambda_handler(event, context):
    print(event)
    # モード, データの抽出(bodyは辞書型ではなくstrで来るので, 辞書型に変換する)
    body_dist = json.loads(event["body"])
    mode = body_dist["mode"]
    data = body_dist["data"]
    print("mode: ", mode)
    print("data: ", data)
    
    if mode == "new_room":
        res = new_room(data)
    elif mode == "join_room":
        res = join_room(data)
    
    return res

    
