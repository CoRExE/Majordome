import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hey(self, ctx):
        await ctx.send("Hi !")
