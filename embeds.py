import discord, images, emojis


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
    embed3.add_field(name=f'**{emojis.die1} *- 100***',
                     value='1 die depicting a 1.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.die5} *- 50***',
                     value='1 die depicting a 5.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.dieRun} *- 2 500***',
                     value='All 6 die values present.',
                     inline=True)
    embed3.add_field(inline=False, name='', value='')
    embed3.add_field(name=f'**{emojis.die1} × 3 *- 1 000***',
                     value='3 dice depicting 1.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.dieAny} × 3 *- 200-600***',
                     value='3 equal dice depicting 2-6.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.diePair} × 3 *- 1 500***',
                     value='3 pairs of equal dice.',
                     inline=True)
    embed3.add_field(inline=False, name='', value='')
    embed3.add_field(name=f'**{emojis.dieAny} × 4 *- 1 000***',
                     value='4 equal dice.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.dieAny} × 5 *- 2 000***',
                     value='5 equal dice.',
                     inline=True)
    embed3.add_field(name=f'**{emojis.dieAny} × 6 *- 3 000***',
                     value='6 equal dice.',
                     inline=True)
    return embed1, embed2, embed3

def getServerRuleEmbeds():
    embed1 = discord.Embed(title='**Server rules**', colour=discord.Colour.yellow(),
                           description='Official server rules 100% real and very original! They\'re not really enforced but please follow them 🙄...')
    embed1.set_thumbnail(
        url=images.getImage(1))
    embed1.add_field(name='**☑ Speak mainly English**',
                     value='This is mainly an English-speaking server, so please write in English. (https://translate.google.com/?sl=auto&tl=en)',
                     inline=False)
    embed1.add_field(name='**☑ Respect everyone**',
                     value='Respect everyone. Don\'t insult or harass other users.',
                     inline=False)
    embed1.add_field(name='**☑ Keep it SFW**',
                     value='Hide stuff that you think is NSFW under a spoiler, or better, just don\'t post it. This includes usernames and other profile info.',
                     inline=False)
    embed1.add_field(name='**☑ Don\'t spam**',
                     value='Don\'t send repetitive messages too often in chats as well as in the sections for bot commands.',
                     inline=False)
    embed1.add_field(name='**☑ Don\'t overload the bot**',
                     value='If one of the bot\'s interactions or commands doesn\'t work, please wait for a few seconds before using it again.',
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
                     value=f'To confirm that you\'re still here, you will be removed from the queue every so often and get pinged.',
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

def getEventChannelEmbeds(event: int, time: int):
    match event:
        case 0: # score attack
            embed1 = discord.Embed(title='**SCORE ATTACK MODE**', colour=discord.Colour.green(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**Score attack:**', value=f'*500 pts.* are removed every turn.', inline=False)
            embed1.add_field(name='**Win condition:**', value=f'The player that finishes a turn with a negative bank looses.', inline=False)
            embed1.add_field(name='**Score cap:**', value=f'You can only have *5000 pts.* in your bank.', inline=False)
            embed1.add_field(name='**Also, there\'s no multipliers or high stakes in this mode.**', value=f'', inline=False)
        case 1:  # snowball
            embed1 = discord.Embed(title='**SNOWBALL MODE**', colour=discord.Colour.blue(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**Common bank:**', value=f'Bot players have a common bank.', inline=False)
            embed1.add_field(name='**Win condition:**',
                             value=f'To win, the bank should be at EXACTLY *5K pts.* The turn score is undone if the bank exceeds the limits', inline=False)
            embed1.add_field(name='**Also, there\'s no multipliers or high stakes in this mode.**', value=f'', inline=False)
        case 2:  # hot potato
            embed1 = discord.Embed(title='**HOT POTATO MODE**', colour=discord.Colour.orange(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**1 meld only:**', value=f'After rolling the dice, you can only pick 1 meld which goes directly to your bank.', inline=False)
            embed1.add_field(name='**Farkle:**', value=f'If you farkle, you loose *500 pts.*', inline=False)
            embed1.add_field(name='**Pass turn:**', value=f'You have the option to pass the turn to the other player for *250 pts.*', inline=False)
            embed1.add_field(name='**Win condition:**', value=f'The player that finishes a turn with a negative bank looses.', inline=False)
            embed1.add_field(name='**Also, there\'s no multipliers or high stakes in this mode.**', value=f'', inline=False)
        case 3:  # tug of war
            embed1 = discord.Embed(title='**TUG OF WAR MODE**', colour=discord.Colour.red(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**Point stealing:**', value=f'All the points you earn are stolen from the opponent\'s bank.', inline=False)
            embed1.add_field(name='**Win condition:**', value=f'The player with a negative bank upon a turn finish looses.', inline=False)
            embed1.add_field(name='**Also, there\'s no high stakes in this mode.**', value=f'', inline=False)
        case 4:  # mystery die
            embed1 = discord.Embed(title='**MYSTERY DIE MODE**', colour=discord.Colour.magenta(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**Mystery die:**', value=f'At the start of a turn the opponent has an option to roll the mystery die. If rolled, it give the turn a random modifier that is only shown to the opponent.', inline=False)
            embed1.add_field(name='**Mystery die values:**', value='**⬇ Heavy pockets:** *100pts.* removed form bank for every die in the inventory\n'
                                                                   '**⬇ Double trouble:** The banked score is added to the opponent\'s bank as well\n'
                                                                   '**⬇ Rounding error:** Banked score is rounded down to the nearest *500* multiple\n'
                                                                   '**⬆ Farkle shield:** *50%* of the turn score is banked upon a farkle.\n'
                                                                   '**⬆ Banking bonus:** *10%* of the bank are added on top of the banked score\n'
                                                                   '**⬆ Point transfer:** *50%* of the banked score is taken from the opponent\'s bank', inline=False)
            embed1.add_field(name='**Also, there\'s no high stakes in this mode.**', value=f'', inline=False)
        case _:  # bounty
            embed1 = discord.Embed(title='**BOUNTY MODE**', colour=discord.Colour.yellow(),
                                   description='It plays like a normal farkle game except a few twists:')
            embed1.add_field(name='**No melds:**', value=f'There aren\'t any specific melds in this mode: you can only meld 1 die at a time for *0 pts.* The only way to get points is to roll bounties.', inline=False)
            embed1.add_field(name='**Bounty:**', value=f'There are 3 bounties for different poins. Bounties change after you collect them to keep the game fresh.', inline=False)
            embed1.add_field(name='**Win condition:**', value=f'You have to get *5000 pts.* in your bank to win.', inline=False)
            embed1.add_field(name='**Also, there\'s no multipliers or high stakes in this mode.**', value=f'',
                             inline=False)
    embed1.add_field(name=f'Mode refreshes <t:{time}:R>.', value='These modes are on a daily rotation, please note that said time is approximate and allows a 10 minute delay.', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(0))
    embed2 = discord.Embed(title='**Event queue**', colour=discord.Colour.blue(),
                           description='React with 🇶 to join the event queue. You will be pinged as soon as there will be enough players. Also, be aware of queue kick time.')
    embed2.set_thumbnail(
        url=images.getImage(2))
    return embed1, embed2

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
                           description=f'You have joined the queue! A game will start as soon as there will be 2 players in the queue. To leave the queue, remove the reaction.\n\nTo confirm your presence, you will be kicked in **10 minutes** and will receive a dm notifying you about this.')
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

def getReadyTimeoutEmbed(p1, p2, time):
    embed1 = discord.Embed(title=f'**Time\'s up!**', colour=discord.Colour.red(),
                           description=f'The game between {p1.mention} and {p2.mention} has failed!\n\nUnfortunately, both players weren\'t ready in time.\n\nThis game will be deleted <t:{time}:R>.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getGiveUpEmbed(user, pNum, time):
    embed1 = discord.Embed(title=f'**P{int(pNum)+1} gave up!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'{user.mention} gave up!\n\nThis game will be deleted <t:{time}:R>, you can save the replay if you need it.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getInteractionTimeoutEmbed(user, time):
    embed1 = discord.Embed(title=f'**Time\'s up!**', colour=discord.Colour.red(),
                           description=f'The game was terminated due to {user.mention} idling!\n\nThis game will be deleted <t:{time}:R>, you can save the replay if you need it.')
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

def getMysteryDieNotYourTurnEmbed():
    embed1 = discord.Embed(title=f'**Opponent only.**', colour=discord.Colour.red(),
                           description=f'Only your opponent can roll the mystery die.\n\nHowever, you can use the *give up* button at any time.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getIdleTimeoutExtendedEmbed():
    embed1 = discord.Embed(title=f'**Reset idle timer.**', colour=discord.Colour.blue(),
                           description=f'The idle timer was reset back to 1 minute.')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getInviteEmbed(p1, p2, time):
    embed1 = discord.Embed(title=f'**Game invitation!**', colour=discord.Colour.green(),
                           description=f'{p1.mention} has invited {p2.mention} to a farkle game!\n\nReady-up as the game is about to begin!\n\nReact with ✅ to get into ready mode. The game will start as soon as both players are ready!\n\nThe invite will expire <t:{time}:R>.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getQueueGameEmbed(p1, p2, time):
    embed1 = discord.Embed(title=f'**Queue complete!**', colour=discord.Colour.green(),
                           description=f'There was enough players waiting in the queue to start a game!\n\n{p1.mention} VS {p2.mention}\n\nReady-up as the game is about to begin!\n\nReact with ✅ to get into ready mode. The game will start as soon as both players are ready!\n\nThe invite will expire <t:{time}:R>.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getStartNormalEmbed(turn, p1, p2, goal, ptLead, mltQty, mltQual):
    embed1 = discord.Embed(title=f'**NORMAL MODE**', colour=discord.Colour.green(),
                           description=f'The game started in normal mode. Roll dice, meld them, get points! First player to get *{goal} pts.* wins!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name='**Win condition:**', value=f'{goal} pts.', inline=True)
    embed1.add_field(name='**Lead from:**', value=f'{ptLead} pts.', inline=True)
    embed1.add_field(name='**Multiplier:**', value=f'+{mltQual}x every {mltQty} turns.', inline=True)
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getStartScoreAttackEmbed(turn, p1, p2):
    embed1 = discord.Embed(title=f'**SCORE ATTACK MODE**', colour=discord.Colour.green(),
                           description=f'The game started in score attack mode. Roll dice, meld them, get points! *500 pts.* removed every turn. First player with negative bank looses!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getStartSnowballEmbed(turn, p1, p2, cap):
    embed1 = discord.Embed(title=f'**SNOWBALL MODE**', colour=discord.Colour.green(),
                           description=f'The game started in snowball mode. Roll dice, meld them, get points, but there\'s only 1 bank! The first player to get the bank to exactly *{cap} pts.* wins.\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getStartHotPotatoEmbed(turn, p1, p2):
    embed1 = discord.Embed(title=f'**HOT POTATO MODE**', colour=discord.Colour.green(),
                           description=f'The game started in hot potato mode. Roll dice, select 1 meld and pass the turn to the next person. You loose *1000 pts.* if you farkle. First player with negative bank looses!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getStartTugOfWarEmbed(turn, p1, p2):
    embed1 = discord.Embed(title=f'**TUG OF WAR MODE**', colour=discord.Colour.green(),
                           description=f'The game started in tug of war mode. Roll dice, meld them, get points, but all the points you earn are stolen!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getStartMysteryDieEmbed(turn, p1, p2):
    embed1 = discord.Embed(title=f'**MYSTERY DIE MODE**', colour=discord.Colour.green(),
                           description=f'The game started in mystery die mode. Roll dice, meld them, get points, but all the start of your turn the opponent has an option to roll the mystery die!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getStartBountyEmbed(turn, p1, p2):
    embed1 = discord.Embed(title=f'**BOUNTY MODE**', colour=discord.Colour.green(),
                           description=f'The game started in bounty mode. Roll dice, meld them, but you only get points for "bounty melds" that are displayed in the turn recap!\n\nP1: {p1.mention}\nP2: {p2.mention}')
    embed1.add_field(name=f'**P{turn + 1} starts!**', value=f'{p2.mention if turn else p1.mention} was picked randomly to do the first turn!', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getMultiplierIncrEmbed(turns, multiplier, incr):
    embed1 = discord.Embed(title=f'**Multiplier increased!**', colour=discord.Colour.blue(),
                           description=f'The game was going on for {turns} turns and the multiplier was increased by **{incr}x**!\n\n**Current multiplier: *{multiplier}x***')
    embed1.set_thumbnail(
        url=images.getImage(1))
    return embed1

def getTurnRecap(destUsr, p1Bank, p2Bank, turnBank, qty, pNum, history):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    embed1.add_field(name='**P1\'s bank:**', value=p1Bank, inline=True)
    embed1.add_field(name='**P2\'s bank:**', value=p2Bank, inline=True)
    embed1.add_field(name='**Turn score:**', value=turnBank, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    turnEmbeds = [discord.Embed(title='**Turn history**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='All your actions during the turn are displayed here!')]
    if history == []:
        turnEmbeds[0].add_field(name='Nothing here yet...', value='', inline=False)
    else:
        while (len(history)-1)//24 + 1 != len(turnEmbeds):
            turnEmbeds += [discord.Embed(title='', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='')]
        for n, i in enumerate(history):
            turnEmbeds[n//24].add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    turnEmbeds[0].set_thumbnail(url=images.getImage(2))
    return [embed1] + turnEmbeds

def getSnowballTurnRecap(destUsr, bank, turnBank, qty, pNum, history):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    embed1.add_field(name='**Bank:**', value=bank, inline=True)
    embed1.add_field(name='**Turn score:**', value=turnBank, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    turnEmbeds = [discord.Embed(title='**Turn history**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='All your actions during the turn are displayed here!')]
    if history == []:
        turnEmbeds[0].add_field(name='Nothing here yet...', value='', inline=False)
    else:
        while (len(history)-1)//24 + 1 != len(turnEmbeds):
            turnEmbeds += [discord.Embed(title='', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='')]
        for n, i in enumerate(history):
            turnEmbeds[n//24].add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    turnEmbeds[0].set_thumbnail(url=images.getImage(2))
    return [embed1] + turnEmbeds

def getHotPotatoRecap(destUsr, bank1, bank2, qty, pNum, history):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    embed1.add_field(name='**P1\'s bank:**', value=bank1, inline=True)
    embed1.add_field(name='**P2\'s bank:**', value=bank2, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    turnEmbeds = [discord.Embed(title='**Turn history**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='All your actions during the turn are displayed here!')]
    if history == []:
        turnEmbeds[0].add_field(name='Nothing here yet...', value='', inline=False)
    else:
        while (len(history)-1)//24 + 1 != len(turnEmbeds):
            turnEmbeds += [discord.Embed(title='', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='')]
        for n, i in enumerate(history):
            turnEmbeds[n//24].add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    turnEmbeds[0].set_thumbnail(url=images.getImage(2))
    return [embed1] + turnEmbeds

def getMysteryDieTurnRecap(destUsr, p1Bank, p2Bank, turnBank, qty, pNum, history, mod, showMod):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    if showMod:
        embed1.add_field(name='**Turn\'s modifier:**', value=mod, inline=False)
    embed1.add_field(name='**P1\'s bank:**', value=p1Bank, inline=True)
    embed1.add_field(name='**P2\'s bank:**', value=p2Bank, inline=True)
    embed1.add_field(name='**Turn score:**', value=turnBank, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    turnEmbeds = [discord.Embed(title='**Turn history**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='All your actions during the turn are displayed here!')]
    if history == []:
        turnEmbeds[0].add_field(name='Nothing here yet...', value='', inline=False)
    else:
        while (len(history)-1)//24 + 1 != len(turnEmbeds):
            turnEmbeds += [discord.Embed(title='', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='')]
        for n, i in enumerate(history):
            turnEmbeds[n//24].add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    turnEmbeds[0].set_thumbnail(url=images.getImage(2))
    return [embed1] + turnEmbeds

def getBountyTurnRecap(destUsr, p1Bank, p2Bank, qty, pNum, history, bounties):
    embed1 = discord.Embed(title=f'**{qty}. P{pNum + 1}\'s turn!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'It\'s {destUsr.mention}\'s turn! Check the message below to see what you can do!')
    embed1.add_field(name='***3000 pts.*:**', value=f'{bounties[0][3]} × {bounties[0][1]}', inline=True)
    embed1.add_field(name='***1500 pts.*:**', value=f'{bounties[1][3]} × {bounties[1][1]}', inline=True)
    embed1.add_field(name='***500 pts.*:**', value=f'{bounties[2][3]} × {bounties[2][1]}', inline=True)
    embed1.add_field(name='**P1\'s bank:**', value=p1Bank, inline=True)
    embed1.add_field(name='**P2\'s bank:**', value=p2Bank, inline=True)
    embed1.set_thumbnail(
        url=images.getImage(not pNum))
    turnEmbeds = [discord.Embed(title='**Turn history**', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='All your actions during the turn are displayed here!')]
    if history == []:
        turnEmbeds[0].add_field(name='Nothing here yet...', value='', inline=False)
    else:
        while (len(history)-1)//24 + 1 != len(turnEmbeds):
            turnEmbeds += [discord.Embed(title='', colour=discord.Colour.blue() if pNum else discord.Colour.red(), description='')]
        for n, i in enumerate(history):
            turnEmbeds[n//24].add_field(name=f'{n+1}. {i[0]}', value=i[1], inline=True)
    turnEmbeds[0].set_thumbnail(url=images.getImage(2))
    return [embed1] + turnEmbeds

def getNormalStartTurnEmbed(mlt, lead, stake, pNum, time):
    embed1 = discord.Embed(title=f'**It\'s dice rolling time!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Your turn just started! You can roll the dice or... roll the dice!')
    if stake != None:
        embed1.add_field(
            name=f'You can do a high stake for *{stake[0]} pts.*',
            value='',
            inline=False)
    if mlt != 1:
        if lead:
            embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your point lead.', value='',
                             inline=False)
        else:
            embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                             inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getScoreAttackStartTurnEmbed(stake, pNum, first, time):
    if first:
        embed1 = discord.Embed(title=f'**It\'s dice rolling time!**',
                               colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                               description=f'Your turn just started!You can roll the dice or... roll the dice!\n\nOnly ***250 pts.*** were removed from your bank because it\'s the first turn of the game.\n')
    else:
        embed1 = discord.Embed(title=f'**It\'s dice rolling time!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Your turn just started!You can roll the dice or... roll the dice!\n\n***500 pts.*** were removed from your bank.\n')
    if stake != None:
        embed1.add_field(
            name=f'You can do a high stake for *{stake[0]} pts.*',
            value='',
            inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHotPotatoStartTurnEmbed(pNum, time, iconList):
    embed1 = discord.Embed(title=f'**It\'s dice rolling time!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Your turn just started! You can roll the dice or pass the turn to the next person for 250 pts.!')
    embed1.add_field(
        name=f'**Remaining dice:**',
        value=' '.join(iconList),
        inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHighStakesEmbed(mlt, iconList, iconList2, lead, pts, pNum, time):
    embed1 = discord.Embed(title=f'**High stakes!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'You chose to continue the turn of your opponent! You got *{pts} pts.* and can now roll the dice. However, if you farkle this turn, you\'ll loose *{pts} pts.* so watch out!')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if mlt != 1:
        if lead:
            embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score gain because of your point lead (still applied on point loss).', value='',
                             inline=False)
        else:
            embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                             inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getMysteryDieChoiceEmbed(pNum, time, user):
    embed1 = discord.Embed(title=f'**P{int(not pNum)+1} can roll the mystery die!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'{user.mention}, would you like to roll the ***mystery die***? Rolling the die will apply a random modifier on the turn! I can either positive or negative, it\'s up to you whether to take the risk!')
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getMysteryDieRolledEmbed(mod):
    embed1 = discord.Embed(title=f'**You rolled the die!**', colour=discord.Colour.green(),
                           description=f'You decided to roll the mystery die! Here\'s the result:\n\n{mod}\n\nYour decision and the result isn\'t shown to your opponent until the end of the turn.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getMysteryDieSkippedEmbed():
    embed1 = discord.Embed(title=f'**You skipped the roll!**', colour=discord.Colour.green(),
                           description=f'You decided to not roll the mystery die!\n\nYour decision isn\'t shown to your opponent until the end of the turn.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHotDiceEmbed(pts, iconList, mlt, lead, pNum, time):
    embed1 = discord.Embed(title=f'**Hot dice!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'{" ".join(iconList)} *- {pts} pts.*\nAll the dice were automatically melded! You can now re-roll all 6 dice again.')
    if mlt != 1:
        if lead:
            embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your point lead.', value='',
                             inline=False)
        else:
            embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                             inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='', inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getFarkledEmbed(turnBank, iconList, pNum):
    embed1 = discord.Embed(title=f'**You farkled!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'{" ".join(iconList)}\nMelds can\'t be formed from the remaining dice! The score you earned this turn will be lost.\n\nPoints lost *- {turnBank} pts.*')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getTurnPassEmbed(pts, pNum):
    embed1 = discord.Embed(title=f'**Turn passed!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You chose not to do a risky play and passed the turn to P{int(not pNum)}, however you lost *{pts} pts.*')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getFailedHighStakeEmbed(iconList, pts, pNum):
    embed1 = discord.Embed(title=f'**High stake failed!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You farkled... and lost the high stake.\n\n{" ".join(iconList)}\nMelds can\'t be formed from the remaining dice! The score you earned this turn will be lost.\n\n*{pts} pts.* were removed from your bank!')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getScoreBankedEmbed(turnBank, pNum):
    embed1 = discord.Embed(title=f'**Score banked!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You finished your turn and banked the score you earned during it.\n\nPoints banked - *{turnBank}*')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getMysteryDierScoreBankedEmbed(turnBank, pNum,mod):
    embed1 = discord.Embed(title=f'**Score banked!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You finished your turn and banked the score you earned during it.\n\nPoints banked - *{turnBank}*\nTurn modifier - {mod}')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getScoreCapExceededEmbed(pts, pNum, cap):
    embed1 = discord.Embed(title=f'**Score cap exceeded!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'Your score went over the limits by *{pts} pts.* It was reset to {cap}.')
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getAfterRollEmbed(iconList, iconList2, mlt, lead, pNum, time):
    embed1 = discord.Embed(title=f'**You rolled the dice!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You rolled the dice, see which melds you can make form them by looking at the interactions. The best meld available is highlighted in purple.')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if mlt != 1:
        if lead:
            embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your point lead.', value='',
                             inline=False)
        else:
            embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                             inline=False)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='',
                     inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getHotPotatoAfterRollEmbed(iconList, iconList2, pNum, time):
    embed1 = discord.Embed(title=f'**You rolled the dice!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You rolled the dice, you can only pick 1 meld per turn, so pick carefully.')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='',
                     inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1

def getAfterMeldEmbed(iconList, iconList2, meld, mlt, lead, pNum, time):
    embed1 = discord.Embed(title=f'**Meld successful!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You melded **{meld[3]} × {meld[1]}** and got *{meld[2]} pts.* You can now select another meld, roll the dice or bank your score!')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if mlt != 1:
        if lead:
            embed1.add_field(name=f'Current multiplier: {mlt}x, however it does not apply to your current score because of your point lead.', value='',
                             inline=False)
        else:
            embed1.add_field(name=f'Current multiplier: {mlt}x.', value='',
                             inline=False)
    if time != None:
        embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='',
                         inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1


def getAfterBountyMeldEmbed(iconList, iconList2, meld, pNum, time):
    embed1 = discord.Embed(title=f'**Bounty melded!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),description=f'You melded **{meld[3]} × {meld[1]}** which was a bounty and therefore got *{meld[2]} pts.* You can now select another meld, roll the dice or bank your score!')
    embed1.add_field(name=f'Remaining dice:', value=' '.join(iconList), inline=True)
    embed1.add_field(name=f'Inventory:', value=' '.join(iconList2), inline=True)
    if time != None:
        embed1.add_field(name=f'The game will be terminated if you won\'t react <t:{time}:R>!', value='',
                         inline=False)
    embed1.set_thumbnail(
        url=images.getImage(2))
    return embed1


def getNormalWinEmbed(winner, turns, pNum, time):
    embed1 = discord.Embed(title=f'**P{pNum+1} WON THE GAME!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'Congratulations, {winner.mention}, you won this game in {turns} turns!\n\nThis game will be deleted <t:{time}:R>, you can save the replay if you need it.')
    embed1.set_thumbnail(
        url=images.getImage(0))
    return embed1

def getNegBankWinEmbed(winner, looser, turns, pNum, time):
    embed1 = discord.Embed(title=f'**P{pNum+1} WON THE GAME!**', colour=discord.Colour.blue() if pNum else discord.Colour.red(),
                           description=f'{looser.mention} finished the turn with a negative bank therefore {winner.mention} won in {turns} turns !\n\nThis game will be deleted <t:{time}:R>, you can save the replay if you need it.')
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

def getReplaySavedEmbed():
    embed1 = discord.Embed(title=f'**Replay saved!**', colour=discord.Colour.yellow(),
                           description=f'Your replay was saved!\n\nYou can check the replays category to see your replays.')
    embed1.set_thumbnail(url=images.getImage(2))
    return embed1

def getReplaySharedEmbed(user):
    embed1 = discord.Embed(title=f'**User added!**', colour=discord.Colour.yellow(),
                           description=f'{user.mention} is now able to see this replay!\n\nDid you know that you can hide this replay from someone by putting *False* in the *status* field?')
    embed1.set_thumbnail(url=images.getImage(2))
    return embed1

def getReplayUnsharedEmbed(user):
    embed1 = discord.Embed(title=f'**User removed!**', colour=discord.Colour.yellow(),
                           description=f'{user.mention} will no longer be able to see this replay!')
    embed1.set_thumbnail(url=images.getImage(2))
    return embed1

def getReplayInfoEmbed(host, id, shared):
    embed1 = discord.Embed(title=f'**Replay info & actions.**', colour=discord.Colour.yellow(),
                           description=f'Replay {id} is saved by {host.mention}.\n\nShared to:\n' + ', '.join([str(i.mention) for i in shared]) + '\n\nIf you\'re the host, you can delete this replay or show it to someone by using the */share* command.')
    embed1.set_thumbnail(url=images.getImage(2))
    return embed1

def getGiveUpConfirmEmbed():
    embed1 = discord.Embed(title=f'**Are you sure?**', colour=discord.Colour.red(),
                           description=f'You are about to give up and quit the game, please confirm that this action is intentional.')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getReplayDeleteConfirmEmbed():
    embed1 = discord.Embed(title=f'**Are you sure?**', colour=discord.Colour.red(),
                           description=f'You are about to delete the replay, please confirm that this action is intentional.')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getNoReplayRightsEmbed():
    embed1 = discord.Embed(title=f'**You can\'t manage this replay!**', colour=discord.Colour.red(),
                           description=f'Only the host of this replay can manage it.')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getNotInReplayChannelEmbed():
    embed1 = discord.Embed(title=f'**This is a replay command!**', colour=discord.Colour.red(),
                           description=f'You can only execute this command in a replay channel.')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

def getHurryUpEmbed(user, time):
    embed1 = discord.Embed(title=f'**Hurry up!**', colour=discord.Colour.red(),
                           description=f'It\'s {user.mention}\'s turn!\n\nThe game will terminate <t:{time}:R>. If you need more time to think, press the "Reset idle timer" button (active for both players).')
    embed1.set_thumbnail(url=images.getImage(1))
    return embed1

