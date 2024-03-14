#  Copyright (c) 2024.
#  Ceci est une propriété de CoRExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

from discord.ext import commands
import requests
import json
import subprocess as sub


def setup(bot):
    bot.add_cog(AIExtension(bot))


def teardown(bot):
    bot.remove_cog("AIExtension")


def launch_ai():
    sub.Popen(["ollama serve"])


class AIExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.serv_online = True if requests.get("http://localhost:11434").status_code == 200 else False
        self.models = []

    @commands.slash_command()
    @commands.has_any_role("Admin")
    async def ask(self, ctx, model, question):
        await ctx.defer()
        response = requests.post(f"http://localhost:11434/api/generate", data=json.dumps({"model": model,"prompt": question}))
        json_reply = [json.loads(line)["response"] for line in response.iter_lines()]
        await ctx.respond("".join(json_reply))
