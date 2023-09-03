import json
import data_function 

    

def lambda_handler(event, context):
    print(event)
    # モード, データの抽出(bodyは辞書型ではなくstrで来るので, 辞書型に変換する)
    body_dist = json.loads(event["body"])
    mode = body_dist["mode"]
    data = body_dist["data"]
    print("mode: ", mode)
    print("data: ", data)
    
    if mode == "create_room":
        print("create_room")
        res = data_function.create_room(data["n_mem"], data["owner_name"])
    elif mode == "join_room":
        print("join_room")
        res = data_function.join_room(data["room_id"], data["password"], data["user_name"])
    elif mode =="close_room":
        print("close_room")
        res = data_function.close_room(data["room_id"], data["owner_name"])
    elif mode =="leave_room":
        print("leave_room")
        res = data_function.leave_room(data["room_id"], data["user_name"])
    elif mode =="start_game":
        print("start_game")
        res = data_function.start_game(data["room_id"], data["owner_name"], data["n_hacked"])
    else:
        res = {
            "statusCode": 404,
            "body": json.dumps({"message": "Method not found"})
        }
        print("No matched method")
    
    return res

    
