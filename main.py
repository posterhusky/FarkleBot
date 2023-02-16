import discord, random, embeds, asyncio
from discord.ui import View, Button

bot = discord.Bot(intents=discord.Intents().all())
farkleCentral = None
regularRole = None
adminRole = None
gamesCategory = None
replaysCategory = None

totalGames=0
currentGames = []

dice = '<:die1:1073714606813483071> <:die2:1073714605051887739> <:die3:1073714602350743692> <:die4:1073714600924692552> <:die5:1073714599691550880> <:die6:1073714597359521822>'.split()


class FarkleGame():
    def __init__(self, type: int, id: int, state: int, players: discord.User | tuple[discord.User, discord.User], channel: discord.TextChannel, latestMsg: discord.Message):
        self.type = type
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

    async def saveReplay(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.latestMsg.edit(embed=self.latestEmbed, view=View(Button(label='Replay saved', emoji='✅', style=discord.ButtonStyle.blurple, disabled=True)))
        channel = await farkleCentral.create_text_channel(name=f'replay-{str(self.id).rjust(6, "0")}', category=replaysCategory)
        await channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
        for i in self.embedList:
            await channel.send(embed=i)
        await channel.set_permissions(self.players[0], read_messages=True, send_messages=False)
        await channel.set_permissions(self.players[1], read_messages=True, send_messages=False)

    async def terminateGame(self, delay):
        self.state = 2
        await self.channel.set_permissions(self.players[0], read_messages=True, send_messages=False)
        await self.channel.set_permissions(self.players[1], read_messages=True, send_messages=False)
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

    def getTurnRecap(self) -> discord.Embed:
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
        self.embedList += [None]
        self.latestEmbed = embeds.getStartTurnEmbed(mlt=self.multiplier, lead=self.turn==self.lead, pNum=self.turn)
        self.latestMsg = await self.channel.send(embeds=[self.getTurnRecap(), self.latestEmbed], view=btns)
        temp = await self.channel.send(f'{self.players[self.turn].mention}')
        await temp.delete()
        self.task = asyncio.create_task(self.cancelIdleUser())

    async def giveUp(self, interaction: discord.Interaction):
        btn = Button(emoji='🏳', label='Give up', style=discord.ButtonStyle.red)
        btn.callback = self.giveUpConfirmed
        await interaction.response.send_message(embed=embeds.getGiveUpConfirmEmbed(), view=View(btn), ephemeral=True)

    async def giveUpConfirmed(self, interaction: discord.Interaction):
        self.task.cancel()
        await interaction.response.defer()
        for n, i in enumerate(self.embedList):
            if i == None:
                self.embedList[n] = self.getTurnRecap()
                break
        await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=None)
        self.embedList += [embeds.getGiveUpEmbed(user=interaction.user, pNum=self.turn)]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(15)

    async def bankScore(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.bank[self.turn] += self.bank[2]
        self.latestEmbed = embeds.getScoreBankedEmbed(turnBank=self.bank[2], pNum=interaction.user==self.players[1])
        self.turnHistory += [('Score banked:', str(self.bank[2]) + ' pts.')]
        await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=None)
        for n, i in enumerate(self.embedList):
            if i == None:
                self.embedList[n] = self.getTurnRecap()
                break
        await asyncio.sleep(2)
        await self.latestMsg.edit(embed=self.getTurnRecap(), view=None)
        if self.bank[self.turn] >= 10000:
            self.embedList += [
                embeds.getWinEmbed(winner=self.players[self.turn], pNum=self.turn, turns=self.turnsQty)]
            await self.channel.send(embed=self.embedList[-1])
            await self.terminateGame(30)
            return
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
        for n, i in enumerate(self.embedList):
            if i == None:
                self.embedList[n] = self.getTurnRecap()
                break
        await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=None)
        self.embedList += [embeds.getInteractionTimeoutEmbed(user=self.players[self.turn])]
        await self.channel.send(embed=self.embedList[-1])
        await self.terminateGame(15)

    async def rollDice(self, interaction: discord.Interaction):
        if interaction.user != self.players[self.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.task.cancel()
        await interaction.response.defer()
        self.tableDice = [random.randint(0, 5) for _ in '.' * len(self.tableDice)]
        result = self.getMelds()
        if result[0] == True:
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
            self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]) + ' (Hot dice)')]
            await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=btns)
            self.tableDice = [0] * 6
            self.invDice = []
            self.task = asyncio.create_task(self.cancelIdleUser())
            return
        if self.melds == []:
            self.latestEmbed = embeds.getFarkledEmbed(turnBank=self.bank[2], pNum=self.turn, iconList=[dice[i] for i in self.tableDice])
            self.turnHistory += [('Rolled dice:', ' '.join([dice[i] for i in self.tableDice]) + ' (Farkled)')]
            await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=None)
            for n, i in enumerate(self.embedList):
                if i == None:
                    self.embedList[n] = self.getTurnRecap()
                    break
            await asyncio.sleep(2)
            await self.latestMsg.edit(embed=self.getTurnRecap(), view=None)
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
        await self.latestMsg.edit(embeds=[self.getTurnRecap(), self.latestEmbed], view=btns)
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
        self.game.turnHistory += [('Melded dice:', f'{self.meld[3]} × {self.meld[1]}')]
        await self.game.latestMsg.edit(embeds=[self.game.getTurnRecap(), self.game.latestEmbed], view=btns)
        self.game.task = asyncio.create_task(self.game.cancelIdleUser())










@bot.event
async def on_ready():
    global farkleCentral, regularRole,adminRole, gamesCategory, replaysCategory, totalGames
    print(f'Logged on as {bot.user}!')
    farkleCentral = bot.guilds[0]
    regularRole = discord.Guild.get_role(farkleCentral, 1073320359245398077)
    adminRole = discord.Guild.get_role(farkleCentral, 1073320074875785216)
    gamesCategory = discord.utils.get(farkleCentral.categories, id=1073357967061164042)
    replaysCategory = discord.utils.get(farkleCentral.categories, id=1075132258127708240)
    totalGames = int(open('save.txt', 'r').read())


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if adminRole in message.author.roles:
        if message.content == '$rules':
            i = await message.channel.send(embeds=embeds.getRuleEmbeds())
        if message.content == '$newgameinfo':
            i = await message.channel.send(embeds=embeds.getNewGameEmbeds(bot.user))
            await i.add_reaction('🇶')

    for i in currentGames:
        if i.channel == message.channel:
            i.embedList += [embeds.getUsrReplayMsgEmbed(message=message.content, user=message.author, pNum=message.author==i.players[0])]

    if message.channel.id == 1073359279827984455:
        await message.delete()

@bot.event
async def on_member_join(member):
    await member.add_roles(regularRole)

@bot.event
async def on_raw_reaction_add(payload):
    farkleCentral = bot.guilds[0]
    channel = discord.utils.get(farkleCentral.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    if str(payload.emoji) == '✅':
        for i in currentGames:
            if i.channel.id == payload.channel_id and i.type == 0 and i.state == 0:
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
    elif str(payload.emoji) == '🇶' and payload.channel_id == 1073359279827984455:
        await channel.send("potato")


@bot.slash_command(guild_ids=[1073319056083517551])
async def invite(ctx, user:discord.Option(discord.User, 'Dice amount', required=True)):
    global totalGames, currentGames
    if ctx.author == user:
        await ctx.respond(embed=embeds.getSelfChallengeErrEmbed(bot.user), ephemeral=True)
        return
    for i in currentGames:
        if ctx.author in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getSelfIngameEmbed(), ephemeral=True)
            return
        if user != bot.user and user in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getInvitedIngameEmbed(user), ephemeral=True)
            return
    await ctx.respond(embed=embeds.getChallengeCreationEmbed(user), ephemeral=True)
    await createUserGame(ctx.author, user, ctx, embeds.getInviteEmbed(ctx.author, user))

async def createUserGame(p1: discord.User, p2: discord.User, ctx, embed: discord.Embed):
    global totalGames, currentGames
    channel = await farkleCentral.create_text_channel(name=f'game-{str(totalGames).rjust(6, "0")}',
                                                      category=gamesCategory)
    await channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
    await channel.set_permissions(p1, read_messages=True, send_messages=False)
    await channel.set_permissions(p2, read_messages=True, send_messages=False)
    msg = await channel.send(embed=embed)
    await msg.add_reaction('✅')
    temp = FarkleGame(type=0, id=totalGames, state=0, players=(p1, p2), channel=channel, latestMsg=msg)
    currentGames += [temp]
    totalGames += 1
    temp2 = open('save.txt', 'w')
    temp2.write(str(totalGames))
    temp2.close()
    temp2 = await channel.send(f'{p1.mention}{p2.mention}')
    await temp2.delete()
    temp.task = asyncio.create_task(cancelUnreadyGame(temp, msg, channel, p1, p2))

async def cancelUnreadyGame(temp, msg, channel, p1, p2):
    try:
        await asyncio.sleep(45)
    except asyncio.CancelledError:
        return
    await msg.clear_reactions()
    await channel.send(embed=embeds.getReadyTimeoutEmbed(p1, p2))
    await temp.terminateGame(15)

bot.run(open('token.txt', 'r').read())