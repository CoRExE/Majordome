#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Moderation(bot))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def cls(self, ctx, num: int):
        """
        Supprime le nombre de messages indiqué
        :param ctx:
        :param num:
        :return:
        """
        await ctx.respond("Suppression lancée !", delete_after=5, ephemeral=True)
        msgs = await ctx.channel.history(limit=num).flatten()
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
    async def create_poll_fast(self, ctx, question: str, anonymous: bool = False):
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.green,
                label="Yes"),
            discord.ui.Button(
                style=discord.ButtonStyle.red,
                label="No")
        ]

        view = discord.ui.View()

        embed = discord.Embed(
            title="Question",
            description=question
        ).set_footer(text="Requested by {}".format(ctx.author.name))

        if anonymous:
            embed.add_field(
                name="Participants",
                value=""
            )
        else:
            embed.add_field(
                name="Yes",
                value="",
                inline=True
            )

            embed.add_field(
                name="No",
                value="",
                inline=True
            )

        def buttons_callback(interaction: discord.Interaction):
            interaction.response.edit_message(interaction)
            print(interaction)

        for button in buttons:
            button.callback = buttons_callback
            # Error in callback attribute
            view.add_item(button)

        await ctx.respond(embed=embed, view=view)
