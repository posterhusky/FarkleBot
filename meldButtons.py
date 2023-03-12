import random

import discord, emojis, embeds, time, asyncio
from discord.ui import View, Button

import gameFunctions


class MeldButton(Button):
    def __init__(self, game, meld, priority: bool):
        super().__init__(label=f'× {meld[1]} - {meld[2]}pts.', emoji=meld[3],
                         style=discord.ButtonStyle.blurple if priority else discord.ButtonStyle.grey)
        self.game = game
        self.meld = meld

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.game.players[self.game.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.game.task.cancel()
        await interaction.response.defer()
        self.game.bank[2] += self.meld[2]
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
        self.game.latestEmbed = embeds.getAfterMeldEmbed(iconList=[emojis.dice[i] for i in self.game.tableDice],
                                                         iconList2=[emojis.dice[i] for i in self.game.invDice], meld=self.meld,
                                                         mlt=self.game.multiplier,
                                                         lead=self.game.turn == self.game.lead, pNum=self.game.turn, time=int(time.time())+60)
        self.game.turnHistory += [('Melded dice:', f'{self.meld[3]} × {self.meld[1]} *- {self.meld[2]}*')]
        await self.game.latestMsg.edit(embeds=self.game.getTurnRecap() + [self.game.latestEmbed], view=btns)
        self.game.task = asyncio.create_task(self.game.cancelIdleUser())

class HotPotatoMeldButton(MeldButton):
    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.game.players[self.game.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.game.task.cancel()
        await interaction.response.defer()
        self.game.bank[self.game.turn] += self.meld[2]
        for _ in range(self.meld[1]):
            self.game.tableDice.remove(self.meld[0])
            self.game.invDice += [self.meld[0]]
        self.game.latestEmbed = embeds.getAfterMeldEmbed(iconList=[emojis.dice[i] for i in self.game.tableDice],
                                                         iconList2=[emojis.dice[i] for i in self.game.invDice], meld=self.meld,
                                                         mlt=self.game.multiplier,
                                                         lead=self.game.turn == self.game.lead, pNum=self.game.turn, time=None)
        self.game.turnHistory += [('Melded dice:', f'{self.meld[3]} × {self.meld[1]} *- {self.meld[2]}*')]
        await self.game.latestMsg.edit(embeds=self.game.getTurnRecap() + [self.game.latestEmbed], view=None)
        self.game.embedList += self.game.getTurnRecap()
        await asyncio.sleep(2)
        if self.game.bank[self.game.turn] > 5000:
            self.game.turnHistory += [('Score cap exceeded:', '*' + str(self.game.bank[self.game.turn] - 5000) + ' pts.* over the limit')]
            self.game.latestEmbed = embeds.getScoreCapExceededEmbed(self.game.bank[self.game.turn] - 5000, pNum=self.game.turn, cap=5000)
            self.game.bank[self.game.turn] = 5000
            await self.game.latestMsg.edit(embeds=self.game.getTurnRecap() + [self.game.latestEmbed], view=None)
            await asyncio.sleep(2)
        await self.game.latestMsg.edit(embeds=self.game.getTurnRecap(), view=None)
        self.game.turn = int(not self.game.turn)
        await self.game.startTurn()


class BountyMeldButton(Button):
    def __init__(self, game, meld, priority: bool):
        super().__init__(label=f'× {meld[1]} - {meld[2]}pts.', emoji=meld[3],
                         style=discord.ButtonStyle.blurple if priority else discord.ButtonStyle.grey)
        self.game = game
        self.meld = meld

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.game.players[self.game.turn]:
            await interaction.response.send_message(embed=embeds.getNotYourTurnEmbed(), ephemeral=True)
            return
        self.game.task.cancel()
        await interaction.response.defer()
        self.game.bank[self.game.turn] += self.meld[2]
        match self.meld[2]:
            case 3000:
                print('3K')
                rn = random.randint(0, 5)
                self.game.bounties[0] = (rn, 4, 3000, gameFunctions.dice[rn])
            case 1500:
                print('1,5K')
                rn = random.randint(0, 5)
                self.game.bounties[1] = (rn, 3, 1500, gameFunctions.dice[rn])
            case 500:
                print('0,5K')
                rn = random.randint(0, 5)
                self.game.bounties[2] = (rn, 2, 500, gameFunctions.dice[rn])
        for _ in range(self.meld[1]):
            self.game.tableDice.remove(self.meld[0])
            self.game.invDice += [self.meld[0]]
        btn1 = Button(label='Roll dice', emoji='🎲', style=discord.ButtonStyle.green, disabled=False)
        btn3 = Button(label='Give up', emoji='🏳', style=discord.ButtonStyle.red, disabled=False)
        btn4 = Button(label='Reset idle timer', emoji='🕓', style=discord.ButtonStyle.blurple, disabled=False)
        btn4.callback = self.game.extendIdleTimeout
        btn1.callback = self.game.rollDice
        btn3.callback = self.game.giveUp
        btns = View()
        self.game.getMelds()
        for i in self.game.melds:
            temp = BountyMeldButton(game=self.game, meld=i, priority=i[2] > 0)
            btns.add_item(temp)
        btns.add_item(btn1)
        btns.add_item(btn3)
        btns.add_item(btn4)
        self.game.latestEmbed = embeds.getAfterMeldEmbed(iconList=[emojis.dice[i] for i in self.game.tableDice],
                                                         iconList2=[emojis.dice[i] for i in self.game.invDice], meld=self.meld,
                                                         mlt=self.game.multiplier, lead=self.game.turn == self.game.lead, pNum=self.game.turn,
                                                         time=int(time.time())+60) if self.meld[2] == 0 else embeds.getAfterBountyMeldEmbed(iconList=[emojis.dice[i] for i in self.game.tableDice],
                                                         iconList2=[emojis.dice[i] for i in self.game.invDice], meld=self.meld, pNum=self.game.turn, time=int(time.time())+60)
        self.game.turnHistory += [('Melded dice:', f'{self.meld[3]} × {self.meld[1]} *- {self.meld[2]}*')]
        await self.game.latestMsg.edit(embeds=self.game.getTurnRecap() + [self.game.latestEmbed], view=btns)
        self.game.task = asyncio.create_task(self.game.cancelIdleUser())