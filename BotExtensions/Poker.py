#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Poker(bot))


def get_ID_role_by_name(ctx: commands.Context, role_name):
    guild = ctx.guild

    role = discord.utils.get(guild.roles, name=role_name)
    if role:
        return role.id
    else:
        return False


class Poker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = []
        self.players = []
        self.table = {}

    def get_manager_roles(self):
        return self.roles

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def set_authorized_role(self, ctx, *role: discord.Role):
        for r in role:
            self.roles.append(r)

    @commands.slash_command()
    @commands.has_any_role(*get_manager_roles())
    async def set_env_table(self, ctx):
        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(get_ID_role_by_name(ctx, "player")): discord.PermissionOverwrite(read_messages=True)
        }

        await ctx.respond("Generation de l'environnement...")
        await guild.create_text_channel(name="tables", overwrites=overwrites)

    # TODO : Ajouter les commandes de unregister

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def register_button(self, ctx):
        @discord.ui.button(label="Register", style=discord.ButtonStyle.green)
        async def register_button_callback(interaction: discord.Interaction):
            interaction.response.send_message("Register", ephemeral=True)
            self.players.append(interaction.user)

    