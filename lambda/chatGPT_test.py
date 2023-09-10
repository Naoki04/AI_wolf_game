# !pip install openai
import credentials
import openai
import yaml
import random

openai.api_key = credentials.chatgpt_secret_key

# 年齢・性別のランダム作成
# 代のリストと性別のリストを定義します
generations = ["10代前半", "10代後半", "20代前半", "20代後半", "30代", "40代", "50代", "60代",  "90代"]
genders = ["男", "女"]
# ランダムに代と性別を選択します
random_generation = random.choice(generations)
random_gender = random.choice(genders)
# 文字列を生成します
result = f"{random_generation}{random_gender}性"
print("設定:", result)


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"あなたは{result}で、友達とアイスブレイクゲームをしています。簡単なクイズに対して、簡潔に答えます。必ずしも文章で答える必要はありません。敬語は禁止で、できれば体現止めで答えてください。'答え：'などの形式も不要です。AIであると気づかれないように回答してください。です、ますは禁止です。"
        },
        
        {
            "role": "user",
            "content": "好きなタイプは"
        },
        {
            "role": "assistant",
            "content": "まじめで素直な人。"
        },
        {
            "role": "user",
            "content": "好きな食べ物は"
        },
        {
            "role": "assistant",
            "content": "寿司"
        },
        {
            "role": "user",
            "content": "身長は？"
        },
        
    ]
)

print(response['choices'][0]['message']['content'])