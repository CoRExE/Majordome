import discord
from discord.ext import commands
# from discord.ui import Button, Select, View


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # All players who joined the game
        self.players = {}
        # All player(s) ban
        self.banPlayer = []
        # Every Item on the game
        self.allItems = []
        # Every Ban Item
        self.banItem = []

    @commands.command()
    async def stats(self, ctx):
        stat = ''
        stat += f'{ctx.author.name}, votre puissance disponible est de : {self.power}, ' \
                f'vos données sont de : {self.data}/100 <:Data:943886193676939345> ' \
                f'et votre Trésorerie est de {self.money} <:TimCoins:944398852910358628>'
        await ctx.send(stat)


class Player:
    def __int__(self, member: discord.Member):
        self.member = member


class Item:
    def __init__(self, name: str, use: bool, desc: str, chance, value):
        self.nameItem = name
        self.utility = use
        self.effect = desc
        self.rate = chance
        self.value = value
