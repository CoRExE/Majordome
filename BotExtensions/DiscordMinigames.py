import discord
import random
from discord.ext import commands
from discord.ui import View, Button


def setup(bot):
    bot.add_cog(DiscordMinigame(bot))


class DiscordMinigame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def pfc(self, ctx):
        view = PFCView(60)
        view.ctx = ctx
        await ctx.respond("Choisissez votre option :", view=view)

    @commands.command()
    async def randomize(self, ctx, *, msg):
        msg = msg.split('-')
        await ctx.send(random.choice(msg))

    @commands.command()
    async def roll(self, ctx, *, msg):
        msg = int(msg)
        if random.randint(0, 99) == 0:
            await ctx.reply('https://youtu.be/dQw4w9WgXcQ')
        else:
            await ctx.reply(random.randint(0, msg), mention_author=False)

    @commands.command()
    async def pile_face(self, ctx):
        await ctx.reply(random.choice(['Pile', 'Face']), mention_author=False)


# # # Class View # # #


class PFCView(View):
    def __init__(self, timeout: int | None = None):
        super().__init__(timeout=timeout)

        self.add_item(Button(style=discord.ButtonStyle.primary, label="Pierre", custom_id="pierre"))
        self.add_item(Button(style=discord.ButtonStyle.primary, label="Feuille", custom_id="feuille"))
        self.add_item(Button(style=discord.ButtonStyle.primary, label="Ciseaux", custom_id="ciseaux"))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        await self.button_callback(interaction)
        return True

    async def on_timeout(self):
        await self.message.edit(content="Le temps imparti pour choisir a expiré.", view=None)

    async def button_callback(self, interaction: discord.Interaction):
        option = interaction.custom_id

        if option == "pierre":
            await interaction.response.send_message("Vous avez choisi Pierre.")
        elif option == "feuille":
            await interaction.response.send_message("Vous avez choisi Feuille.")
        elif option == "ciseaux":
            await interaction.response.send_message("Vous avez choisi Ciseaux.")

        await self.message.edit(view=None)
