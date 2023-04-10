import discord

from MyClient import MyDisClient

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'MTA5NDE5Mjc3ODM0ODYwOTY5OQ.GH4WQ4.8oNYrn18uLk4g5NuzeoLZtfka1cJHeiYEs8y8E'

# 接続に必要なオブジェクトを生成
client = MyDisClient(intents=discord.Intents.default())

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
