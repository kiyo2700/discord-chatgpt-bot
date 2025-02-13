import discord
import openai
import os
from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

# 環境変数を取得
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI クライアントの設定
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Discord Bot設定（Intentを全許可）
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ ログインしました: {client.user}')

@client.event
async def on_message(message):
    print(f'📩 受信メッセージ: {message.content}')  # 受信ログ

    if message.author.bot:
        return  # Botのメッセージは無視

    # Botへのメンションのみ反応（ロールメンションは無視）
    if client.user in message.mentions:
        content = message.content.replace(f'<@{client.user.id}>', '').strip()
        print(f'🔍 メンション検出: {content}')  # メンションを確認

        if not content:
            await message.reply("はい、呼びましたか？")  # メンションだけなら簡単に返信
            return

        try:
            # OpenAIにリクエスト
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": content}]
            )

            # OpenAIの返答を取得
            reply = response.choices[0].message.content
            print(f'💬 OpenAIの返答: {reply}')  # OpenAIの返答を出力

            # 返信
            await message.reply(reply)

        except Exception as e:
            print(f'⚠️ エラー発生: {e}')  # エラーログ
            await message.reply("⚠️ エラーが発生しました。ログを確認してください。")

# Botを起動
client.run(DISCORD_BOT_TOKEN)
