#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.
from discord.ext import commands
import os


def setup(bot):
    bot.add_cog(Phasmophobia(bot))


class Phasmophobia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
