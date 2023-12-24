#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands
from discord.ext.pages import Paginator

from BotExtensions.PokeInteract import *


def setup(bot):
    bot.add_cog(PokeExtension(bot))


class PokeExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.interact = PokeInteract()

    @commands.slash_command()
    async def poke(self, ctx, name):
        poke = self.interact.get_poke(name)
        embed = discord.Embed(title=self.interact.get_species(name)['names'][4]['name'], color=0x00ff00)
        embed.set_thumbnail(url=poke['sprites']['front_default'])
        for poke_type in PokeInteract.get_poke_types(poke):
            embed.add_field(name=poke_type, value=poke_type, inline=True)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def pokemon(self, ctx):
        # TODO Add paginator
        basic_info_page = "Informations basiques du Pokemon"
        stats_page = "Statistiques du Pokemon"
        talent_page = "Talent du Pokemon"
        abilities_page = "Capacités du Pokemon"

        pages = [basic_info_page, stats_page, talent_page, abilities_page]
        paginator = Paginator(pages)

        @discord.ui.button(label="Page suivante", style=discord.ButtonStyle.green)
        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Page suivante", ephemeral=True)
            await paginator.goto_page((paginator.current_page + 1)//len(pages))

        await ctx.respond(paginator.pages[0])
