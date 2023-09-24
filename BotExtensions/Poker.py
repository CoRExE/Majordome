#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands
from random import choice as ch


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
        self.table = {"Table 1": []}

    def check_roles(self, ctx):
        check = False
        for role in ctx.author.roles:
            if role in self.roles:
                check = True
        if not check:
            raise Exception("Vous n'avez pas les droits")

    @commands.slash_command()
    async def set_authorized_role(self, ctx):
        ...  # TODO Add Select to Choice Role

    @commands.slash_command()
    async def set_env_table(self, ctx):
        self.check_roles(ctx)

        guild = ctx.guild

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.get_role(get_ID_role_by_name(ctx, "player")): discord.PermissionOverwrite(read_messages=True)
        }

        await ctx.respond("Generation de l'environnement...")
        await guild.create_text_channel(name="tables", overwrites=overwrites)

    @set_env_table.error
    async def set_env_table_error(self, ctx, error):
        if error is Exception:
            await ctx.respond("Vous n'avez pas les droits", ephemeral=True)

    # TODO : Ajouter les commandes de unregister

    @commands.slash_command()
    async def register_button(self, ctx):
        # self.check_roles(ctx)

        async def button_callback(interaction: discord.Interaction):
            if interaction.user not in self.players:
                self.players.append(interaction.user)
                await interaction.response.send_message("You have been registered", ephemeral=True, delete_after=5)
            else:
                await interaction.response.send_message("You are already registered", ephemeral=True, delete_after=5)

        button = discord.ui.Button(label="Register", style=discord.ButtonStyle.green)
        button.callback = button_callback

        view = discord.ui.View()
        view.add_item(button)

        await ctx.respond("Ajoutez vous aux participants", view=view)

    @commands.slash_command()
    async def draw_tables(self, ctx, max_players: int = 5):
        # self.check_roles(ctx)
        list_players = self.players.copy()
        while len(list_players) > 0:
            pick_up = ch(list_players)
            if len(self.table[f"Table {len(self.table)}"]) == max_players:
                self.table[f"Table {len(self.table) + 1}"] = []
            self.table[f"Table {len(self.table)}"].append(pick_up)
            list_players.remove(pick_up)

        embed = discord.Embed(title="Tables",
                              description="Distribution des tables",
                              color=0x00ff00)

        for table, members in self.table.items():
            member_names = [member.display_name for member in members]
            embed.add_field(name=table, value='\n'.join(member_names), inline=True)

        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def delete_tables(self, ctx):
        # self.check_roles(ctx)
        self.table.clear()
        await ctx.respond("Tables supprimées", ephemeral=True)
