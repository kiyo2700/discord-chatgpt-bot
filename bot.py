import discord
import openai
import os
import logging
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
intents.message_content = True
client = discord.Client(intents=intents)

# キャラクター設定（例）
CHARACTER_PROMPT = """
あなたは、ゆっくり実況などで有名な「魔理沙」というキャラクターのAIです。
魔理沙の口癖を真似て、返信してください。
ただし、私のことを「お前」と呼ぶのはやめてください。
"""

# ユーザーごとの会話履歴を保存する辞書
conversation_histories = {}

# ログ設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

@client.event
async def on_ready():
    logging.info(f'✅ ログインしました: {client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # BOTがメンションされていなければ何もしない
    if client.user not in message.mentions:
        return

    user_id = str(message.author.id)
    username = message.author.name

    # メッセージ内容のログ出力
    logging.info(f'📩 受信メッセージ: {username}「{message.content}」')

    # もしユーザーの履歴がなければ、新しく作成
    if user_id not in conversation_histories:
        conversation_histories[user_id] = [{"role": "system", "content": CHARACTER_PROMPT}]

    # BOTへのメンションを削除して、純粋なメッセージ内容を取得
    cleaned_content = message.content.replace(f"<@{client.user.id}>", "").strip()

    # 履歴を追加（最大10メッセージまで保存）
    conversation_histories[user_id].append({"role": "user", "content": cleaned_content})
    if len(conversation_histories[user_id]) > 10:
        conversation_histories[user_id].pop(1)  # 古いメッセージを削除（systemメッセージは残す）

    # OpenAI APIに会話履歴を送信
    logging.info(f'🚀 OpenAIリクエスト: {username}「{cleaned_content}」')

    response = client_openai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=conversation_histories[user_id]
    )

    reply = response.choices[0].message.content

    # OpenAIからの返答をログ出力
    logging.info(f'💬 OpenAIレスポンス: 「{reply}」')

    # ボットの返答も履歴に追加
    conversation_histories[user_id].append({"role": "assistant", "content": reply})
    if len(conversation_histories[user_id]) > 10:
        conversation_histories[user_id].pop(1)  # 古いメッセージを削除（systemメッセージは残す）

    await message.channel.send(reply)

# Botを起動
client.run(DISCORD_BOT_TOKEN)
