#  Copyright (c) 2024.
#  Ceci est une propriété de CoRExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands
import requests
import json


def setup(bot):
    bot.add_cog(AIExtension(bot))


class AIExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_any_role("Admin")
    async def ask(self, ctx, model, question):
        await ctx.defer()
        response = requests.post(f"http://localhost:11434/api/generate", data=json.dumps({"model": model,"prompt": question}))
        json_reply = [json.loads(line)["response"] for line in response.iter_lines()]
        await ctx.respond("".join(json_reply))
