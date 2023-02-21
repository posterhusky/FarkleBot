import discord, images


def getGameRuleEmbeds():
    embed1 = discord.Embed(title='**Farkle Rules**', colour=discord.Colour.yellow(),
                           description='FARKLE is a push-your-luck game in which the objective is to be the first player to accumulate 10 000 points.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    embed2 = discord.Embed(title='**Gameplay**', colour=discord.Colour.yellow(),
                           description='The game is played with 6 dice and is turn based. Both players start at 0 points and obtain them by form scoring melds.')
    embed2.set_thumbnail(
        url=images.getImage(1))
    embed2.add_field(name='**🎲💰 Rolling, Scoring, Banking**',
                     value='A player starts their turn by throwing all 6 dice. After a throw, the player must set aside at least 1 meld and get score for it. After that the player can either finish their turn by banking all the score or re-roll the remaining dice.',
                     inline=False)
    embed2.add_field(name='**💰❌ Farkling**',
                     value='If there are no melds on the table after a throw, the player has "farkled" and lost the score gained during this turn.',
                     inline=True)
    embed2.add_field(name='**🎲🔥 Hot Dice**',
                     value='If melds can be formed from all the remaining dice, the player can re-roll all 6 dice or finish their turn by banking their score.',
                     inline=True)
    embed2.add_field(name='**💰🔥 High stakes**',
                     value='If a player farkles the other player can continue his turn and get all the points (or 1000 pts. if the turn score was smaller than 1000). However if the other player farkles on his first roll the high stake is failed! Upon a failed high the player looses the same amount of points form his bank as the amount of points in the turn score. A failed high steak can\'t be continued.',
                     inline=False)
    embed2.add_field(name='**➕💰 Multipliers**',
                     value='To seed up long games, every 5th turn the multiplier will be increased by 0,2x. It multiplies all score earned during a turn, however it is disabled if of players that have a 1,5K+ point lead. It is done to make comebacks easier, so watch out!',
                     inline=False)
    embed2.add_field(name='**💰👑 Game End**',
                     value='The game ends when a player that finished his turn has a total of 10 000 points or more.',
                     inline=False)
    embed3 = discord.Embed(title='**Melds**', colour=discord.Colour.yellow(),
                           description='Melds are specific combinations of dice that grant points when picked.')
    embed3.set_thumbnail(
        url=images.getImage(2))
    embed3.add_field(name=f'**<:die1:1073714606813483071> *- 100***',
                     value='1 die depicting a 1.',
                     inline=True)
    embed3.add_field(name=f'**<:die5:1073714599691550880> *- 50***',
                     value='1 die depicting a 5.',
                     inline=True)
    embed3.add_field(name=f'**<:dieRun:1073766074157371392> *- 2 500***',
                     value='All 6 die values present.',
                     inline=True)
    embed3.add_field(inline=False, name='', value='')
    embed3.add_field(name=f'**<:die1:1073714606813483071> × 3 *- 1 000***',
                     value='3 dice depicting 1.',
                     inline=True)
    embed3.add_field(name=f'**<:dieAny:1073725730392911972> × 3 *- 200-600***',
                     value='3 equal dice depicting 2-6.',
                     inline=True)
    embed3.add_field(name=f'**<:dieStack:1073775606510133259> × 3 *- 1 500***',
                     value='3 pairs of equal dice.',
                     inline=True)
    embed3.add_field(inline=False, name='', value='')
    embed3.add_field(name=f'**<:dieAny:1073725730392911972> × 4 *- 1 000***',
                     value='4 equal dice.',
                     inline=True)
    embed3.add_field(name=f'**<:dieAny:1073725730392911972> × 5 *- 2 000***',
                     value='5 equal dice.',
                     inline=True)
    embed3.add_field(name=f'**<:dieAny:1073725730392911972> × 6 *- 3 000***',
                     value='6 equal dice.',
                     inline=True)
    return embed1, embed2, embed3

def getServerRuleEmbeds():
    embed1 = discord.Embed(title='**Server rules**', colour=discord.Colour.yellow(),
                           description='Official server rules 100% real and very original! They\'re not really enforced but please follow them 🙄...')
    embed1.set_thumbnail(
        url=images.getImage(1))
    embed1.add_field(name='**☑ Speak mainly English**',
                     value='This is mainly an english-speaking server, so please write in english. (https://translate.google.com/?sl=auto&tl=en)',
                     inline=False)
    embed1.add_field(name='**☑ Respect everyone**',
                     value='Respect everyone. Don\'t insult or harass other users.',
                     inline=False)
    embed1.add_field(name='**☑ Keep it sfw**',
                     value='Hide stuff that you think is nsfw under a spoiler, or better, just don\'t post it. This includes usernames and other profile info.',
                     inline=False)
    embed1.add_field(name='**☑ Don\'t ping**',
                     value='Please don\'t ping people for no apparent reason. If you don\'t like recieving pings, you can turn off invites in <#1076954499421319198>.',
                     inline=False)
    embed1.add_field(name='**☑ Keep it in topic**',
                     value='<#1077318483777437758> is a general chat without a specific topic, however the threads of this chat generally have a topic that you should consider respecting. You can reate your own thread with any topic if you want.',
                     inline=False)
    embed1.add_field(name='**A thing to note is that the project crew is able to mute anyone they want.\nYou can find the rules of the game in <#1073356373515042897>\nHave Fun!**', value='', inline=False)
    return embed1

def getNewGameEmbeds(self):
    embed1 = discord.Embed(title='**How to start a new game?**', colour=discord.Colour.green(),
                           description='There\'s 3 options to start a new game:')
    embed1.add_field(name='**Invite a friend**',
                     value='Use the */invite <tag>* command in this channel to invite someone to a farkle game. As soon as you run it, a new private channel with further information will appear.',
                     inline=False)
    embed1.add_field(name='**Play against AI**',
                     value=f'Use the */invite {self.mention}* command in this channel to play against AI. As soon as you run it, a new channel private will be created in this category with the game already launched.',
                     inline=False)
    embed1.add_field(name='**Public queue**',
                     value=f'To join the queue, react under the public queue embed (see below). As soon as 2 people will simultaneously be in the queue, a new private channel with further information will appear.',
                     inline=False)
    embed1.set_thumbnail(
        url=images.getImage(0))
    embed2 = discord.Embed(title='**Important!**', colour=discord.Colour.red(), description='Here are a few important thing to mention:')
    embed2.add_field(name='**You can only play 1 game at a time**',
                     value=f'To prevent spam and bot exploits, you will not be able to use the /invite command or join the queue if you are in-game. Also, you can\'t invite someone in-game.',
                     inline=False)
    embed2.add_field(name='**Queue kick time**',
                     value=f'To confirm that you\'re still here, you will be removed from the queue every so often and get pinged. If you join the queue within 30 seconds of the ping, your kick time will be doubled up to 16 minutes.',
                     inline=False)
    embed2.add_field(name='**This channel is command-only**',
                     value=f'This channel is not for chatting, all messages sent here will be deleted.',
                     inline=False)
    embed2.set_thumbnail(
        url=images.getImage(1))
    embed3 = discord.Embed(title='**Public queue**', colour=discord.Colour.blue(),
                           description='React with 🇶 to join the public queue. You will be pinged as soon as there will be enough players. Also, be aware of queue kick time (see above).')
    embed3.set_thumbnail(
        url=images.getImage(2))
    return embed1, embed2, embed3

def getBlockInvitesEmbed():
    embed1 = discord.Embed(title=f'**Disable invites**', colour=discord.Colour.blue(),
                           description=f'Prevents all players from inviting you.\n\nAdd a reaction to enable this option.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getAnnouncementPingEmbed():
    embed1 = discord.Embed(title=f'**Announcement ping**', colour=discord.Colour.blue(),
                           description=f'Enable if you want to get pinged on an announcement.\n\nAdd a reaction to enable this option.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getQueuePingEmbed():
    embed1 = discord.Embed(title=f'**Queue ping**', colour=discord.Colour.blue(),
                           description=f'Enable if you want to get pinged when someone joins the queue.\n\nAdd a reaction to enable this option.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getChallengeCreationEmbed(destUsr):
    embed1 = discord.Embed(title=f'**Starting game...**', colour=discord.Colour.blue(),
                           description=f'You have invited {destUsr.mention} to a game.\n\nThe game is now setting up, please wait...')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getAiGameStartingEmbed():
    embed1 = discord.Embed(title=f'**Starting game...**', colour=discord.Colour.blue(),
                           description=f'You have started a game against AI.\n\nThe game is now setting up, please wait...')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getQueueJoinEmbed():
    embed1 = discord.Embed(title=f'**Joined the queue!**', colour=discord.Colour.blue(),
                           description=f'You have joined the queue! A game will start as soon as there will be 2 players in the queue. To leave the queue, remove the reaction.\n\nTo confirm your presence, you will be kicked in **10 minutes** and will recieve a dm notifiying you about this.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getQueueLeaveEmbed():
    embed1 = discord.Embed(title=f'**Left the queue!**', colour=discord.Colour.blue(),
                           description=f'You have left the queue! If you can\'t find players, try asking in the chat!')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getQueueKickEmbed():
    embed1 = discord.Embed(title=f'**You have been kicked from the queue!**', colour=discord.Colour.blue(),
                           description=f'You have have been kicked from the queue. If you\'re still interested in joining a farkle game, react under the queue message.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getSelfChallengeErrEmbed(destUsr):
    embed1 = discord.Embed(title=f'**You can\'t invite yourself!**', colour=discord.Colour.red(),
                           description=f'Unfortunately, you can\'t play a game with yourself *(for now...)*.\n\nIf you want, you can play against me!\n*/invite user: {destUsr.mention} *')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getReadyTimeoutEmbed(p1, p2):
    embed1 = discord.Embed(title=f'**Time\'s up!**', colour=discord.Colour.red(),
                           description=f'The game between {p1.mention} and {p2.mention} has failed!\n\nUnfortunately, both players weren\'t ready in time.\n\nThis game will be deleted in **15 seconds**.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getGiveUpEmbed(user, pNum):
    embed1 = discord.Embed(title=f'**P{int(pNum)+1} gave up!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'{user.mention} gave up!\n\nThis game will be deleted in **15 seconds**, you can save the replay if you need it.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getInteractionTimeoutEmbed(user):
    embed1 = discord.Embed(title=f'**Time\'s up!**', colour=discord.Colour.red(),
                           description=f'The game was terminated due to {user.mention} idling!\n\nThis game will be deleted in **15 seconds**, you can save the replay if you need it.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getInvitedIngameEmbed(destUsr):
    embed1 = discord.Embed(title=f'**This user is already in-game!**', colour=discord.Colour.red(),
                           description=f'You can\'t invite {destUsr.mention} since this user is already in-game.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getHasDisabledInvitesEmbed(destUsr):
    embed1 = discord.Embed(title=f'**This user disabled invites!**', colour=discord.Colour.red(),
                           description=f'You can\'t invite {destUsr.mention} since they chose to block all the invites.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getSelfIngameEmbed():
    embed1 = discord.Embed(title=f'**You are already in-game!**', colour=discord.Colour.red(),
                           description=f'You can\'t send invites while you\'re in-game.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getNotYourTurnEmbed():
    embed1 = discord.Embed(title=f'**It\'s not your turn.**', colour=discord.Colour.red(),
                           description=f'You can\'t use the interactions while it\'s not your turn.\n\nHowever, you can use the *give up* button at any time.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getIdleTimeoutExtendedEmbed():
    embed1 = discord.Embed(title=f'**Reset idle timer.**', colour=discord.Colour.blue(),
                           description=f'The idle timer was reset back to 1 minute.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getInviteEmbed(p1, p2):
    embed1 = discord.Embed(title=f'**Game invitation!**', colour=discord.Colour.green(),
                           description=f'{p1.mention} has invited {p2.mention} to a farkle game!\n\nReady-up as the game is about to begin!\n\nReact with ✅ to get into ready mode. The game will start as soon as both players are ready!\n\nThe invite is valid for **45 seconds**.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getQueueGameEmbed(p1, p2):
    embed1 = discord.Embed(title=f'**Queue complete!**', colour=discord.Colour.green(),
                           description=f'There was enough players waiting in the queue to start a game!\n\n{p1.mention} VS {p2.mention}\n\nReady-up as the game is about to begin!\n\nReact with ✅ to get into ready mode. The game will start as soon as both players are ready!\n\nThe invite is valid for **45 seconds**.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getBothReadyEmbed(destUsr, p1, p2):
    embed1 = discord.Embed(title=f'**Starting the game...**', colour=discord.Colour.green(),
                           description=f'Both players are ready! Starting the game...\n\nP1: {p1.mention}\nP2: {p2.mention}\n\n{destUsr.mention} starts!')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getAiGameReadyEmbed(player):
    embed1 = discord.Embed(title=f'**Game created!**', colour=discord.Colour.green(),
                           description=f'The game against an AI was successfully created! Please note that you will still not be able to join the queue or invite someone during this game.\n\nP1: {player.mention}\nP2: Farkle bot\n\nYou start!')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getMultiplierIncrEmbed(turns, multiplier):
    embed1 = discord.Embed(title=f'**Multiplier increased!**', colour=discord.Colour.blue(),
                           description=f'The game was going on for {turns} turns and the multiplier was increased by **0,2x**!\n\n**Current multiplier: *{multiplier}x***')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getTurnRecap(destUsr, p1Bank, p2Bank, turnBank, qty, pNum, history):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    embed1.add_field(name='**Turn history:**', value='', inline=False)
    if history == []:
        embed1.add_field(name='Nothing here yet...', value='', inline=False)
    else:
        for n, i in enumerate(history):
            embed1.add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    embed1.add_field(name='', value='', inline=False)
    embed1.add_field(name='**P1\'s bank:**', value=p1Bank, inline=True)
    embed1.add_field(name='**P2\'s bank:**', value=p2Bank, inline=True)
    embed1.add_field(name='**Turn score:**', value=turnBank, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    return embed1

def getStartTurnEmbed(mlt, lead, stake, pNum):
    embed1 = discord.Embed(title=f'**It\'s dice rolling time!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Your turn just started! You can roll the dice or... roll the dice!')
    if stake != None:
        embed1.add_field(
            name=f'You can do a high stake for *{stake[0]} pts.*',
            value='',
            inline=False)
    if lead:
        embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your 1,5K+ lead.', value='',
                         inline=False)
    else:
        embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                         inline=False)
    embed1.add_field(name='The game will be terminated if you won\'t react within **1 minute**!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHighStakesEmbed(mlt, iconList, iconList2, lead, pts, pNum):
    embed1 = discord.Embed(title=f'**High stakes!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'You chose to continue the turn of your opponent! You got *{pts} pts.* and can now roll the dice. However, if you farkle this turn, you\'ll loose *{pts} pts.* so watch out!')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if lead:
        embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score gain because of your 1,5K+ lead (still applied on point loss).', value='',
                         inline=False)
    else:
        embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                         inline=False)
    embed1.add_field(name='The game will be terminated if you won\'t react within **1 minute**!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHotDiceEmbed(pts, iconList, mlt, lead, pNum):
    embed1 = discord.Embed(title=f'**Hot dice!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'{" ".join(iconList)} *- {pts} pts.*\nAll the dice were automatically melded! You can now re-roll all 6 dice again.')
    if lead:
        embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your 1,5K+ lead.', value='',
                         inline=False)
    else:
        embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                         inline=False)
    embed1.add_field(name='The game will be terminated if you won\'t react within **1 minute**!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getFarkledEmbed(turnBank, iconList, pNum):
    embed1 = discord.Embed(title=f'**You got farkled!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'{" ".join(iconList)}\nMelds can\'t be formed from the remaining dice! The score you earned this turn will be lost.\n\nPoints lost *- {turnBank} pts.*')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getFailedHighStakeEmbed(turnBank, iconList, pts, pNum):
    embed1 = discord.Embed(title=f'**High stake failed!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You got farkled... and lost the high stake.\n\n{" ".join(iconList)}\nMelds can\'t be formed from the remaining dice! The score you earned this turn will be lost.\n\n*{pts} pts.* were removed from your bank!')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getScoreBankedEmbed(turnBank, pNum):
    embed1 = discord.Embed(title=f'**Score banked!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You finished your turn and banked the score you earned during it.\n\nPoints banked *- {turnBank}*')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getAfterRollEmbed(iconList, iconList2, mlt, lead, pNum):
    embed1 = discord.Embed(title=f'**You rolled the dice!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You rolled the dice, see which melds you can make form them by looking at the interactions. The best meld available is highlighted in purple.')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if lead:
        embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your 1,5K+ lead.', value='',
                         inline=False)
    else:
        embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                         inline=False)
    embed1.add_field(name='The game will be terminated if you won\'t react within **1 minute**!', value='',
                     inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1
def getAfterMeldEmbed(iconList, iconList2, meld, mlt, lead, pNum):
    embed1 = discord.Embed(title=f'**Meld successful!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You melded **{meld[3]} × {meld[1]}** and got *{meld[2]} pts.* You can now select another meld, roll the dice or bank your score!')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if lead:
        embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your 1,5K+ lead.', value='',
                         inline=False)
    else:
        embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                         inline=False)
    embed1.add_field(name='The game will be terminated if you won\'t react within **1 minute**!', value='',
                     inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getWinEmbed(winner, turns, pNum):
    embed1 = discord.Embed(title=f'**P{pNum+1} WON THE GAME!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Congratulations, {winner.mention}, you won this game in {turns} turns!\n\nThis game will be deleted in **30 seconds**, you can save the replay if you need it.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getUsrReplayMsgEmbed(user, message, pNum):
    embed1 = discord.Embed(title=f'**Player message:**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description=f'{user.mention}: {message}')
    return embed1

def getReplayEmbed():
    embed1 = discord.Embed(title=f'**GAME OVER!**', colour=discord.Colour.yellow(),
                           description=f'Thanks for playing!\n\nYou can save the replay of this game by clicking the interaction below this message.')
    embed1.set_thumbnail(url=images.getImage(2))
    return embed1

def getGiveUpConfirmEmbed():
    embed1 = discord.Embed(title=f'**Are you sure?**', colour=discord.Colour.red(),
                           description=f'You are about to give up and quit the game, please confirm that this action is intentional.')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getHurryUpEmbed(user):
    embed1 = discord.Embed(title=f'**Hurry up!**', colour=discord.Colour.red(),
                           description=f'It\'s {user.mention}\'s turn!\n\nThe game will terminate in 15. If you need more time to think, press the "Reset idle timer" button (active for both players).')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1