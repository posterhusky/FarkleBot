import discord, random, embeds, asyncio, idList, emojis, time, replayFunctions, gameFunctions
from discord.ui import View, Button

print('starting bot...')

bot = discord.Bot(intents=discord.Intents().all())
farkleCentral, regularRole, adminRole, gamesCategory, replaysCategory, qDisplayChannel, qChannel, qMessage, prefChannel, pref1Msg, pref2Msg, pref3Msg, annPingRole, qPingRole, savesChannel, totalGamesMsg, replaysChannel, eChannel, eMsg, *_ = [None] * 50

totalGames = 0
currentGames = []
queue = []
eventQueue = []
eventBuffer = []
liveEvent = 0

async def createAiEventGame(interaction: discord.Interaction):
    for i in currentGames:
        if interaction.user in i.players and i.state != 2:
            await interaction.response.send_message(embed=embeds.getSelfIngameEmbed(), ephemeral=True)
            return
    await interaction.response.send_message(embed=embeds.getAiGameStartingEmbed(), ephemeral=True)
    await createAiGame(player=interaction.user, startMultiplier=1, multiplierQuantity=5,
                       multiplierQuality=0.2, leadAmount=1500, goal=10000, event=liveEvent)

dice = [emojis.die1, emojis.die2, emojis.die3, emojis.die4, emojis.die5, emojis.die6]

currentDay = int(time.time()) // 86400


class QueuedPerson():
    def __init__(self, user: discord.user):
        self.user = user
        self.task = asyncio.create_task(self.kickQueuedMember())

    async def kickQueuedMember(self):
        try:
            await asyncio.sleep(600)
        except:
            return
        print('user got kicked from queue:', self.user.name)
        await qMessage.remove_reaction(emoji='🇶', member=self.user)
        await self.user.send(embed=embeds.getQueueKickEmbed(), silent=True)
        while self in queue:
            queue.remove(self)

    async def instantKickQueuedMember(self):
        print('user got removed from queue:', self.user.name)
        await qMessage.remove_reaction(emoji='🇶', member=self.user)
        await self.user.send(embed=embeds.getQueueKickEmbed(), silent=True)
        while self in queue:
            queue.remove(self)


#
# === === === === === === === === === === === === === === === === === === ===
#
# EVENTS
#
# === === === === === === === === === === === === === === === === === === ===
#
# === === === === === === === === === === === === === === === === === === ===
#
# === === === === === === === === === === === === === === === === === === ===
#

@bot.event
async def on_ready():
    global farkleCentral, regularRole, adminRole, gamesCategory, replaysCategory, totalGames, qDisplayChannel, qChannel, qMessage, prefChannel, pref1Msg, pref2Msg, pref3Msg, annPingRole, qPingRole, savesChannel, totalGamesMsg, replaysChannel, eChannel, eMsg, liveEvent, eventBuffer, currentDay
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
    eChannel = discord.utils.get(farkleCentral.channels, id=idList.eChannel)
    prefChannel = discord.utils.get(farkleCentral.channels, id=idList.prefChannel)
    savesChannel = discord.utils.get(farkleCentral.channels, id=idList.savesChannel)
    await qDisplayChannel.edit(name=f'Queued members: {len(queue)}')
    qMessage = await qChannel.fetch_message(idList.queueMsg)
    pref1Msg = await prefChannel.fetch_message(idList.pref1Msg)
    pref2Msg = await prefChannel.fetch_message(idList.pref2Msg)
    pref3Msg = await prefChannel.fetch_message(idList.pref3Msg)
    eMsg = await eChannel.fetch_message(idList.eMsg)
    totalGamesMsg = await savesChannel.fetch_message(idList.totalGamesMsg)
    replaysChannel = discord.utils.get(farkleCentral.channels, id=idList.replayChannel)
    print(totalGamesMsg.content)
    totalGames = int(totalGamesMsg.content)
    gameFunctions.init(farkleCentralArg=farkleCentral, replaysChannelArg=replaysChannel,
                       botArg=bot, currentGamesArg=currentGames,
                       regularRoleArg=regularRole, replaysCategoryArg= replaysCategory)
    await replayFunctions.readReplayData(replaysChannel=replaysChannel, farkleCentral=farkleCentral)
    liveEvent = random.randint(0, 5)
    eventBuffer = [liveEvent]
    aiEventGameBtn = Button(label='Play against AI', emoji='🤖', style=discord.ButtonStyle.blurple)
    aiEventGameBtn.callback = createAiEventGame
    aiEventGameView = View()
    aiEventGameView.add_item(aiEventGameBtn)
    await eMsg.edit(embeds=embeds.getEventChannelEmbeds(liveEvent, (currentDay + 1) * 86400), view=aiEventGameView)
    print('changing event to', liveEvent, 'with buffer containing', eventBuffer)
    while 1:
        await asyncio.sleep(600)
        print(f'checking day: {currentDay}days vs {int(time.time()) // 86400}now')
        if currentDay != int(time.time()) // 86400:
            currentDay = int(time.time()) // 86400
            while liveEvent in eventBuffer:
                liveEvent = random.randint(0, 5)
            eventBuffer = [eventBuffer[-1], liveEvent]
            print('changing event to', liveEvent, 'with buffer containing', eventBuffer)
            await eMsg.edit(embeds=embeds.getEventChannelEmbeds(liveEvent, (currentDay + 1) * 86400), view=aiEventGameView)


@bot.event
async def on_message(message: discord.Message):
    global liveEvent, eventBuffer
    if message.author == bot.user:
        return
    if isinstance(message.author, discord.User):
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
        elif message.content == '$eventdisplay':
            i = await message.channel.send(embeds=embeds.getEventChannelEmbeds(0, (currentDay + 1)*86400))
            print(message.id)
            await i.add_reaction('🇶')
        elif message.content == '$eventrefresh':
            while liveEvent in eventBuffer:
                liveEvent = random.randint(0, 5)
            eventBuffer = [eventBuffer[-1], liveEvent]
            print('changing event to', liveEvent, 'with buffer containing', eventBuffer, 'as requested by', message.author.name)
            aiEventGameBtn = Button(label='Play against AI', emoji='🤖', style=discord.ButtonStyle.blurple)
            aiEventGameBtn.callback = createAiEventGame
            aiEventGameView = View()
            aiEventGameView.add_item(aiEventGameBtn)
            await eMsg.edit(embeds=embeds.getEventChannelEmbeds(liveEvent, (currentDay + 1) * 86400), view=aiEventGameView)
        elif message.content[:-1] == '$react':
            if message.reference != None:
                i = await message.channel.fetch_message(message.reference.message_id)
                await i.add_reaction(message.content[-1])
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
            await message.channel.send('stopping...')
            print('stopping bot as requested by', message.author.name)
            try: await bot.close()
            except: pass

    for i in currentGames:
        if i.channel == message.channel:
            i.embedList += [embeds.getUsrReplayMsgEmbed(message=message.content, user=message.author,
                                                        pNum=message.author == i.players[0])]

    if message.channel.id == idList.newGameChannel:
        await message.delete()
        return

    for i in replayFunctions.replays:
        if i.channel == message.channel:
            await message.delete()
            return


@bot.event
async def on_member_join(member):
    await member.add_roles(regularRole)


@bot.event
async def on_raw_reaction_add(payload):
    global queue, pref2Msg, eventQueue
    farkleCentral = bot.guilds[0]
    channel = discord.utils.get(farkleCentral.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    print('reaction added:', channel.name, message.content, payload.emoji, payload.member.name)
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
                    await i.startGame()
                break
    elif str(payload.emoji) == '🇶' and payload.channel_id in [idList.newGameChannel, idList.eChannel]:
        print('player joined normal queue:' if payload.channel_id == idList.newGameChannel else 'player joined event queue:', payload.member.name)
        for i in currentGames:
            if payload.member in i.players:
                print('but was removed due to being in-game:', payload.member.name, 'in', i.players[0], 'vs',
                      i.players[1])
                await message.remove_reaction(emoji='🇶', member=payload.member)
                return
        for i in queue + eventQueue:
            if payload.member == i.user:
                print('but was removed due to being in-queud:', payload.member.name)
                await message.remove_reaction(emoji='🇶', member=payload.member)
                return
        await payload.member.send(embed=embeds.getQueueJoinEmbed(), silent=True)
        if payload.channel_id == idList.newGameChannel:
            queue += [QueuedPerson(user=payload.member)]
            if len(queue) >= 2:
                await createUserGame(p1=queue[0].user, p2=queue[1].user,
                                     embed=embeds.getQueueGameEmbed(queue[0].user, queue[1].user,
                                                                    time=int(time.time()) + 120), leadAmount=1500,
                                     startMultiplier=1.0, multiplierQuality=0.2, multiplierQuantity=5, goal=10000)
                await message.remove_reaction(emoji='🇶', member=queue[0].user)
                await message.remove_reaction(emoji='🇶', member=queue[1].user)
                print('Queue full, starting game:')
                for i in queue:
                    i.task.cancel()
                queue = []
            else:
                temp = await channel.send(qPingRole.mention)
                await temp.delete()
        else:
            eventQueue += [QueuedPerson(user=payload.member)]
            if len(eventQueue) >= 2:
                await createUserGame(p1=eventQueue[0].user, p2=eventQueue[1].user,
                                     embed=embeds.getQueueGameEmbed(eventQueue[0].user, eventQueue[1].user,
                                                                    time=int(time.time()) + 120), leadAmount=1500,
                                     startMultiplier=1.0, multiplierQuality=0.2, multiplierQuantity=5, goal=10000, event=liveEvent)
                await message.remove_reaction(emoji='🇶', member=eventQueue[0].user)
                await message.remove_reaction(emoji='🇶', member=eventQueue[1].user)
                print('Queue full, starting game:')
                for i in eventQueue:
                    i.task.cancel()
                eventQueue = []
            else:
                temp = await channel.send(qPingRole.mention)
                await temp.delete()
        await qDisplayChannel.edit(name=f'Queued members: {len(queue + eventQueue)}')


@bot.event
async def on_raw_reaction_remove(payload):
    global queue
    channel = discord.utils.get(farkleCentral.channels, id=payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = discord.utils.get(farkleCentral.members, id=payload.user_id)
    print('reaction removed:', channel.name, message.content, payload.emoji, member.name)
    if channel == prefChannel:
        if payload.message_id == idList.pref2Msg:
            await member.remove_roles(annPingRole)
        elif payload.message_id == idList.pref3Msg:
            await member.remove_roles(qPingRole)
        return
    if str(payload.emoji) == '🇶' and payload.channel_id in [idList.newGameChannel, idList.eChannel]:
        print('player left the queue:', member.name)
        for i in queue+eventQueue:
            if i.user == member:
                i.task.cancel()
                if i in queue: queue.remove(i)
                if i in eventQueue: eventQueue.remove(i)
                break
        else:
            return  # in case a player got kicked (was already removed in QueuedUser.kickQueuedMember())
        await member.send(embed=embeds.getQueueLeaveEmbed(), silent=True)
        await qDisplayChannel.edit(name=f'Queued members: {len(queue)}')


@bot.slash_command(name='invite', guild_ids=[idList.farkleCentralId], description='Invite your friend to a farkle game')
async def invite(ctx,
                 user: discord.Option(discord.User, 'The user you want to invite', required=True),
                 goal: discord.Option(int, 'The amount of points needed to win the game', default=10000),
                 lead_amount: discord.Option(int,
                                             'The amount of point lead needed to disable the multiplier (set to 0 to disable)',
                                             default=1500),
                 multiplier_start: discord.Option(float, 'The multiplier value on start', default=1.0),
                 multiplier_quality: discord.Option(float, 'By how much the multiplier should increase', default=0.2),
                 multiplier_quantity: discord.Option(int, 'How often the multiplier should increase (in turns)',
                                                     default=5)
                 ):
    if goal <= 0:
        goal = 10000
    if multiplier_start <= 0:
        multiplier_start = 1.0
    if multiplier_quality < 0:
        multiplier_quality = 0.2
    if multiplier_quantity <= 0:
        multiplier_quantity = 5
    global totalGames, currentGames
    if ctx.author == user:
        await ctx.respond(embed=embeds.getSelfChallengeErrEmbed(bot.user), ephemeral=True)
        return
    for i in currentGames:
        if ctx.author in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getSelfIngameEmbed(), ephemeral=True)
            return
        if user in i.players and i.state != 2:
            await ctx.respond(embed=embeds.getInvitedIngameEmbed(user), ephemeral=True)
            return
    if user == bot.user:
        await ctx.respond(embed=embeds.getAiGameStartingEmbed(), ephemeral=True)
        await createAiGame(player=ctx.author, startMultiplier=multiplier_start, multiplierQuantity=multiplier_quantity,
                           multiplierQuality=multiplier_quality, leadAmount=lead_amount, goal=goal)
        return
    users = []
    async for user1 in pref1Msg.reactions[0].users():
        users += [user1]
    if user in users:
        await ctx.respond(embed=embeds.getHasDisabledInvitesEmbed(user), ephemeral=True)
        return
    await ctx.respond(embed=embeds.getChallengeCreationEmbed(user), ephemeral=True)
    await createUserGame(ctx.author, user, embeds.getInviteEmbed(ctx.author, user, time=int(time.time())+120), startMultiplier=multiplier_start,
                         multiplierQuantity=multiplier_quantity, multiplierQuality=multiplier_quality,
                         leadAmount=lead_amount, goal=goal)


@bot.slash_command(name='share', guild_ids=[idList.farkleCentralId], description='Share you replay with a friend')
async def share(ctx, user: discord.Option(discord.User, 'The user you want to start/stop sharing the replay',
                                           required=True),
                 status: discord.Option(bool, 'True if you want to add the user, False if you want to remove the user',
                                        required=True)):
    for i in replayFunctions.replays:
        if i.channel == ctx.channel:
            if status:
                await i.addMember(user=user)
                await ctx.respond(embed=embeds.getReplaySharedEmbed(user=user), ephemeral=True)
                return
            await i.removeMember(user=user)
            await ctx.respond(embed=embeds.getReplaySharedEmbed(user=user), ephemeral=True)
            return
    await ctx.respond(embed=embeds.getNotInReplayChannelEmbed(), ephemeral=True)


async def createAiGame(player, startMultiplier: float, multiplierQuantity: int, multiplierQuality: float,
                       leadAmount: int, goal: int, event: int = 6):
    global totalGames, currentGames
    for i in queue + eventQueue:
        if i.user == player:
            await i.instantKickQueuedMember()
    channel = await farkleCentral.create_text_channel(name=f'game-{totalGames}', category=gamesCategory)
    await channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
    await channel.set_permissions(player, read_messages=True, send_messages=False)
    gameTypes = [gameFunctions.ScoreAttackGame, gameFunctions.SnowballGame, gameFunctions.HotPotatoGame,
                 gameFunctions.TugOfWarGame, gameFunctions.MysteryDieGame, gameFunctions.BountyGame, gameFunctions.NormalGame]
    temp = gameTypes[event](id=totalGames, state=1, players=(player, bot.user), channel=channel, startMultiplier=startMultiplier,
                      multiplierQuantity=multiplierQuantity, multiplierQuality=multiplierQuality, leadAmount=leadAmount,
                      goal=goal)
    currentGames += [temp]
    totalGames += 1
    await totalGamesMsg.edit(f'{totalGames}')
    await temp.startGame()


async def createUserGame(p1: discord.User, p2: discord.User, embed: discord.Embed, startMultiplier: float,
                         multiplierQuantity: int, multiplierQuality: float, leadAmount: int, goal: int, event: int = 6):
    global totalGames, currentGames
    for i in queue + eventQueue:
        if i.user in [p1, p2]:
            await i.instantKickQueuedMember()
    channel = await farkleCentral.create_text_channel(name=f'game-{totalGames}',
                                                      category=gamesCategory)
    await channel.set_permissions(farkleCentral.default_role, read_messages=False, send_messages=False)
    await channel.set_permissions(regularRole, read_messages=False, send_messages=False)
    await channel.set_permissions(p1, read_messages=True, send_messages=False)
    await channel.set_permissions(p2, read_messages=True, send_messages=False)
    msg = await channel.send(embed=embed)
    temp = await channel.send(f'{p1.mention}{p2.mention}')
    await temp.delete()
    await msg.add_reaction('✅')
    gameTypes = [gameFunctions.ScoreAttackGame, gameFunctions.SnowballGame, gameFunctions.HotPotatoGame,
                 gameFunctions.TugOfWarGame, gameFunctions.MysteryDieGame, gameFunctions.BountyGame, gameFunctions.NormalGame]
    temp = gameTypes[event](id=totalGames, state=0, players=(p1, p2), channel=channel,
                      startMultiplier=startMultiplier, multiplierQuantity=multiplierQuantity,
                      multiplierQuality=multiplierQuality, leadAmount=leadAmount, goal=goal)
    currentGames += [temp]
    totalGames += 1
    await totalGamesMsg.edit(f'{totalGames}')
    temp.task = asyncio.create_task(cancelUnreadyGame(temp, msg, channel, p1, p2))


async def cancelUnreadyGame(temp, msg, channel, p1, p2):
    try:
        await asyncio.sleep(120)
    except asyncio.CancelledError:
        return
    await msg.clear_reactions()
    await channel.send(embed=embeds.getReadyTimeoutEmbed(p1, p2, time=int(time.time())+15))
    await temp.terminateGame(15)


f = open('token.txt', 'r')
token = f.read()
f.close()

bot.run(token)
print('The bot is stopped. Type anything.')
input()
print('You\'ve quit, end of program.')
