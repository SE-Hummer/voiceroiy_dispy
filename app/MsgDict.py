import discord
import asyncio
import time

Msgs = {
    'MSG_ONMSG_E001' : ['VCに入ってから誘ってください'],
    'MSG_ONMSG_E002' : ['VCにいません'],
    'MSG_ONMSG_S001' : ['登場しました'],
    'MSG_ONMSG_S002' : ['speakerは0~24の中から半角数字で選べます', '_config -hで喋り手一覧を表示します'],
    'MSG_ONMSG_S003' : ['_config speaker　のコマンドを送信してください', 'speakerは0~24の中から半角数字で選べます', '_config -hで喋り手一覧を表示します'],
    'MSG_ONMSG_S004' : ['退場します']
}

async def send_msg(channel, id):
    for msg in Msgs[id]:
        #ループによるメッセージ送信は受け入れにディレイを挟む
        await channel.send(msg)
        time.sleep(0.5)
