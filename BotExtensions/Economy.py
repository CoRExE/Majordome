import discord
from discord.ext import commands
from BotExtensions.Manage_DataBase import *
from asyncio import sleep

# from discord.ui import Button, Select, View


data_management = ManageDB("BotExtensions/EconomyData")


def setup(bot):
    bot.add_cog(Game(bot))
    try:
        create_database(data_management)
    except AssertionError:
        data_management.connexion("Economy")
    print("Economy cog loaded")


def teardown(bot):
    print("Economy cog unloaded")
    data_management.safe_close()


def create_database(data):
    data.create_schema("Economy")
    data.create_table(
        ["Players", [("id", "INTEGER PRIMARY KEY AUTOINCREMENT"), ("name", "TEXT"), ("money", "INTEGER")]])


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
