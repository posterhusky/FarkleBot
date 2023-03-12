import discord, embeds, asyncio, emojis, random, time

import replayFunctions
from replayFunctions import Replay
from meldButtons import MeldButton, HotPotatoMeldButton
from discord.ui import View, Button

dice = [emojis.die1, emojis.die2, emojis.die3, emojis.die4, emojis.die5, emojis.die6]
turnMods = [
    '**⬇ Heavy pockets:** *100pts.* removed form bank for every die in the inventory',
    '**⬇ Double trouble:** The banked score is added to the opponent\'s bank as well',
    '**⬇ Rounding error:** Banked score is rounded down to the nearest *500* multiple',
    '**⬆ Farkle shield:** *50%* of the turn score is banked upon a farkle.',
    '**⬆ Banking bonus:** *10%* of the bank are added on top of the banked score',
    '**⬆ Point transfer:** *50%* of the banked score is taken from the opponent\'s bank'
]

farkleCentral, replaysCategory, currentGames, bot, replaysChannel, regularRole = [None]*6

def init(farkleCentralArg, replaysCategoryArg, currentGamesArg, botArg, replaysChannelArg, regularRoleArg):
    global farkleCentral, replaysCategory, currentGames, bot, replaysChannel, regularRole
    farkleCentral, replaysCategory, currentGames, bot, replaysChannel, regularRole = farkleCentralArg, replaysCategoryArg, currentGamesArg, botArg, replaysChannelArg, regularRoleArg


class NormalGame():
    def __init__(self, id: int, state: int, players: tuple, channel: discord.TextChannel,
                 goal: int, startMultiplier: float, multiplierQuantity: int, multiplierQuality: float, leadAmount: int):
        self.id = id
        self.state = state
        self.players = players
        self.channel = channel
        self.turn = 0
        self.bank = [0, 0, 0]
        self.msgCount = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.latestMsg = None
        self.task = None
        self.melds = []
        self.latestEmbed = None
        self.embedList = []
        self.multiplier = startMultiplier
        self.mltQty = multiplierQuantity
        self.mltQual = multiplierQuality
        self.turnsQty = 0
        self.lead = None
        self.hurryUpMsg = None
        self.turnHistory = []
        self.highStakesPass = None
        self.goal = goal
        self.leadAmount = leadAmount
        self.isHighStake = False
        print('created game: ', [p.name for p in players])

    async def startGame(self):
        self.embedList = [embeds.getStartNormalEmbed(mltQty=self.mltQty,ptLead=self.leadAmount, mltQual=self.mltQual, goal=self.goal, p2=self.players[1], p1=self.players[0], turn=self.turn)]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        await self.startTurn()

    async def saveReplay(self, interaction: discord.Interaction):
        global replays
        await interaction.response.send_message(embed=embeds.getReplaySavedEmbed(), ephemeral=True)
        temp = Replay(sharedAccess=[self.players[1] if interaction.user == self.players[0] else self.players[0]],
                      host=interaction.user,
                      channel=await farkleCentral.create_text_channel(name=f'replay-{self.id}',
                                                                      category=replaysCategory),
                      id=self.id, infoMsg=None)
        replayFunctions.replays += [temp]
        await temp.uploadReplay(embedList=self.embedList, farkleCentral=farkleCentral, replaysChannel=replaysChannel, regularRole=regularRole)

    async def terminateGame(self, delay):
        self.state = 2
        btn = Button(label='Save replay', emoji='💿', style=discord.ButtonStyle.blurple, disabled=False)
        btn.callback = self.saveReplay
        btns = View()
        btns.add_item(btn)
        self.latestEmbed = embeds.getReplayEmbed()
        self.latestMsg = await self.channel.send(embed=self.latestEmbed, view=btns)
        print('game ended:', [p.name for p in self.players])
        await asyncio.sleep(delay)
        await self.channel.delete()
        while self in currentGames:
            currentGames.remove(self)

    def isBot(self) -> bool:
        return self.turn == 1 and self.players[1] == bot.user

    def getTurnRecap(self) -> list:
        return embeds.getTurnRecap(destUsr=self.players[self.turn], p1Bank=self.bank[0], p2Bank=self.bank[1],
                                   turnBank=self.bank[2], qty=self.turnsQty, pNum=self.turn, history=self.turnHistory)

    async def startTurn(self):
        if self.state == 2:
            return
        if abs(self.bank[0] - self.bank[1]) >= self.leadAmount and self.leadAmount > 0:
            self.lead = 0 if self.bank[0] > self.bank[1] else 1
        else:
            self.lead = -1
        self.turnHistory = []
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        self.isHighStake = False
        if self.turnsQty % self.mltQty == 0:
            self.multiplier = round(self.multiplier + self.mltQual, 3)
            self.embedList += [
                embeds.getMultiplierIncrEmbed(multiplier=self.multiplier, turns=self.turnsQty, incr=self.mltQual)]
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
        self.latestEmbed = embeds.getNormalStartTurnEmbed(mlt=self.multiplier, lead=self.turn == self.lead, pNum=self.turn,
                                                    stake=self.highStakesPass, time=int(time.time())+60)
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            if self.highStakesPass != None and self.highStakesPass[0] * random.randint(1, 3) >= 500 and random.randint(
                    0, 7) <= len(self.highStakesPass[1]):
                print('high stakes', self.highStakesPass)
                self.bank[2] = self.highStakesPass[0]
                self.tableDice = self.highStakesPass[1]
                self.invDice = self.highStakesPass[2]
                self.isHighStake = True
                btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
                btn3.callback = self.giveUp
                btns = View()
                btns.add_item(btn3)
                self.latestEmbed = embeds.getHighStakesEmbed(mlt=self.multiplier,
                                                             iconList=[dice[i] for i in self.tableDice],
                                                             iconList2=[dice[i] for i in self.invDice],
                                                             pts=self.highStakesPass[0], lead=1 == self.lead,
                                                             pNum=1, time=int(time.time())+60)
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
        self.isHighStake = True
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
        self.latestEmbed = embeds.getHighStakesEmbed(mlt=self.multiplier, iconList=[dice[i] for i in self.tableDice],
                                                     iconList2=[dice[i] for i in self.invDice],
                                                     pts=self.highStakesPass[0], lead=self.turn == self.lead,
                                                     pNum=self.turn, time=int(time.time())+60)
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
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.embedList += [embeds.getGiveUpEmbed(user=interaction.user, pNum=int(interaction.user == self.players[1]), time=int(time.time())+15)]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(15)

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[self.turn] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user == self.players[1])
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] >= self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[self.turn], pNum=self.turn, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = int(not self.turn)
        await self.startTurn()

    async def extendIdleTimeout(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=embeds.getIdleTimeoutExtendedEmbed(), ephemeral=True)
        self.task.cancel()
        self.task = asyncio.create_task(self.cancelIdleUser())
        if self.hurryUpMsg != None:
            await self.hurryUpMsg.delete()
        self.hurryUpMsg = None
        self.latestEmbed.remove_field(-1)
        self.latestEmbed.add_field(name=f'The game will be terminated if you won\'t react <t:{int(time.time())+60}:R>!', value='', inline=False)
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed])

    async def cancelIdleUser(self):
        if self.hurryUpMsg != None:
            await self.hurryUpMsg.delete()
        self.hurryUpMsg = None
        try:
            await asyncio.sleep(45)
        except asyncio.CancelledError:
            return
        self.hurryUpMsg = await self.channel.send(embed=embeds.getHurryUpEmbed(self.players[self.turn], time=int(time.time())+15))
        temp = await self.channel.send(f'{self.players[self.turn].mention}')
        await temp.delete()
        try:
            await asyncio.sleep(15)
        except asyncio.CancelledError:
            return
        self.embedList += self.getTurnRecap()
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += [embeds.getInteractionTimeoutEmbed(user=self.players[self.turn], time=int(time.time())+15)]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(15)

    async def hotDiceActions(self, result):
        btns = View()
        if not self.isBot():
            btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
            btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=False)
            btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
            btn4.callback = self.extendIdleTimeout
            btn1.callback = self.rollDice
            btn2.callback = self.bankScore
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn4)
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns.add_item(btn3)
        self.bank[2] += result[1]
        self.latestEmbed = embeds.getHotDiceEmbed(iconList=[dice[i] for i in self.tableDice], pts=result[1],
                                                  mlt=self.multiplier, lead=self.turn == self.lead, pNum=self.turn, time=int(time.time())+60)
        self.turnHistory += [
            ('Rolled hot dice:', ' '.join([dice[i] for i in self.tableDice]) + f' *- {result[1]}*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        self.tableDice = [0] * 6
        self.invDice = []

    async def farkleActions(self):
        if self.isHighStake == False or len(self.turnHistory) != 1:
            self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn,
                                                      iconList=[dice[i] for i in self.tableDice])
            self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            if self.isHighStake == False:
                self.highStakesPass = (self.bank[2] if self.bank[2] > 1000 else 1000, self.tableDice, self.invDice)
            else:
                self.highStakesPass = None
        else:
            self.latestEmbed = embeds.getFailedHighStakeEmbed(pNum=self.turn,
                                                              iconList=[dice[i] for i in self.tableDice],
                                                              pts=self.highStakesPass[0])
            self.turnHistory += [('High stakes failed:', ' '.join(
                [dice[i] for i in self.tableDice]) + f" (*{self.highStakesPass[0]} pts.* lost)")]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            self.bank[self.turn] -= self.highStakesPass[0]
            if self.bank[self.turn] < 0:
                self.bank[self.turn] = 0
            self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
        await self.startTurn()


    async def botRollDice(self):  # bot action ========================================================
        if self.turn == 0 or self.state == 2:
            return
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0]:
            if self.turn == 0:
                return
            await self.hotDiceActions(result=result)
            await asyncio.sleep(1.5)
            await self.botRollDice()
            return
        if self.melds == []:
            if self.turn == 0:
                return
            await self.farkleActions()
            return
        if self.turn == 0:
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn3)
        self.latestEmbed = embeds.getAfterRollEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], mlt=self.multiplier,
                                                    lead=1 == self.lead, pNum=1, time=int(time.time())+60)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        await self.botMeldItem(self.melds[0])

    async def botMeldItem(self, meld):
        if self.turn == 0 or self.state == 2:
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
                                                    lead=1 == self.lead, pNum=1, time=int(time.time())+60)
        self.turnHistory += [('Melded dice:', f'{meld[3]} × {meld[1]} *- {meld[2]}*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        if self.turn == 0:
            return
        if self.bank[1] + self.bank[2] >= self.goal:
            await self.botBankScore()
            return
        if self.melds != []:
            await self.botMeldItem(self.melds[0])
            return
        if random.randint(0, 7) <= len(self.tableDice) + 1:
            if self.highStakesPass != 0 and random.randint(0, 2) == 0:
                await self.botBankScore()
                return
            await self.botRollDice()
            return
        await self.botBankScore()

    async def botBankScore(self):
        if self.turn == 0 or self.state == 2:
            return
        self.bank[1] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=True)
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[1] >= self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[1], pNum=1, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
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
            await self.hotDiceActions(result=result)
            self.task = asyncio.create_task(self.cancelIdleUser())
            return
        if self.melds == []:
            await self.farkleActions()
            return
        btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=True)
        btn2 = Button(label='Bank score', emoji='💰', style=discord.ButtonStyle.green, disabled=True)
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.extendIdleTimeout
        btn2.callback = self.bankScore
        btn3.callback = self.giveUp
        btns = View()
        for i in self.melds:
            temp = MeldButton(game=self, meld=i, priority=i[2] == self.melds[0][2])
            btns.add_item(temp)
        btns.add_item(btn1)
        btns.add_item(btn2)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.latestEmbed = embeds.getAfterRollEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], mlt=self.multiplier,
                                                    lead=self.turn == self.lead, pNum=self.turn, time=int(time.time())+60)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        self.task = asyncio.create_task(self.cancelIdleUser())

    def getMelds(self):
        multiplier = 1 if self.turn == self.lead else self.multiplier
        amount = len(self.tableDice)
        sorted_nums = self.tableDice.copy()
        sorted_nums.sort()
        perfectTable = sorted_nums.copy()  # tests the possibility of hot dice by removing meldable dice
        perfectScore = 0  # score in case of hot dice
        self.melds = []  # die id, amount, pts, emoji
        for i in range(6):
            if self.tableDice.count(i) == 6:
                return (True, int(3000 * multiplier))
        if sorted_nums == list(range(6)):
            return (True, int(2500 * multiplier))
        for i in range(6):
            if self.tableDice.count(i) >= 5:
                self.melds += [(i, 5, int(2000 * multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int(2000 * multiplier)
        if amount == 6 and sorted_nums[0] == sorted_nums[1] and sorted_nums[2] == sorted_nums[3] and sorted_nums[4] == \
                sorted_nums[5]:
            return (True, int(1500 * multiplier))
        if self.tableDice.count(0) >= 3:
            self.melds += [(0, 3, int(1000 * multiplier), dice[0])]
            if 0 in perfectTable:
                while 0 in perfectTable:
                    perfectTable.remove(0)
                perfectScore += int(1100 * multiplier) if self.tableDice.count(0) == 4 else int(1000 * multiplier)
        for i in range(6):
            if self.tableDice.count(i) >= 4:
                self.melds += [(i, 4, int(1000 * multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int(1000 * multiplier)
        for i in range(1, 6):
            if self.tableDice.count(i) >= 3:
                self.melds += [(i, 3, int((i + 1) * 100 * multiplier), dice[i])]
                if i in perfectTable:
                    while i in perfectTable:
                        perfectTable.remove(i)
                    perfectScore += int((i + 1) * 100 * multiplier)
        if 0 in self.tableDice:
            if self.tableDice.count(0) == 2:
                self.melds += [(0, 2, int(200 * multiplier), dice[0])]
            self.melds += [(0, 1, int(100 * multiplier), dice[0])]
            perfectScore += perfectTable.count(0) * int(100 * multiplier)
            while 0 in perfectTable:
                perfectTable.remove(0)
        if 4 in self.tableDice:
            if self.tableDice.count(4) == 2:
                self.melds += [(4, 2, int(100 * multiplier), dice[4])]
            self.melds += [(4, 1, int(50 * multiplier), dice[4])]
            perfectScore += perfectTable.count(4) * int(50 * multiplier)
            while 4 in perfectTable:
                perfectTable.remove(4)

        if perfectTable == []:
            self.melds = []
            return (True, perfectScore)
        else:
            return (False, 0)

class ScoreAttackGame(NormalGame):
    async def startGame(self):
        self.embedList = [
            embeds.getStartScoreAttackEmbed(self.turn, p1=self.players[0], p2=self.players[1])]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        self.bank = [1000, 1000, 0]
        await self.startTurn()
    async def farkleActions(self):
        if self.isHighStake == False or len(self.turnHistory) != 2:
            self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn,
                                                      iconList=[dice[i] for i in self.tableDice])
            self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            if self.bank[self.turn] < 0:
                await asyncio.sleep(2)
                self.embedList += self.getTurnRecap()
                await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
                self.embedList += [
                    embeds.getNegBankWinEmbed(winner=self.players[not self.turn], pNum=1, turns=self.turnsQty, looser=self.players[self.turn], time=int(time.time())+30)]
                await self.channel.send(embed=self.embedList[-1])
                await self.terminateGame(30)
                return
            if self.isHighStake == False:
                self.highStakesPass = (self.bank[2] if self.bank[2] > 1000 else 1000, self.tableDice, self.invDice)
            else:
                self.highStakesPass = None
        else:
            self.latestEmbed = embeds.getFailedHighStakeEmbed(pNum=self.turn,
                                                              iconList=[dice[i] for i in self.tableDice],
                                                              pts=self.highStakesPass[0])
            self.turnHistory += [('High stakes failed:', ' '.join(
                [dice[i] for i in self.tableDice]) + f" (*{self.highStakesPass[0]} pts.* lost)")]
            self.bank[self.turn] -= self.highStakesPass[0]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            if self.bank[self.turn] < 0:
                await asyncio.sleep(2)
                self.embedList += self.getTurnRecap()
                await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
                self.embedList += [
                    embeds.getNegBankWinEmbed(winner=self.players[not self.turn], pNum=1, turns=self.turnsQty, looser=self.players[self.turn], time=int(time.time())+30)]
                await self.channel.send(embed=self.embedList[-1])
                await self.terminateGame(30)
                return
            self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
        await self.startTurn()

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[self.turn] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user == self.players[1])
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        await asyncio.sleep(2)
        if self.bank[self.turn] > 5000:
            self.turnHistory += [('Score cap exceeded:', '*' + str(self.bank[self.turn] - 5000) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[self.turn] - 5000, self.turn, 5000)
            self.bank[self.turn] = 5000
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        self.embedList += self.getTurnRecap()
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] < 0:
            self.embedList += [
                embeds.getNegBankWinEmbed(winner=self.players[not self.turn], pNum=1, turns=self.turnsQty,
                                              looser=self.players[self.turn], time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = int(not self.turn)
        await self.startTurn()

    async def botBankScore(self):
        if self.turn == 0 or self.state == 2:
            return
        self.bank[1] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=True)
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        await asyncio.sleep(2)
        if self.bank[self.turn] > 5000:
            self.turnHistory += [('Score cap exceeded:', '*' + str(self.bank[1] - 5000) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[1] - 5000, 1, 5000)
            self.bank[1] = 5000
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.embedList += self.getTurnRecap()
        if self.bank[1] >= self.goal:
            self.embedList += [
                embeds.getNegBankWinEmbed(winner=self.players[0], pNum=1, turns=self.turnsQty,
                                              looser=self.players[1], time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = 0
        await self.startTurn()

    async def startTurn(self):
        if self.state == 2:
            return
        self.turnHistory = [('Score attack:', f'*{-250 if self.turnsQty==0 else -500} pts.*')]
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        self.bank[self.turn] -= 250 if self.turnsQty==1 else 500
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
        self.latestEmbed = embeds.getScoreAttackStartTurnEmbed(pNum=self.turn,
                                                    stake=self.highStakesPass, first=self.turnsQty==1, time=int(time.time())+60)
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            if self.highStakesPass != None and self.highStakesPass[0] * random.randint(1, 3) >= 500 and random.randint(
                    0, 7) <= len(self.highStakesPass[1]):
                print('high stakes', self.highStakesPass)
                self.bank[2] = self.highStakesPass[0]
                self.tableDice = self.highStakesPass[1]
                self.invDice = self.highStakesPass[2]
                self.isHighStake = True
                btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
                btn3.callback = self.giveUp
                btns = View()
                btns.add_item(btn3)
                self.latestEmbed = embeds.getHighStakesEmbed(mlt=self.multiplier,
                                                             iconList=[dice[i] for i in self.tableDice],
                                                             iconList2=[dice[i] for i in self.invDice],
                                                             pts=self.highStakesPass[0], lead=1 == self.lead,
                                                             pNum=1, time=int(time.time())+60)
                self.turnHistory += [('High stakes!', f'*{self.highStakesPass[0]} pts.*')]
                await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
                await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())


class SnowballGame(NormalGame):
    async def startGame(self):
        self.goal = 5000
        self.embedList = [
            embeds.getStartSnowballEmbed(self.turn, p1=self.players[0], p2=self.players[1], cap=self.goal)]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        await self.startTurn()

    def getTurnRecap(self) -> list:
        return embeds.getSnowballTurnRecap(destUsr=self.players[self.turn], bank=self.bank[0], turnBank=self.bank[2], qty=self.turnsQty, pNum=self.turn, history=self.turnHistory)

    async def farkleActions(self):
        self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn, iconList=[dice[i] for i in self.tableDice])
        self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
        await self.startTurn()

    async def botRollDice(self):  # bot action ========================================================
        if self.turn == 0 or self.state == 2:
            return
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0]:
            if self.turn == 0:
                return
            await self.hotDiceActions(result=result)
            await asyncio.sleep(1.5)
            await self.botRollDice()
            return
        if self.melds == []:
            if self.turn == 0:
                return
            await self.farkleActions()
            return
        if self.turn == 0:
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn3)
        self.latestEmbed = embeds.getAfterRollEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], mlt=self.multiplier,
                                                    lead=1 == self.lead, pNum=1, time=int(time.time())+60)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        if sum([i[2] for i in self.melds]) + self.bank[0] + self.bank[2] > self.goal and len(self.melds) != 1:
            print('making plan')
            plan = []
            for meld in self.melds:
                if meld[2] + sum([k[2] for k in plan]) + self.bank[0] + self.bank[2] <= self.goal:
                    plan += [meld]
            print('plan:', plan)
            if plan != []:
                await self.botMeldPlan(plan)
                return
        await self.botMeldItem(self.melds[0])

    async def botMeldPlan(self, plan):
        if self.turn == 0 or self.state == 2:
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn3)
        for meld in plan:
            print('meld:', meld)
            self.bank[2] += meld[2]
            for _ in range(meld[1]):
                self.tableDice.remove(meld[0])
                self.invDice += [meld[0]]
            self.latestEmbed = embeds.getAfterMeldEmbed(iconList=[dice[i] for i in self.tableDice],
                                                        iconList2=[dice[i] for i in self.invDice], meld=meld,
                                                        mlt=self.multiplier,
                                                        lead=1 == self.lead, pNum=1, time=int(time.time())+60)
            self.turnHistory += [('Melded dice:', f'{meld[3]} × {meld[1]} *- {meld[2]}*')]
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
            await asyncio.sleep(1.5)
            if self.turn == 0:
                return
        if self.bank[0] + self.bank[2] >= self.goal:
            await self.botBankScore()
            return
        if random.randint(0, 7) <= len(self.tableDice) + 1 and self.goal - self.bank[0] - self.bank[2] <= random.randint(0, 4)*50:
            await self.botRollDice()
            return
        await self.botBankScore()

    # ✈

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        oldBank = self.bank[0]
        self.bank[0] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=bool(self.turn))
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        if self.bank[0] > self.goal:
            self.turnHistory += [('Score cap exceeded:', '*' + str(self.bank[0] - self.goal) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[0] - self.goal, self.turn, oldBank)
            self.bank[0] = oldBank
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[0] == self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[self.turn], pNum=self.turn, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = int(not self.turn)
        await self.startTurn()

    async def botBankScore(self):
        if self.turn == 0 or self.state == 2:
            return
        oldBank = self.bank[0]
        self.bank[0] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=True)
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        if self.bank[0] > self.goal:
            self.turnHistory += [('Score cap exceeded:', '*' + str(self.bank[0] - self.goal) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[0] - self.goal, 1, oldBank)
            self.bank[0] = oldBank
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[0] == self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[1], pNum=1, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = 0
        await self.startTurn()

    async def startTurn(self):
        if self.state == 2:
            return
        self.turnHistory = []
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        self.isHighStake = False
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
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getNormalStartTurnEmbed(mlt=self.multiplier, lead=self.turn == self.lead, pNum=self.turn,
                                                    stake=self.highStakesPass, time=int(time.time())+60)
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())
            
class HotPotatoGame(NormalGame):
    async def startGame(self):
        self.embedList = [
            embeds.getStartHotPotatoEmbed(self.turn, p1=self.players[0], p2=self.players[1])]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        self.bank = [1000, 1000, 0]
        await self.startTurn()

    def getTurnRecap(self) -> list:
        return embeds.getHotPotatoRecap(destUsr=self.players[self.turn], bank1=self.bank[0], bank2=self.bank[1], qty=self.turnsQty, pNum=self.turn, history=self.turnHistory)

    async def farkleActions(self):
        self.latestEmbed = embeds.getFarkledEmbed(turnBank=500, pNum=self.turn, iconList=[dice[i] for i in self.tableDice])
        self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]) + ' (*500 pts.* lost)')]
        self.bank[self.turn] -= 500
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] < 0:
            await asyncio.sleep(2)
            self.embedList += self.getTurnRecap()
            await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
            self.embedList += [
                embeds.getNegBankWinEmbed(winner=self.players[not self.turn], pNum=1, turns=self.turnsQty,
                                          looser=self.players[self.turn], time=int(time.time()) + 30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.turn = int(not self.turn)
        self.tableDice = [0] * 6
        self.invDice = []
        await self.startTurn()

    async def passTurn(self, interaction: discord.Interaction = None):
        if interaction != None and interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        if interaction != None:
            self.task.cancel()
            await interaction.response.defer()
        self.latestEmbed = embeds.getTurnPassEmbed(pts=250, pNum=self.turn)
        self.turnHistory += [('Turn Passed:', '*-250 pts.*')]
        self.bank[self.turn] -= 250
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] < 0:
            await asyncio.sleep(2)
            self.embedList += self.getTurnRecap()
            await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
            self.embedList += [
                embeds.getNegBankWinEmbed(winner=self.players[not self.turn], pNum=1, turns=self.turnsQty,
                                          looser=self.players[self.turn], time=int(time.time()) + 30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.turn = int(not self.turn)
        await self.startTurn()

    async def hotDiceActions(self, result):
        self.bank[self.turn] += result[1]
        self.latestEmbed = embeds.getHotDiceEmbed(iconList=[dice[i] for i in self.tableDice], pts=result[1],
                                                  mlt=self.multiplier, lead=self.turn == self.lead, pNum=self.turn, time=int(time.time())+60)
        self.turnHistory += [
            ('Rolled hot dice:', ' '.join([dice[i] for i in self.tableDice]) + f' *- {result[1]}*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        if self.bank[self.turn] > 5000:
            self.turnHistory += [
                ('Score cap exceeded:', '*' + str(self.bank[self.turn] - 5000) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[self.turn] - 5000, pNum=self.turn, cap=5000)
            self.bank[self.turn] = 5000
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
        await self.startTurn()
    
    async def botRollDice(self):  # bot action ========================================================
        if self.turn == 0 or self.state == 2:
            return
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0]:
            if self.turn == 0:
                return
            await self.hotDiceActions(result=result)
            await asyncio.sleep(1.5)
            await self.botRollDice()
            return
        if self.melds == []:
            if self.turn == 0:
                return
            await self.farkleActions()
            return
        if self.turn == 0:
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        btns = View()
        btns.add_item(btn3)
        self.latestEmbed = embeds.getHotPotatoAfterRollEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], pNum=1, time=int(time.time())+60)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        await asyncio.sleep(1.5)
        await self.botMeldItem(self.melds[0])

    async def botMeldItem(self, meld):
        if self.turn == 0 or self.state == 2:
            return
        self.bank[1] += meld[2]
        for _ in range(meld[1]):
            self.tableDice.remove(meld[0])
            self.invDice += [meld[0]]
        self.latestEmbed = embeds.getAfterMeldEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], meld=meld,
                                                    mlt=self.multiplier,
                                                    lead=1 == self.lead, pNum=1, time=None)
        self.turnHistory += [('Melded dice:', f'{meld[3]} × {meld[1]} *- {meld[2]}*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        if self.bank[self.turn] > 5000:
            self.turnHistory += [
                ('Score cap exceeded:', '*' + str(self.bank[1] - 5000) + ' pts.* over the limit')]
            self.latestEmbed = embeds.getScoreCapExceededEmbed(self.bank[1] - 5000, pNum=self.turn, cap=5000)
            self.bank[1] = 5000
            await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
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
            await self.hotDiceActions(result=result)
            return
        if self.melds == []:
            await self.farkleActions()
            return
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.extendIdleTimeout
        btn3.callback = self.giveUp
        btns = View()
        for i in self.melds:
            temp = HotPotatoMeldButton(game=self, meld=i, priority=i[2] == self.melds[0][2])
            btns.add_item(temp)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.latestEmbed = embeds.getHotPotatoAfterRollEmbed(iconList=[dice[i] for i in self.tableDice],
                                                    iconList2=[dice[i] for i in self.invDice], pNum=self.turn, time=int(time.time())+60)
        self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        self.task = asyncio.create_task(self.cancelIdleUser())

    async def startTurn(self):
        if self.state == 2:
            return
        self.turnHistory = []
        self.turnsQty += 1
        btns = View()
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        if self.isBot():
            btns.add_item(btn3)
        else:
            btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
            btn2 = Button(label='Pass turn', emoji='📨', style=discord.ButtonStyle.blurple, disabled=False)
            btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
            btn4.callback = self.extendIdleTimeout
            btn2.callback = self.passTurn
            btn1.callback = self.rollDice
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getHotPotatoStartTurnEmbed(pNum=self.turn, time=int(time.time())+60, iconList=[dice[i] for i in self.tableDice])
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            if random.randint(0, 2) < len(self.tableDice):
                await self.botRollDice()
                return
            await self.passTurn()
            return
        temp = await self.channel.send(f'{self.players[self.turn].mention}')
        await temp.delete()
        self.task = asyncio.create_task(self.cancelIdleUser())

class TugOfWarGame(NormalGame):
    async def startGame(self):
        self.embedList = [
            embeds.getStartTugOfWarEmbed(self.turn, p1=self.players[0], p2=self.players[1])]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        self.bank = [2500, 2500, 0]
        self.goal = 5001
        await self.startTurn()

    async def startTurn(self):
        if self.state == 2:
            return
        self.highStakesPass = None
        self.turnHistory = []
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        self.isHighStake = False
        if self.turnsQty % self.mltQty == 0:
            self.multiplier = round(self.multiplier + self.mltQual, 3)
            self.embedList += [
                embeds.getMultiplierIncrEmbed(multiplier=self.multiplier, turns=self.turnsQty, incr=self.mltQual)]
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
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getNormalStartTurnEmbed(mlt=self.multiplier, lead=self.turn == self.lead, pNum=self.turn,
                                                    stake=self.highStakesPass, time=int(time.time())+60)
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[self.turn] += self.bank[2]
        self.bank[not self.turn] -= self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user == self.players[1])
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[not self.turn] < 0:
            self.embedList += [
                embeds.getNormalWinEmbed(pNum=self.turn, time=int(time.time())+30, turns=self.turnsQty, winner=self.players[self.turn])]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = int(not self.turn)
        await self.startTurn()

    async def botBankScore(self):
        if self.turn == 0 or self.state == 2:
            return
        self.bank[1] += self.bank[2]
        self.bank[0] -= self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=True)
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[0] < 0:
            self.embedList += [
                embeds.getNegBankWinEmbed(winner=self.players[1], pNum=1, turns=self.turnsQty,
                                          looser=self.players[0], time=int(time.time()) + 30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = 0
        await self.startTurn()

class MysteryDieGame(NormalGame):
    async def startGame(self):
        self.embedList = [
            embeds.getStartMysteryDieEmbed(self.turn, p1=self.players[0], p2=self.players[1])]
        self.latestMsg = await self.channel.send(embed=self.embedList[0])
        self.mod = None
        self.showMod = False
        await self.startTurn()

    def getTurnRecap(self) -> list:
        return embeds.getMysteryDieTurnRecap(destUsr=self.players[self.turn], p1Bank=self.bank[0], p2Bank=self.bank[1],
                                   turnBank=self.bank[2], qty=self.turnsQty, pNum=self.turn, history=self.turnHistory, mod=None if self.mod == None else turnMods[self.mod], showMod=self.showMod)

    async def startTurn(self):
        if self.state == 2:
            return
        if abs(self.bank[0] - self.bank[1]) >= self.leadAmount and self.leadAmount > 0:
            self.lead = 0 if self.bank[0] > self.bank[1] else 1
        else:
            self.lead = -1
        self.turnHistory = []
        self.bank[2] = 0
        self.tableDice = [0] * 6
        self.invDice = []
        self.turnsQty += 1
        self.isHighStake = False
        self.highStakesPass = None
        self.mod = None
        self.showMod = False
        if self.turnsQty % self.mltQty == 0:
            self.multiplier = round(self.multiplier + self.mltQual, 3)
            self.embedList += [
                embeds.getMultiplierIncrEmbed(multiplier=self.multiplier, turns=self.turnsQty, incr=self.mltQual)]
            await self.channel.send(embed=self.embedList[-1])
            await asyncio.sleep(1)
        btns = View()
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn3.callback = self.giveUp
        if bot.user in self.players and not self.isBot():
            btns.add_item(btn3)
        else:
            btn1 = Button(label='Yes, roll it', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
            btn2 = Button(label='No, continue', emoji='📨', style=discord.ButtonStyle.red, disabled=False)
            btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
            btn4.callback = self.extendIdleTimeout
            btn1.callback = self.mysteryDieRolled
            btn2.callback = self.mysteryDieSkipped
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getMysteryDieChoiceEmbed(pNum=self.turn, time=int(time.time()) + 60, user=self.players[not self.turn])
        self.latestMsg = await self.channel.send(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if bot.user in self.players and not self.isBot():
            await asyncio.sleep(1.5)
            if random.randint(0, 2):
                await self.mysteryDieRolled()
            else:
                await self.mysteryDieSkipped()
        else:
            temp = await self.channel.send(f'{self.players[not self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser(user=self.players[not self.turn]))


    async def mysteryDieRolled(self, interaction: discord.Interaction = None):
        if interaction != None and interaction.user != self.players[not self.turn]:
            await interaction.response.send_message(embed=embeds.getMysteryDieNotYourTurnEmbed(), ephemeral=True)
            return
        self.mod = random.randint(0, 5)
        if interaction != None:
            self.task.cancel()
            await interaction.response.send_message(embed=embeds.getMysteryDieRolledEmbed(mod=None if self.mod == None else turnMods[self.mod]), ephemeral=True)
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
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getNormalStartTurnEmbed(mlt=self.multiplier, lead=self.turn == self.lead,
                                                          pNum=self.turn,
                                                          stake=self.highStakesPass, time=int(time.time()) + 60)
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())

    async def mysteryDieSkipped(self, interaction: discord.Interaction = None):
        if interaction != None and interaction.user != self.players[not self.turn]:
            await interaction.response.send_message(embed=embeds.getMysteryDieNotYourTurnEmbed(), ephemeral=True)
            return
        if interaction != None:
            self.task.cancel()
            await interaction.response.send_message(embed=embeds.getMysteryDieSkippedEmbed(), ephemeral=True)
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
            btns.add_item(btn1)
            btns.add_item(btn2)
            btns.add_item(btn3)
            btns.add_item(btn4)
        self.latestEmbed = embeds.getNormalStartTurnEmbed(mlt=self.multiplier, lead=self.turn == self.lead,
                                                          pNum=self.turn,
                                                          stake=self.highStakesPass, time=int(time.time()) + 60)
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=btns)
        if self.isBot():
            await asyncio.sleep(1.5)
            await self.botRollDice()
        else:
            temp = await self.channel.send(f'{self.players[self.turn].mention}')
            await temp.delete()
            self.task = asyncio.create_task(self.cancelIdleUser())

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.showMod = True
        match self.mod:
            case 0:
                self.bank[2] -= len(self.invDice) * 150
                self.turnHistory += [('Heavy pockets:', f'*-{len(self.invDice) * 150} pts.*')]
            case 1:
                self.bank[0] += self.bank[2]
                self.turnHistory += [('Double trouble:', f'*+{self.bank[2]} pts.* for P{int(not self.turn) + 1}')]
            case 2:
                self.bank[2] = (self.bank[2] // 500) * 500
                self.turnHistory += [
                    ('Rounding error:', f'*+{(self.bank[2] // 500) * 500 - self.bank[self.turn]} pts.*')]
            case 4:
                self.bank[2] += self.bank[self.turn] // 10
                self.turnHistory += [('Banking bonus:', f'*+{self.bank[self.turn] // 10} pts.*')]
            case 5:
                self.bank[0] -= self.bank[2] // 2
                self.turnHistory += [('Point transfer:', f'*-{self.bank[2] // 2} pts.* for P{int(not self.turn) + 1}')]
        if self.bank[not self.turn] < 0: self.bank[not self.turn] = 0
        self.bank[self.turn] += self.bank[2]
        self.latestEmbed = embeds.getMysteryDierScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user == self.players[1], mod=None if self.mod == None else turnMods[self.mod])
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[self.turn] >= self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[self.turn], pNum=self.turn, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = int(not self.turn)
        await self.startTurn()

    async def botBankScore(self):
        if self.turn == 0 or self.state == 2:
            return
        self.showMod = True
        match self.mod:
            case 0:
                self.bank[2] -= len(self.invDice) * 150
                self.turnHistory += [('Heavy pockets:', f'*-{len(self.invDice) * 150} pts.*')]
            case 1:
                self.bank[0] += self.bank[2]
                self.turnHistory += [('Double trouble:', f'*+{self.bank[2]} pts.* for P{int(not self.turn) + 1}')]
            case 2:
                self.bank[2] = (self.bank[2] // 500) * 500
                self.turnHistory += [
                    ('Rounding error:', f'*+{(self.bank[2] // 500) * 500 - self.bank[self.turn]} pts.*')]
            case 4:
                self.bank[2] += self.bank[self.turn] // 10
                self.turnHistory += [('Banking bonus:', f'*+{self.bank[self.turn] // 10} pts.*')]
            case 5:
                self.bank[0] -= self.bank[2] // 2
                self.turnHistory += [('Point transfer:', f'*-{self.bank[2] // 2} pts.* for P{int(not self.turn) + 1}')]
        self.bank[1] += self.bank[2]
        if self.bank[0] < 0: self.bank[0] = 0
        self.latestEmbed = embeds.getMysteryDierScoreBankedEmbed(turnBank=self.bank[2], pNum=True, mod=None if self.mod == None else turnMods[self.mod])
        self.turnHistory += [('Score banked:', '*' + str(self.bank[2]) + ' pts.*')]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        if self.bank[1] >= self.goal:
            self.embedList += [
                embeds.getNormalWinEmbed(winner=self.players[1], pNum=1, turns=self.turnsQty, time=int(time.time())+30)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
        self.highStakesPass = None
        self.turn = 0
        await self.startTurn()

    async def farkleActions(self):
        self.showMod = True
        self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn,
                                                  iconList=[dice[i] for i in self.tableDice])
        self.turnHistory += [('Rolled & farkled:', ' '.join([dice[i] for i in self.tableDice]))]
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        if self.mod == 3:
            self.bank[self.turn] += self.bank[2]//2
            self.turnHistory += [('Farkle shield:', f'*+{self.bank[2]//2} pts.*')]
        if self.mod == 4:
            self.bank[2] += self.bank[self.turn] // 10
            self.turnHistory += [('Banking bonus:', f'*+{self.bank[self.turn] // 10} pts.*')]
        self.highStakesPass = None
        self.embedList += self.getTurnRecap()
        await asyncio.sleep(2)
        await self.latestMsg.edit(embeds=self.getTurnRecap(), view=None)
        self.turn = int(not self.turn)
        await self.startTurn()

    async def cancelIdleUser(self, user: discord.user = None):
        if user == None:
            user = self.players[self.turn]
        if self.hurryUpMsg != None:
            await self.hurryUpMsg.delete()
        self.hurryUpMsg = None
        try:
            await asyncio.sleep(45)
        except asyncio.CancelledError:
            return
        self.hurryUpMsg = await self.channel.send(embed=embeds.getHurryUpEmbed(user, time=int(time.time())+15))
        temp = await self.channel.send(f'{user.mention}')
        await temp.delete()
        try:
            await asyncio.sleep(15)
        except asyncio.CancelledError:
            return
        self.embedList += self.getTurnRecap()
        await self.latestMsg.edit(embeds=self.getTurnRecap() + [self.latestEmbed], view=None)
        self.embedList += [embeds.getInteractionTimeoutEmbed(user=user, time=int(time.time())+15)]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(15)
