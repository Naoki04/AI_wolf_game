import boto3

table_name = 'game_manager_2'

dynamodb = boto3.resource(
        "dynamodb", 
        region_name='ap-northeast-3',
        aws_access_key_id='',
        aws_secret_access_key='',
        #aws_session_token='YOUR_SESSION_TOKEN
        )

def make_game_table():
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'RoomID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'RoomID',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

def new_item():
    table = dynamodb.Table(table_name)
    table.put_item(
        Item={
            'RoomID': 219211,
            'Password': "alaksa",
            'N_mem': 4,
            'Members': ["asae", "asda"],
            'N_hacked': 1,
            'Hacked': [],
            'State': 0,
            'Created-at': '20230931-09-12-43'
        }
    )
    return  0

def main():
    # ゲーム管理テーブルの作成
    ## テーブル作成をAWSマネジメントコンソールで行うとkeyschemaがHASHにならないので, scanで条件指定した際に怒られる。
    #make_game_table()
    new_item()
    return 0


if __name__ == '__main__':
    main()
