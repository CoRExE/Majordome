import discord
from discord.ext import commands
from Manage_DataBase import *
# from discord.ui import Button, Select, View


data_management = ManageDB("Data")

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
