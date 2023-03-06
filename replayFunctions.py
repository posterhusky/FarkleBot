import discord, embeds
from discord.ui import View, Button

replays = []

class Replay():
    def __init__(self, host: discord.User, channel: discord.TextChannel, sharedAccess: list, id: int, infoMsg=None,
                 saveMsg: discord.Message = None):
        self.host = host
        self.channel = channel
        self.sharedAccess = sharedAccess
        self.id = id
        self.infoMsg = infoMsg
        self.saveMsg = saveMsg

    async def uploadReplay(self, embedList, farkleCentral, regularRole, replaysChannel):
        await self.channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
        await self.channel.set_permissions(regularRole, read_messages=False, send_messages=False)
        replayQueue = []
        for i in embedList:
            replayQueue += [i]
            if len(replayQueue) >= 5:
                try:
                    await self.channel.send(embeds=replayQueue)
                except:
                    for j in replayQueue:
                        await self.channel.send(embed=j)
                replayQueue = []
        if replayQueue != []:
            await self.channel.send(embeds=replayQueue)
        btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
        btn1.callback = self.deleteReplay
        btns = View()
        btns.add_item(btn1)
        self.infoMsg = await self.channel.send(
            embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)
        await self.channel.set_permissions(self.host, read_messages=True, send_messages=True)
        for i in self.sharedAccess:
            await self.channel.set_permissions(i, read_messages=True, send_messages=False)
        self.saveMsg = await replaysChannel.send(
            f'{self.id};{self.host.id};{self.channel.id};{self.infoMsg.id};{"^".join([str(i.id) for i in self.sharedAccess])}')

    async def deleteReplay(self, interaction: discord.Interaction):
        if interaction.user != self.host:
            await interaction.response.send_message(embed=embeds.getNoReplayRightsEmbed(), ephemeral=True)
            return
        btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
        btn1.callback = self.deleteReplayConfirm
        btns = View()
        btns.add_item(btn1)
        await interaction.response.send_message(embed=embeds.getReplayDeleteConfirmEmbed(), view=btns, ephemeral=True)

    async def deleteReplayConfirm(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.saveMsg.delete()
        await self.channel.delete()
        replays.remove(self)
        return

    async def addMember(self, user: discord.user):
        if user not in self.sharedAccess:
            await self.channel.set_permissions(user, read_messages=True, send_messages=False)
            self.sharedAccess += [user]
            await self.saveMsg.edit(
                content=f'{self.id};{self.host.id};{self.channel.id};{self.infoMsg.id};{"^".join([str(i.id) for i in self.sharedAccess])}')
            btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
            btn1.callback = self.deleteReplay
            btns = View()
            btns.add_item(btn1)
            await self.infoMsg.edit(
                embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)

    async def removeMember(self, user: discord.user):
        if user in self.sharedAccess:
            await self.channel.set_permissions(user, read_messages=False, send_messages=False)
            self.sharedAccess.remove(user)
            await self.saveMsg.edit(
                content=f'{self.id};{self.host.id};{self.channel.id};{self.infoMsg.id};{"^".join([str(i.id) for i in self.sharedAccess])}')
            btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
            btn1.callback = self.deleteReplay
            btns = View()
            btns.add_item(btn1)
            await self.infoMsg.edit(
                embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)

async def readReplayData(replaysChannel, farkleCentral):
    global replays
    replays = []
    messages = await replaysChannel.history(limit=500).flatten()
    for i in messages:
        rawData = i.content.split(';')
        temp = Replay(
            host=discord.utils.get(farkleCentral.members, id=int(rawData[1])),
            channel=discord.utils.get(farkleCentral.channels, id=int(rawData[2])),
            sharedAccess=[discord.utils.get(farkleCentral.members, id=int(i)) for i in rawData[4].split('^')],
            id=int(rawData[0]),
            infoMsg=None,
            saveMsg=i
        )
        temp.infoMsg = await temp.channel.fetch_message(rawData[3])
        replays += [temp]
        btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
        btn1.callback = temp.deleteReplay
        btns = View()
        btns.add_item(btn1)
        await temp.infoMsg.edit(embed=embeds.getReplayInfoEmbed(host=temp.host, shared=temp.sharedAccess, id=temp.id),
                                view=btns)