from enum import Enum
import discord
import asyncio
import time
from discord.player import FFmpegPCMAudio

from VoiceGenerator import VcGenerator
import ConfigSpeak
import MsgDict

channel = None
vcGenerator = VcGenerator()
vcGenerator.set_speaker(3)

class MyDisClient(discord.Client):
    #override
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #override
    # 起動時に動作する処理
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    #override
    # メッセージ受信時に動作する処理
    async def on_message(self, message):
        global vcGenerator
        global channel
        await self.wait_until_ready()
        # デバッグ情報
        print(message.content)
        # メッセージング対象者判定
        if message.author.bot:
            return
        # メッセージ内容判定
        if message.content == '_come':
            await self.cmd_come(message)
            return

        # メッセージ内容判定
        if message.content == '_bye':
            await self.cmd_bye(message)
            return

        # メッセージ内容判定
        if message.content.startswith('_config'):
            await self.cmd_config(message)
            return

        # 特別なコマンド以外は音声として再生する
        if len(self.voice_clients) > 0 and channel != None and channel == message.channel:
            print(f"{self.voice_clients}-{channel}-{message.guild.voice_client}")
            # メッセージ→音声ファイル
            vcGenerator.generate_wav(message.content)
            # 形式変換
            source = discord.FFmpegPCMAudio("output.wav")
            # 音声再生
            self.voice_clients[0].play(source)

    #comeに対する動作
    async def cmd_come(self, message):
        global channel
        if message.author.voice is None:
            #voice_channelに接続していないユーザからメッセージを受けた場合に
            #メッセージを表示する
            await MsgDict.send_msg(message.channel, 'MSG_ONMSG_E001')
        else:
            if len(self.voice_clients) == 0:
                #voice_channelに接続しているユーザからメッセージを受けた場合に
                #メッセージを表示後、voice_channelに接続する
                channel = message.channel
                await MsgDict.send_msg(message.channel, 'MSG_ONMSG_S001')
                await message.author.voice.channel.connect()
                await message.channel.send(f'{message.channel.name}を読み上げます')

    #byeに対する動作
    async def cmd_bye(self, message):
        global channel
        if message.guild.voice_client is None:
            #voice_channelに接続していない場合にメッセージを表示する
            await MsgDict.send_msg(message.channel, 'MSG_ONMSG_E002')
        else:
            #voice_channelに接続している場合にメッセージを表示後、
            #voice_channelから切断する
            channel = None
            await MsgDict.send_msg(message.channel, 'MSG_ONMSG_S004')
            await self.voice_clients[0].disconnect()

    #configに対する動作(line:_config speaker speed pitch)
    async def cmd_config(self, message):
        global vcGenerator
        arr = message.content.split(' ')
        print(arr)
        if len(arr) > 1:
            #lineが有効範囲の場合
            #1桁目をhelpかspeaker valueかを判定する
            if arr[1].isdecimal():
                vcGenerator.set_speaker(int(arr[1]))
                if vcGenerator.get_speaker() > 38 or vcGenerator.get_speaker() < 0:
                    vcGenerator.set_speaker(1)
                if vcGenerator.get_speaker() == 20:
                    vcGenerator.set_speaker(1)
                await message.channel.send(ConfigSpeak.speakers[vcGenerator.get_speaker()])
            elif arr[1] == '-h':
                for name in ConfigSpeak.speakers:
                    #ループによるメッセージ送信は受け入れにディレイを挟む
                    await message.channel.send(name)
                    time.sleep(0.5)
            else:
                await MsgDict.send_msg(message.channel, 'MSG_ONMSG_S002')
        else:
            await MsgDict.send_msg(message.channel, 'MSG_ONMSG_S003')
