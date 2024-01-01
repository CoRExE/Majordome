import discord
from discord.ext import commands
from BotExtensions.Manage_DataBase import *
from asyncio import sleep
# from discord.ui import Button, Select, View


data_management  = ManageDB("BotExtensions/EconomyData")


def setup(bot):
    bot.add_cog(Game(bot))
    print("Economy cog loaded")


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
    def init_db(self):
        pass


    @commands.slash_command()
    async def create_profile(self, ctx: discord.ApplicationContext):
        pass


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
