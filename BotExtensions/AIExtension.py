#  Copyright (c) 2024.
#  Ceci est une propriété de CoRExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.
import discord
from discord.ext import commands
import requests
import json
import subprocess as sub


def setup(bot):
    bot.add_cog(AIExtension(bot))


def teardown(bot):
    bot.remove_cog("AIExtension")


def launch_ai():
    return sub.Popen("ollama serve")

def kill_ai(ai: sub.Popen):
    ai.terminate()

class AIExtension(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        try :
            self.serv_online = requests.get("http://localhost:11434").status_code == 200
        except requests.exceptions.ConnectionError:
            self.serv_online = False
        if self.serv_online:
            self.models = []

    @commands.slash_command()
    @commands.has_role("AI Key")
    async def ask(self, ctx, model, question):
        # await self.bot.change_presence(activity=discord.Activity(name="AI Thinking"))
        await ctx.defer()
        response = requests.post(f"http://localhost:11434/api/generate",
                                 data=json.dumps({"model": model, "prompt": question, "stream": False}))
        await ctx.respond(json.loads(response.text)["response"])

    @ask.error
    async def ask_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.respond("Tu n'as pas la permission d'utiliser cette commande", ephemeral=True)


    @commands.slash_command()
    @commands.has_any_role("Admin", "Modo")
    async def ai_setup(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(title="Paramétrage du serveur", description='Ceci est une commande de paramétrage du serveur', colour=discord.Colour.dark_blue())
        view = discord.ui.View(timeout=120, disable_on_timeout=True)

        embed.add_field(name="Description", value="Cette commande permet de paramétrer le serveur discord et d'y rajouter la catégorie 'AI'", inline=False)
        embed.set_footer(text="Péremption de la commande : 2:00")

        view.add_item(discord.ui.Button(label="Créer la catégorie", style=discord.ButtonStyle.blurple, custom_id="create_category"))
        async def check(interaction: discord.Interaction):
            if interaction.custom_id == "create_category":
                await interaction.response.send_message("Création de la catégorie...")
                # TODO : Create category

        view.interaction_check = check

        await ctx.respond(embed=embed, view=view)



    @commands.slash_command()
    @commands.has_any_role("Admin", "Modo")
    async def ai_status(self, ctx):
        embed = discord.Embed(title="AI", description='Toutes les information concernant l\'AI ')
        view = discord.ui.View()

        if self.serv_online:
            embed.add_field(name="Status", value="Online", inline=False)
            embed.colour = discord.Colour.green()
            view.add_item(discord.ui.Button(label="Turn OFF AI", style=discord.ButtonStyle.red, custom_id="kill_ai"))
        else:
            embed.add_field(name="Status", value="Offline", inline=False)
            embed.colour = discord.Colour.red()
            view.add_item(discord.ui.Button(label="Turn ON AI", style=discord.ButtonStyle.green, custom_id="launch_ai"))
        await ctx.respond(embed=embed)
