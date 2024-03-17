#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.
from asyncio import sleep
from Data.Manage_DataBase import ManageDB
import discord
from discord.ext import commands


def setup(bot):
    db = ManageDB(f"/Data")
    bot.add_cog(Moderation(bot, db))


class Moderation(commands.Cog):
    def __init__(self, bot, db: ManageDB):
        self.bot = bot
        self.variable_temp: dict = {}
        self.db = db

    # TODO : Corriger ces methods
    # def db_init(self):
    #     self.db.connexion("Moderation")
    #     if "Notes" not in self.db.show_tables("Moderation"):
    #         self.db.simple_create_table("Notes", [("ID", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    #                                               ("Title", "TEXT"),
    #                                               ("Note", "TEXT"),
    #                                               ("Owner", "TEXT")]
    #                                     )
    #
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.db_init()

    @commands.slash_command()
    async def avatar(self, ctx, member: discord.Member | None = None):
        """
        Montre votre avatar ou celui d'un membre cité
        :param member:
        :param ctx:
        :return None:
        """
        if member is None:
            await ctx.respond(ctx.author.avatar)
        else:
            await ctx.respond(member.avatar)

    @commands.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def cls(self, ctx, amount: int = 10, purge: bool = False):
        """
        Supprime le nombre de messages indiqué
        :param purge:
        :param ctx:
        :param amount:
        :return:
        """
        if purge:
            await ctx.respond("Suppression Complete Lancée !", delete_after=3, ephemeral=True)
            await sleep(5)
            await ctx.channel.purge()
        else:
            await ctx.respond("Suppression lancée !", delete_after=5, ephemeral=True)
            msgs = await ctx.channel.history(limit=amount).flatten()
            for msg in msgs:
                await msg.delete()

    @commands.slash_command()
    async def rules(self, ctx):
        await ctx.respond("Les règles:\n1. Pas d'Insultes\n2.Pas de Doubles Compte\n3.Pas de Spam")
        print(ctx.author)

    @commands.command()
    async def def_rules(self, ctx):
        await ctx.send("Les règles sont faites pour être Rompu")

    @commands.slash_command()
    @commands.has_permissions(manage_messages=True)
    async def users_profile(self, ctx, member: discord.Member):
        # Create an Embed to display the user's profile
        embed = discord.Embed(title=f"Profile for {member.display_name}", color=0x00ff00)
        embed.add_field(name="Username", value=member.name, inline=True)
        embed.add_field(name="ID", value=str(member.id), inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
        embed.add_field(name="Created At", value=member.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.add_field(name="Joined Server At", value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=True)
        embed.set_thumbnail(url=member.avatar)

        # Send the Embed as a response
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.respond('{0} joined on {0.joined_at}'.format(member))

    @commands.slash_command()
    async def citation(self, ctx, member: discord.Member, *, text: str):
        """
        Cite les conneries hors contexte d'un membre
        :param ctx:
        :param member: Le/la poète·e
        :param text: La citation
        :return:
        """
        embed = discord.Embed(
            title="Citation",
            description=text
        )
        embed.set_author(name=member.name, icon_url=member.avatar)
        embed.set_footer(text="Requested by {}".format(ctx.author.name), icon_url=ctx.author.avatar)
        await ctx.respond(embed=embed)

    @commands.slash_command()
    async def bloc_notes(self, ctx):
        pass
