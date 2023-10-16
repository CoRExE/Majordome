#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from PokeInteract import *


def setup(bot):
    bot.add_cog(PokeInteract(bot))


class PokeInteract:
    def __init__(self, bot):
        self.bot = bot
        self.interact = PokeInteract()

