#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.


import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Troll(bot))


class Troll(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot

    @commands.command()
    async def yes(self, ctx):
        await ctx.send('https://tenor.com/view/jojo-anime-yes-yes-yes-yeah-its-a-yes-gif-17161748')
        await ctx.message.delete()

    @commands.command()
    async def noice(self, ctx):
        await ctx.send('https://tenor.com/view/noice-nice-click-gif-8843762')
        await ctx.message.delete()

    @commands.command()
    async def rick(self, ctx):
        await ctx.send('https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173')
        await ctx.message.delete()

    @commands.command()
    async def Ooh(self, ctx):
        await ctx.send(
            'https://tenor.com/view/%D1%81%D1%80%D1%81%D0%BC-%D0%B1%D0%B5%D0%BB%D0%B0-%D0%B8%D0%BD%D0%B5%D0%BD'
            '%D0%B0%D0%B4%D0%B0-%D0%B8%D0%B7%D0%BD%D0%B5%D0%BD%D0%B0%D0%B4%D0%B0-%D1%81%D0%BC%D1%8F%D1%85-gif'
            '-24523449')
        await ctx.message.delete()

    @commands.command()
    async def yeet(self, ctx):
        await ctx.send("https://tenor.com/view/whats-a-yeet-playing-gif-15038419")
        await ctx.message.delete()

    @commands.command()
    async def groult(self, ctx):
        await ctx.send(
            'https://cdn.vox-cdn.com/thumbor/yzPdGsXFWCHbNMlDWHhPROUzVeI=/1400x1400/filters:format('
            'jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/8378039/baby-groot-guardians.0.jpg')
        await ctx.message.delete()
