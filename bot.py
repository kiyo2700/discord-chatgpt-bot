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
openai.api_key = OPENAI_API_KEY

# Discord Bot設定
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return  # Botのメッセージは無視

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message.content}]
    )

    reply = response["choices"][0]["message"]["content"]
    await message.channel.send(reply)

# Botを起動
client.run(DISCORD_BOT_TOKEN)
