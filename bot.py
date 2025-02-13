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
intents.message_content = True  # メッセージの内容を取得するために追加
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    print(f'📩 受信メッセージ: {message.content}')
    if message.author.bot:
        return  # Botのメッセージは無視

    # メンションされているか確認
    if client.user in message.mentions:
        # メンション部分を削除（@BotName を除いたテキストのみ取得）
        content = message.content.replace(f'<@{client.user.id}>', '').strip()
        print(f'🔍 メンション検出: {content}')

        try:

            # OpenAIにリクエスト
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": content}]
            )

            # OpenAIの返答を取得
            reply = response["choices"][0]["message"]["content"]
            print(f'💬 OpenAIの返答: {reply}')

            # 返信
            await message.reply(reply)

        except Exception as e:
            print(f'⚠️ エラー発生: {e}')  # ← エラー内容を出力
            await message.reply("⚠️ エラーが発生しました。ログを確認してください。")
# Botを起動
client.run(DISCORD_BOT_TOKEN)
