#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands
from BotExtensions.PokeInteract import *


def setup(bot):
    bot.add_cog(PokeExtension(bot))


class PokeExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interact = PokeInteract()

    @commands.slash_command()
    async def poke(self, ctx, name):
        embed = discord.Embed(title=name, color=0x00ff00)
        poke = self.interact.get_poke(name)
        embed.set_thumbnail(url=poke['sprites']['front_default'])
        for poke_type in poke['types']:
            embed.add_field(name=poke_type['type']['name'], value=poke_type['type']['name'], inline=True)
        await ctx.respond(embed=embed)
