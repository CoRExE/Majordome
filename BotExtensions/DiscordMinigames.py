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

    @commands.slash_command()
    async def memory(self, ctx):
        view = Memory()
        await ctx.respond("Sélectionnez 2 Buttons :", view=view)


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


class Memory(View):
    # TODO Correction of revel emoji button
    def __init__(self, timeout: int | None = None):
        super().__init__(timeout=timeout)
        self.emojis = ['🌼', '🌺', '🌸', '🌻', '🌹', '🌷']
        self.buttons = []
        self.couple = []

        compteur = 0
        emoji_copy = self.emojis.copy()
        for x in range(len(self.emojis)):
            emoji = random.choice(emoji_copy)
            for y in range(2):
                compteur += 1
                but = Button(style=discord.ButtonStyle.primary, label="?", custom_id=emoji+str(compteur))
                self.buttons.append(but)
                self.add_item(but)
            emoji_copy.remove(emoji)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        await self.button_react(interaction)
        return True

    async def on_timeout(self) -> None:
        await self.message.edit(view=None)

    async def button_react(self, interaction: discord.Interaction):
        emoji = interaction.custom_id
        button = self.get_button_by_id(emoji)
        if len(self.couple) == 1:
            self.couple.append(emoji)
            if self.couple[0] == self.couple[1]:
                await interaction.response.send_message(f"Vous avez trouvé une paire avec l'emoji : {emoji}")
            else:
                await interaction.response.send_message(f"Mauvaise paire !")
                await self.hide_buttons([self.couple[0], self.couple[1]])
            self.couple = []
        else:
            self.couple = [emoji]
        await interaction.message.edit()

    async def hide_buttons(self, emojis):
        for emoji in emojis:
            button = self.get_button_by_id(emoji)
            await self.update_button_label(button, "?")

    async def update_button_label(self, button, emoji):
        button.label = emoji
        button.disabled = True

    def get_button_by_id(self, emoji):
        for button in self.buttons:
            if button.custom_id == emoji:
                return button
