import discord
import random
import embeds
import asyncio
import idList
from discord.ui import View, Button

bot = discord.Bot(intents=discord.Intents().all())
farkleCentral, regularRole, adminRole, gamesCategory, replaysCategory, qDisplayChannel, qChannel, qMessage, prefChannel, pref1Msg, pref2Msg, pref3Msg, annPingRole, qPingRole, savesChannel, totalGamesMsg, replaysChannel, *_ = [None]*50

totalGames = 0
currentGames = []
queue = []
replays = []

dice = '<:die1:1073714606813483071> <:die2:1073714605051887739> <:die3:1073714602350743692> <:die4:1073714600924692552> <:die5:1073714599691550880> <:die6:1073714597359521822>'.split()

class Replay():
    def __init__(self, host: discord.User, channel: discord.TextChannel, sharedAccess: list, id: int, infoMsg = None, saveMsg: discord.Message = None):
        self.host = host
        self.channel = channel
        self.sharedAccess = sharedAccess
        self.id = id
        self.infoMsg = infoMsg
        self.saveMsg = saveMsg

    async def uploadReplay(self, embedList):
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
        self.infoMsg = await self.channel.send(embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)
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
            await self.saveMsg.edit(content=f'{self.id};{self.host.id};{self.channel.id};{self.infoMsg.id};{"^".join([str(i.id) for i in self.sharedAccess])}')
            btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
            btn1.callback = self.deleteReplay
            btns = View()
            btns.add_item(btn1)
            await self.infoMsg.edit(embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)

    async def removeMember(self, user: discord.user):
        if user in self.sharedAccess:
            await self.channel.set_permissions(user, read_messages=False, send_messages=False)
            self.sharedAccess.remove(user)
            await self.saveMsg.edit(content=f'{self.id};{self.host.id};{self.channel.id};{self.infoMsg.id};{"^".join([str(i.id) for i in self.sharedAccess])}')
            btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
            btn1.callback = self.deleteReplay
            btns = View()
            btns.add_item(btn1)
            await self.infoMsg.edit(embed=embeds.getReplayInfoEmbed(host=self.host, shared=self.sharedAccess, id=self.id), view=btns)


async def readReplayData():
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
            infoMsg= None,
            saveMsg= i
        )
        temp.infoMsg = await temp.channel.fetch_message(rawData[3])
        replays += [temp]
        btn1 = Button(label='Delete replay', emoji='🗑', style=discord.ButtonStyle.red)
        btn1.callback = temp.deleteReplay
        btns = View()
        btns.add_item(btn1)
        await temp.infoMsg.edit(embed=embeds.getReplayInfoEmbed(host=temp.host, shared=temp.sharedAccess, id=temp.id), view=btns)



class QueuedPerson():
    def __init__(self, user: discord.user):
        self.user = user
        self.task = asyncio.create_task(kickQueuedMember(self.user))


class FarkleGame():
    def __init__(self, id: int, state: int, players: tuple, channel: discord.TextChannel, latestMsg: discord.Message):
        self.id = id
        self.state = state
        self.players = players
        self.channel = channel
        self.turn = 0
        self.bank = [0, 0, 0]
        self.msgCount = 0
        self.tableDice = [0]*6
        self.invDice = []
        self.latestMsg = latestMsg
        self.task = None
        self.melds = []
        self.latestEmbed = None
        self.embedList = []
        self.multiplier = 1.0
        self.turnsQty = 0
        self.lead = None
        self.hurryUpMsg = None
        self.turnHistory = []
        self.highStakesPass = None
        print('created game: ', players)

    async def saveReplay(self, interaction: discord.Interaction):
        global replays
        await interaction.response.send_message(embed=embeds.getReplaySavedEmbed(), ephemeral=True)
        temp = Replay(sharedAccess=[self.players[1] if interaction.user == self.players[0] else self.players[0]], host=interaction.user,
                      channel=await farkleCentral.create_text_channel(name=f'replay-{self.id}', category=replaysCategory),
                      id=self.id, infoMsg= None)
        replays += [temp]
        await temp.uploadReplay(embedList=self.embedList)


    async def terminateGame(self, delay):
        self.state = 2
        btn = Button(label='Save replay', emoji='💿', style=discord.ButtonStyle.blurple, disabled=False)
        btn.callback = self.saveReplay
        btns = View()
        btns.add_item(btn)
        self.latestEmbed = embeds.getReplayEmbed()
        self.latestMsg = await self.channel.send(embed=self.latestEmbed, view=btns)
        await asyncio.sleep(15)
        await self.channel.delete()
        while self in currentGames:
            currentGames.remove(self)

    def isBot(self) -> bool:
        return self.turn == 1 and self.players[1] == bot.user

    def getTurnRecap(self) -> list:
        return embeds.getTurnRecap(destUsr=self.players[self.turn], p1Bank=self.bank[0], p2Bank=self.bank[1],
                            turnBank=self.bank[2], qty=self.turnsQty, pNum=self.turn, history=self.turnHistory)

    async def startTurn(self):
        if abs(self.bank[0] - self.bank[1]) >= 1500:
            self.lead = 0 if self.bank[0] > self.bank[1] else 1
        else:
            self.lead = -1
        self.turnHistory = []
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        if self.turnsQty % 5 == 0:
            self.multiplier = int(self.multiplier*10 + 2)/10
            self.embedList += [embeds.getMultiplierIncrEmbed(multiplier=self.multiplier, turns=self.turnsQty)]
            await self.channel.send(embed=self.embedList[-1])
            await asyncio.sleep(1)
        btns = View()
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        if self.isBot():
            btns.add_item(btn3)
        else:
            btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
            btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=True)
            btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
            btn4.callback = self.extendIdleTimeout
            btn1.callback = self.rollDice
            if self.highStakesPass != None:
                btn5 = Button(label='High stakes', emoji='🔥', style=discord.ButtonStyle.blurple, disabled=False)
                btn5.callback = self.highStakes
                btns.add_item(btn5)
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getStartTurnEmbed(mlt=self.multiplier, lead=self.turn==self.lead, pNum=self.turn, stake=self.highStakesPass)
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            if self.highStakesPass != None and self.highStakesPass[0]*random.randint(1,3) >= 500 and random.randint(0, 7) <= len(self.highStakesPass[1]):
                print('high stakes', self.highStakesPass)
                self.bank[2] = self.highStakesPass[0]
                self.tableDice = self.highStakesPass[1]
                self.invDice = self.highStakesPass[2]
                btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
                btn3.callback = self.giveUp
                btns = View()
                btns.add_item(btn3)
                self.latestEmbed = embeds.getHighStakesEmbed(mlt=self.multiplier,
                                                             iconList=[dice[i] for i in self.tableDice],
                                                             iconList2=[dice[i] for i in self.invDice],
                                                             pts=self.highStakesPass[0], lead=1 == self.lead,
                                                             pNum=1)
                self.turnHistory += [('High stakes!', f'*{self.highStakesPass[0]} pts.*')]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
                await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())

    async def highStakes(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[2] = self.highStakesPass[0]
        self.tableDice = self.highStakesPass[1]
        self.invDice = self.highStakesPass[2]
        btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
        btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=True)
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.extendIdleTimeout
        btn1.callback = self.rollDice
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn1)
        btns.add_item(btn2)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.latestEmbed = embeds.getHighStakesEmbed(mlt=self.multiplier, iconList=[dice[i] for i in self.tableDice], iconList2=[dice[i] for i in self.invDice], pts=self.highStakesPass[0], lead=self.turn==self.lead, pNum=self.turn)
        self.turnHistory += [('High stakes!', f'*{self.highStakesPass[0]} pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        self.task = asyncio.create_task(self.cancelIdleUser())

    async def giveUp(self, interaction: discord.Interaction):
        btn = Button(emoji='🏳', label='Give up', style=discord.ButtonStyle.red)
        btn.callback = self.giveUpConfirmed
        await interaction.response.send_message(embed=embeds.getGiveUpConfirmEmbed(), view=View(btn), ephemeral=True)

    async def giveUpConfirmed(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.state == 2:
            return
        self.task.cancel()
        self.embedList += self.getTurnRecap()
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += [embeds.getGiveUpEmbed(user=interaction.user, pNum= int(interaction.user == self.players[1]))]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(30)

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[self.turn] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user==self.players[1])
        self.turnHistory += [('Score banked:', str(self.bank[2]) + ' pts.')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] >= 10000:
            self.embedList += [
                embeds.getWinEmbed(winner=self.players[self.turn], pNum=self.turn, turns=self.turnsQty)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(45)
            return
        self.highStakesPass = None
        self.turn += 1
        self.turn %= 2
        await self.startTurn()

    async def extendIdleTimeout(self, interaction: discord.Interaction):
        self.task.cancel()
        self.task = asyncio.create_task(self.cancelIdleUser())
        await interaction.response.send_message(embed=embeds.getIdleTimeoutExtendedEmbed(), ephemeral=True)

    async def cancelIdleUser(self):
        if self.hurryUpMsg != None:
            await self.hurryUpMsg.delete()
        self.hurryUpMsg = None
        try:
            await asyncio.sleep(45)
        except asyncio.CancelledError:
            return
        self.hurryUpMsg = await self.channel.send(embed=embeds.getHurryUpEmbed(self.players[self.turn]))
        temp = await self.channel.send(f'{self.players[self.turn].mention}')
        await temp.delete()
        try:
            await asyncio.sleep(15)
        except asyncio.CancelledError:
            return
        self.embedList += self.getTurnRecap()
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += [embeds.getInteractionTimeoutEmbed(user=self.players[self.turn])]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(30)

    async def botRollDice(self): # bot action ========================================================
        if self.turn == 0:
            return
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0]:
            if self.turn == 0:
                return
            btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
            btn3.callback = self.giveUp
            btns = View()
            btns.add_item(btn3)
            self.bank[2] += result[1] # bot action ===================================================
            self.latestEmbed = embeds.getHotDiceEmbed(iconList=[dice[i] for i in self.tableDice], pts=result[1], mlt=self.multiplier, lead=self.lead==1, pNum=1)
            self.turnHistory += [('Rolled hot dice:', ' '.join([dice[i] for i in self.tableDice]) + f' *- {result[1]}*')]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
            self.tableDice = [0] * 6
            self.invDice = []
            await asyncio.sleep(1.5)
            await self.botRollDice()
        if self.melds == []:
            if self.turn == 0:
                return
            if self.highStakesPass == None or len(self.turnHistory) > 2:
                self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=1, iconList=[dice[i] for i in self.tableDice])
                self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
                if self.highStakesPass == None:
                    self.highStakesPass = (self.bank[2] if self.bank[2] > 1000 else 1000, self.tableDice, self.invDice)
                else:
                    self.highStakesPass = None
            else:
                self.latestEmbed = embeds.getFailedHighStakeEmbed(turnBank=self.bank[2], pNum=1,
                                                          iconList=[dice[i] for i in self.tableDice], pts=self.highStakesPass[0])
                self.turnHistory += [('High stakes failed:', ' '.join([dice[i] for i in self.tableDice]))]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
                self.bank[1] = self.bank[1] - 500*self.multiplier if self.bank[1] > 500 else 0
                self.highStakesPass = None
            for n, i in enumerate(self.embedList):
                if i == None:
                    self.embedList[n] = self.getTurnRecap()
                    break
            await asyncio.sleep(2)
            await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
            self.turn = 0
            await self.startTurn()
            return
        if self.turn == 0:
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn3)
        self.latestEmbed = embeds.getAfterRollEmbed(iconList=[dice[i] for i in self.tableDice], iconList2=[dice[i] for i in self.invDice], mlt=self.multiplier, lead=1==self.lead, pNum=1)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        await self.botMeldItem(self.melds[0])

    async def botMeldItem(self, meld):
        if self.turn == 0:
            return
        self.bank[2] += meld[2]
        for _ in range(meld[1]):
            self.tableDice.remove(meld[0])
            self.invDice += [meld[0]]
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        self.getMelds()
        btns.add_item(btn3)
        self.latestEmbed = embeds.getAfterMeldEmbed(iconList=[dice[i] for i in self.tableDice],
                                                         iconList2=[dice[i] for i in self.invDice], meld=meld,
                                                         mlt=self.multiplier,
                                                         lead=1 == self.lead, pNum=1)
        self.turnHistory += [('Melded dice:', f'{meld[3]} × {meld[1]} *- {meld[2]}*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        if self.turn == 0:
            return
        if self.bank[1] + self.bank[2] >= 10000:
            await self.botBankScore()
            return
        if self.melds != []:
            await self.botMeldItem(self.melds[0])
            return
        if random.randint(0, 7) <= len(self.tableDice)+1:
            if self.highStakesPass != 0 and random.randint(0, 2) == 0:
                await self.botBankScore()
                return
            await self.botRollDice()
            return
        await self.botBankScore()

    async def botBankScore(self):
        self.bank[1] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=True)
        self.turnHistory += [('Score banked:', str(self.bank[2]) + ' pts.')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[1] >= 10000:
            self.embedList += [
                embeds.getWinEmbed(winner=self.players[1], pNum=1, turns=self.turnsQty)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(45)
            return
        self.highStakesPass = None
        self.turn = 0
        await self.startTurn()

    async def rollDice(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0]:
            btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
            btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=False)
            btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
            btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
            btn4.callback = self.extendIdleTimeout
            btn1.callback = self.rollDice
            btn2.callback = self.bankScore
            btn3.callback = self.giveUp
            btns = View()
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
            self.bank[2] += result[1]
            self.latestEmbed = embeds.getHotDiceEmbed(iconList=[dice[i] for i in self.tableDice], pts=result[1], mlt=self.multiplier, lead=self.turn==self.lead, pNum=self.turn)
            self.turnHistory += [('Rolled hot dice:', ' '.join([dice[i] for i in self.tableDice]) + f' *- {result[1]}*')]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
            self.tableDice = [0] * 6
            self.invDice = []
            self.task = asyncio.create_task(self.cancelIdleUser())
            return
        if self.melds == []:
            if self.highStakesPass == None or len(self.turnHistory) != 1:
                self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn, iconList=[dice[i] for i in self.tableDice])
                self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
                if self.highStakesPass == None:
                    self.highStakesPass = (self.bank[2] if self.bank[2] > 1000 else 1000, self.tableDice, self.invDice)
                else:
                    self.highStakesPass = None
            else:
                self.latestEmbed = embeds.getFailedHighStakeEmbed(turnBank=self.bank[2], pNum=self.turn,
                                                          iconList=[dice[i] for i in self.tableDice], pts=self.highStakesPass[0])
                self.turnHistory += [('High stakes failed:', ' '.join([dice[i] for i in self.tableDice]) + f" (*{self.highStakesPass[0]} pts.* lost)")]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
                self.bank[self.turn] -= self.highStakesPass[0]
                if self.bank[self.turn] < 0:
                    self.bank[self.turn] = 0
                self.highStakesPass = None
            for n, i in enumerate(self.embedList):
                if i == None:
                    self.embedList[n] = self.getTurnRecap()
                    break
            await asyncio.sleep(2)
            await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
            self.turn += 1
            self.turn %= 2
            await self.startTurn()
            return
        btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=True)
        btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=self.invDice==[])
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.extendIdleTimeout
        btn2.callback = self.bankScore
        btn3.callback = self.giveUp
        btns = View()
        for i in self.melds:
            temp = MeldButton(game=self, meld=i, priority=i[2]==self.melds[0][2])
            btns.add_item(temp)
        btns.add_item(btn1)
        btns.add_item(btn2)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.latestEmbed = embeds.getAfterRollEmbed(iconList=[dice[i] for i in self.tableDice], iconList2=[dice[i] for i in self.invDice], mlt=self.multiplier, lead=self.turn==self.lead, pNum=self.turn)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        self.task = asyncio.create_task(self.cancelIdleUser())

    def getMelds(self):
        multiplier = 1 if self.turn == self.lead else self.multiplier
        amount = len(self.tableDice)
        sorted_nums = self.tableDice.copy()
        sorted_nums.sort()
        perfectTable = sorted_nums.copy() # tests the possibility of hot dice by removing meldable dice
        perfectScore = 0 # score in case of hot dice
        self.melds = [] # die id, amount, pts, emoji
        for i in range(6):
            if self.tableDice.count(i) == 6:
                return (True, int(3000*multiplier))
        if sorted_nums == list(range(6)):
            return (True, int(2500*multiplier))
        for i in range(6):
            if self.tableDice.count(i) >= 5:
                self.melds += [(i, 5, int(2000*multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int(2000*multiplier)
        if amount == 6 and sorted_nums[0] == sorted_nums[1] and sorted_nums[2] == sorted_nums[3] and sorted_nums[4] == sorted_nums[5]:
            return (True, int(1500*multiplier))
        if self.tableDice.count(0) >= 3:
            self.melds += [(0, 3, int(1000*multiplier), dice[0])]
            if 0 in perfectTable:
                while 0 in perfectTable:
                    perfectTable.remove(0)
                perfectScore += int(1100*multiplier) if self.tableDice.count(0) == 4 else int(1000*multiplier)
        for i in range(6):
            if self.tableDice.count(i) >= 4:
                self.melds += [(i, 4, int(1000*multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int(1000*multiplier)
        for i in range(1, 6):
            if self.tableDice.count(i) >= 3:
                self.melds += [(i, 3, int((i+1)*100*multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int((i+1)*100*multiplier)
        if 0 in self.tableDice:
            self.melds += [(0, 1, int(100*multiplier), dice[0])]
            perfectScore += perfectTable.count(0) * int(100*multiplier)
            while 0 in perfectTable:
                perfectTable.remove(0)
        if 4 in self.tableDice:
            self.melds += [(4, 1, int(50*multiplier), dice[4])]
            perfectScore += perfectTable.count(4) * int(50*multiplier)
            while 4 in perfectTable:
                perfectTable.remove(4)

        if perfectTable == []:
            self.melds = []
            return (True, perfectScore)
        else:
            return (False, 0)



class MeldButton(Button):
    def __init__(self, game: FarkleGame, meld, priority: bool):
        super().__init__(label=f'× {meld[1]} - {meld[2]}pts.', emoji=meld[3], style=discord.ButtonStyle.blurple if priority else discord.ButtonStyle.grey)
        self.game = game
        self.meld = meld

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.game.players[self.game.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.game.task.cancel()
        await interaction.response.defer()
        self.game.bank[2] += self.meld[2]
        self.game.melds.remove(self.meld)
        for _ in range(self.meld[1]):
            self.game.tableDice.remove(self.meld[0])
            self.game.invDice += [self.meld[0]]
        btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
        btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=self.game.invDice == [])
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.game.extendIdleTimeout
        btn1.callback = self.game.rollDice
        btn2.callback = self.game.bankScore
        btn3.callback = self.game.giveUp
        btns = View()
        self.game.getMelds()
        for i in self.game.melds:
            temp = MeldButton(game=self.game, meld=i, priority=i[2] == self.game.melds[0][2])
            btns.add_item(temp)
        btns.add_item(btn1)
        btns.add_item(btn2)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.game.latestEmbed = embeds.getAfterMeldEmbed(iconList=[dice[i] for i in self.game.tableDice], iconList2=[dice[i] for i in self.game.invDice], meld=self.meld, mlt=self.game.multiplier, lead=self.game.turn==self.game.lead, pNum=self.game.turn)
        self.game.turnHistory += [('Melded dice:', f'{self.meld[3]} × {self.meld[1]} *- {self.meld[2]}*')]
        await self.game.latestMsg.edit(embeds=self.game.getTurnRecap() + [self.game.latestEmbed], view=btns)
        self.game.task = asyncio.create_task(self.game.cancelIdleUser())

#
#=== === === === === === === === === === === === === === === === === === ===
#
# EVENTS
#
#=== === === === === === === === === === === === === === === === === === ===
#
#=== === === === === === === === === === === === === === === === === === ===
#
#=== === === === === === === === === === === === === === === === === === ===
#

@bot.event
async def on_ready():
    global farkleCentral, regularRole,adminRole, gamesCategory, replaysCategory, totalGames, qDisplayChannel, qChannel, qMessage, prefChannel, pref1Msg, pref2Msg, pref3Msg, annPingRole, qPingRole, savesChannel, totalGamesMsg, replaysChannel
    print(f'Logged on as {bot.user}!')
    farkleCentral = discord.utils.get(bot.guilds, id=idList.farkleCentralId)
    regularRole = discord.Guild.get_role(farkleCentral, idList.regularRole)
    annPingRole = discord.Guild.get_role(farkleCentral, idList.annPingRole)
    qPingRole = discord.Guild.get_role(farkleCentral, idList.qPingRole)
    adminRole = discord.Guild.get_role(farkleCentral, idList.adminRole)
    gamesCategory = discord.utils.get(farkleCentral.categories, id=idList.gamesCategory)
    replaysCategory = discord.utils.get(farkleCentral.categories, id=idList.replaysCategory)
    qDisplayChannel = discord.utils.get(farkleCentral.channels, id=idList.qDisplayChannel)
    qChannel = discord.utils.get(farkleCentral.channels, id=idList.qChannel)
    prefChannel = discord.utils.get(farkleCentral.channels, id=idList.prefChannel)
    savesChannel = discord.utils.get(farkleCentral.channels, id=idList.savesChannel)
    await qDisplayChannel.edit(name=f'Queued members: {len(queue)}')
    qMessage = await qChannel.fetch_message(idList.queueMsg)
    pref1Msg = await prefChannel.fetch_message(idList.pref1Msg)
    pref2Msg = await prefChannel.fetch_message(idList.pref2Msg)
    pref3Msg = await prefChannel.fetch_message(idList.pref3Msg)
    totalGamesMsg = await savesChannel.fetch_message(idList.totalGamesMsg)
    replaysChannel = discord.utils.get(farkleCentral.channels, id=idList.replayChannel)
    print(totalGamesMsg.content)
    totalGames = int(totalGamesMsg.content)
    await readReplayData()
    print(replays)


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if adminRole in message.author.roles:
        if message.content == '$gamerules':
            await message.channel.send(embeds=embeds.getGameRuleEmbeds())
        elif message.content == '$servrules':
            await message.channel.send(embed=embeds.getServerRuleEmbeds())
        elif message.content == '$save1':
            await message.channel.send(f'{totalGames}')
        elif message.content == '$newgameinfo':
            i = await message.channel.send(embeds=embeds.getNewGameEmbeds(bot.user))
            await i.add_reaction('🇶')
        elif message.content == '$pref1':
            i = await message.channel.send(embed=embeds.getBlockInvitesEmbed())
            await i.add_reaction('✅')
        elif message.content == '$pref2':
            i = await message.channel.send(embed=embeds.getAnnouncementPingEmbed())
            await i.add_reaction('✅')
        elif message.content == '$pref3':
            i = await message.channel.send(embed=embeds.getQueuePingEmbed())
            await i.add_reaction('✅')
        elif message.content == '$stopbot':
            await bot.close()

    for i in currentGames:
        if i.channel == message.channel:
            i.embedList += [embeds.getUsrReplayMsgEmbed(message=message.content, user=message.author, pNum=message.author==i.players[0])]

    if message.channel.id == idList.newGameChannel:
        await message.delete()
        return

    for i in replays:
        if i.channel == message.channel:
            await message.delete()
            return

@bot.event
async def on_member_join(member):
    await member.add_roles(regularRole)

@bot.event
async def on_raw_reaction_add(payload):
    global queue, pref2Msg
    farkleCentral = bot.guilds[0]
    channel = discord.utils.get(farkleCentral.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if str(payload.emoji) == '✅':
        if channel == prefChannel:
            if payload.message_id == idList.pref2Msg:
                await payload.member.add_roles(annPingRole)
            elif payload.message_id == idList.pref3Msg:
                await payload.member.add_roles(qPingRole)
            return
        for i in currentGames:
            if i.channel.id == payload.channel_id and i.state == 0:
                users = []
                async for user in message.reactions[0].users():
                    users += [user]
                if i.players[0] in users and i.players[1] in users:
                    i.task.cancel()
                    await message.clear_reactions()
                    i.state = 1
                    i.turn = random.randint(0, 1)
                    await channel.set_permissions(i.players[0], read_messages=True, send_messages=True)
                    await channel.set_permissions(i.players[1], read_messages=True, send_messages=True)
                    i.embedList += [embeds.getBothReadyEmbed(i.players[i.turn], *i.players)]
                    await channel.send(embed=i.embedList[-1])
                    await i.startTurn()
                break
    elif str(payload.emoji) == '🇶' and payload.channel_id == idList.newGameChannel:
        for i in currentGames:
            if payload.member in i.players:
                await message.remove_reaction(emoji='🇶', member=payload.member)
                return
        await payload.member.send(embed=embeds.getQueueJoinEmbed())
        queue += [QueuedPerson(user=payload.member)]
        if len(queue) >= 2:
            await createUserGame(p1=queue[0].user, p2=queue[1].user, embed=embeds.getQueueGameEmbed(queue[0].user, queue[1].user))
            await message.remove_reaction(emoji='🇶', member=queue[0].user)
            await message.remove_reaction(emoji='🇶', member=queue[1].user)
            for i in queue:
                i.task.cancel()
            queue = []
        else:
            temp = await channel.send(qPingRole.mention)
            await temp.delete()
        await qDisplayChannel.edit(name=f'Queued members: {len(queue)}')

@bot.event
async def on_raw_reaction_remove(payload):
    global queue
    farkleCentral = bot.guilds[0]
    channel = discord.utils.get(farkleCentral.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = discord.utils.get(farkleCentral.members, id=payload.user_id)
    if channel == prefChannel:
        if payload.message_id == idList.pref2Msg:
            await member.remove_roles(annPingRole)
        elif payload.message_id == idList.pref3Msg:
            await member.remove_roles(qPingRole)
        return
    if str(payload.emoji) == '🇶' and payload.channel_id == idList.newGameChannel:
        for i in queue:
            if i.user == member:
                i.task.cancel()
                queue = [j for j in queue if j != i]
                break
        await member.send(embed=embeds.getQueueLeaveEmbed())
        await qDisplayChannel.edit(name=f'Queued members: {len(queue)}')

async def kickQueuedMember(user: discord.User):
    global queue
    try:
        await asyncio.sleep(60)
    except:
        return
    for n, i in enumerate(queue):
        if i.user == user:
            del queue[n]
            break
    await user.send(embed=embeds.getQueueKickEmbed())

@bot.slash_command(name='invite', guild_ids=[idList.farkleCentralId], description='Invite your friend to a farkle game')
async def invite(ctx, user:discord.Option(discord.User, 'The user you want to invite', required=True)):
    global totalGames, currentGames
    if ctx.author == user:
        await ctx.respond(embed=embeds.getSelfChallengeErrEmbed(bot.user), ephemeral=True)
        return
    if user == bot.user:
        await ctx.respond(embed=embeds.getAiGameStartingEmbed(), ephemeral=True)
        await createAiGame(player=ctx.author)
        return
    for i in currentGames:
        if ctx.author in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getSelfIngameEmbed(), ephemeral=True)
            return
        if user in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getInvitedIngameEmbed(user), ephemeral=True)
            return
    users = []
    async for user1 in pref1Msg.reactions[0].users():
        users += [user1]
    if user in users:
        await ctx.respond(embed=embeds.getHasDisabledInvitesEmbed(user), ephemeral=True)
        return
    await ctx.respond(embed=embeds.getChallengeCreationEmbed(user), ephemeral=True)
    await createUserGame(ctx.author, user, embeds.getInviteEmbed(ctx.author, user))

@bot.slash_command(name='share', guild_ids=[idList.farkleCentralId], description='Share you replay with a friend')
async def invite(ctx, user:discord.Option(discord.User, 'The user you want to start/stop sharing the replay', required=True), status:discord.Option(bool, 'True if you want to add the user, False if you want to remove the user', required=True)):
    for i in replays:
        if i.channel == ctx.channel:
            if status:
                await i.addMember(user=user)
                await ctx.respond(embed=embeds.getReplaySharedEmbed(user=user), ephemeral=True)
                return
            await i.removeMember(user=user)
            await ctx.respond(embed=embeds.getReplaySharedEmbed(user=user), ephemeral=True)
            return
    await ctx.respond(embed=embeds.getNotInReplayChannelEmbed(), ephemeral=True)

async def createAiGame(player):
    global totalGames, currentGames
    channel = await farkleCentral.create_text_channel(name=f'game-{totalGames}',category=gamesCategory)
    await channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
    await channel.set_permissions(player, read_messages=True, send_messages=False)
    temp = FarkleGame(id=totalGames, state=1, players=(player, bot.user), channel=channel, latestMsg= await channel.send(embed=embeds.getAiGameReadyEmbed(player=player)))
    currentGames += [temp]
    temp.embedList += [embeds.getAiGameReadyEmbed(player=player)]
    totalGames += 1
    await totalGamesMsg.edit(f'{totalGames}')
    await temp.startTurn()

async def createUserGame(p1: discord.User, p2: discord.User, embed: discord.Embed):
    global totalGames, currentGames
    channel = await farkleCentral.create_text_channel(name=f'game-{totalGames}',
                                                      category=gamesCategory)
    await channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
    await channel.set_permissions(p1, read_messages=True, send_messages=False)
    await channel.set_permissions(p2, read_messages=True, send_messages=False)
    msg = await channel.send(embed=embed)
    await msg.add_reaction('✅')
    temp = FarkleGame(id=totalGames, state=0, players=(p1, p2), channel=channel, latestMsg=msg)
    currentGames += [temp]
    totalGames += 1
    await totalGamesMsg.edit(f'{totalGames}')
    temp.task = asyncio.create_task(cancelUnreadyGame(temp, msg, channel, p1, p2))

async def cancelUnreadyGame(temp, msg, channel, p1, p2):
    try:
        await asyncio.sleep(45)
    except asyncio.CancelledError:
        return
    await msg.clear_reactions()
    await channel.send(embed=embeds.getReadyTimeoutEmbed(p1, p2))
    await temp.terminateGame(15)

f = open('token.txt', 'r')
bot.run(f.read())
f.close()