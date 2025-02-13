import discord
import openai
import os
from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

# 環境変数を取得
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI API設定
client_openai = openai.OpenAI(api_key=OPENAI_API_KEY)

# Discord Bot設定
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# ユーザーごとの会話履歴を保存する辞書
conversation_histories = {}

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Botのメッセージは無視

    user_id = str(message.author.id)

    # もしユーザーの履歴がなければ、新しく作成
    if user_id not in conversation_histories:
        conversation_histories[user_id] = []

    # 履歴を追加（最大10メッセージまで保存）
    conversation_histories[user_id].append({"role": "user", "content": message.content})
    if len(conversation_histories[user_id]) > 10:
        conversation_histories[user_id].pop(0)  # 古いメッセージを削除

    # OpenAI APIに会話履歴を送信
    response = client_openai.chat.completions.create(
        model="gpt-4",
        messages=conversation_histories[user_id]
    )

    reply = response.choices[0].message.content

    # ボットの返答も履歴に追加
    conversation_histories[user_id].append({"role": "assistant", "content": reply})
    if len(conversation_histories[user_id]) > 10:
        conversation_histories[user_id].pop(0)  # 古いメッセージを削除

    await message.channel.send(reply)

# Botを起動
client.run(DISCORD_BOT_TOKEN)
