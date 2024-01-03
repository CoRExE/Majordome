import discord
from discord.ext import commands
from BotExtensions.Manage_DataBase import *
from asyncio import sleep
# from discord.ui import Button, Select, View


data_management  = ManageDB("BotExtensions/EconomyData")


def setup(bot):
    bot.add_cog(Game(bot))
    try :
        data_management.create_schema("Economy")
        print("Economy Schema init")
        data_management.connexion("Economy")
        data_management.create_table("Player")
    except AssertionError:
        data_management.connexion("Economy")
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
    async def create_profile(self, ctx):
        await ctx.respond(Player.get_player(ctx.author))

class Player:
    def __int__(self, member: discord.member.Member):
        self.member = member

    @staticmethod
    def get_player(member: discord.Member):
        if data_management.connexion("Player"):
            pass


class Item:
    def __init__(self, name: str, use: bool, desc: str, chance, value):
        self.nameItem = name
        self.utility = use
        self.effect = desc
        self.rate = chance
        self.value = value
