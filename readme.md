#
<div align="center">
    <a href="https://www.python.org/">
        <img 
            src="https://img.shields.io/badge/WRITTEN%20IN-PYTHON%203.11-4B8BBE?style=for-the-badge&logo=python&logoColor=white"
            height="30"
        />
    </a> 
    <a href="https://discord.gg/Q3JWsayfSp">
        <img 
            src="https://img.shields.io/discord/1073319056083517551?color=5865F2&label=DISCORD&logo=discord&logoColor=white&style=for-the-badge"
            height="30"
        />
    </a>
    <a href="https://github.com/posterhusky/FarkleBot">
        <img 
            src="https://img.shields.io/badge/REPO%20LINK-%2FFarkleBot-6cc644?style=for-the-badge&logo=github&logoColor=white"
            height="30"
        />
    </a>
</div>

# Farkle bot

Welcome to the Farkle Discord Bot! This bot is designed to replicate the popular board game Farkle, where players roll dice to score points and try to reach a winning score before their opponents. The bot is supposed to be used in the [official discord server](https://discord.gg/Q3JWsayfSp).


## How to play farkle
- The game is played with six dice, and the object of the game is to score points by rolling certain combinations of numbers on the dice.

- Each turn, the player rolls all six dice and sets aside any dice that score points. The player can then choose to roll the remaining dice or stop and keep their current score.

- If the player sets aside all six dice, they can roll all six dice again for bonus points.

- If the player rolls a combination of dice that does not score any points, this is called a Farkle and the player loses all points accumulated in that turn.

- The game ends when one player reaches a predetermined winning score, typically 10 000 points.

More detailed rules can be seen in the [official discord server](https://discord.gg/Q3JWsayfSp).

## How to self-host the bot
We should warn you that this version of the bot isn't meant to be used on other servers. To operate the bot your server must have specific channels and messages. We are currently working on a "light" version that can be used by everyone.

- First you should make sure you have the following dependencies: `discord.py`, `pycord`, `asyncio`, `random`, `time`

- Then, you should create the required roles and channels

- After this you have to update the ID of the admin role and get the required messages and their IDs via the $ commands

- Finally, you have to replace all the IDs in the "idList.py". You can also replace the images in "images.py".

## Authors

- [@Vanolex](https://github.com/posterhusky)

- [@Hexabyte](https://github.com/brianag010)


We hope you enjoy playing Farkle with our Discord Bot! If you have any questions or feedback, please don't hesitate to reach out to us.
