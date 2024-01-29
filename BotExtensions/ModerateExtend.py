#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.
from asyncio import sleep

import discord
from discord.ext import commands


def setup(bot):
    bot.add_cog(Moderation(bot))


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.variable_temp: dict = {}

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
    async def create_poll_fast(self, ctx, question: str, anonymous: bool = False, duration: int = 120):
        self.variable_temp['participants'] = []
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.green,
                label="Yes",
                custom_id="yes"),
            discord.ui.Button(
                style=discord.ButtonStyle.red,
                label="No")
        ]

        view = discord.ui.View(timeout=duration, disable_on_timeout=True)

        embed = discord.Embed(
            title="Question",
            description=question
        ).set_footer(text="Requested by {}".format(ctx.author.name))

        if anonymous:
            embed.add_field(
                name="Participants",
                value="0"
            )
            self.variable_temp['yes'] = 0
            self.variable_temp['no'] = 0
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

        if anonymous:
            async def buttons_callback(interaction: discord.Interaction):
                if interaction.user.name in self.variable_temp['participants']:
                    await interaction.response.send_message("You already voted!", ephemeral=True)
                else:
                    embed.fields[0].value = int(embed.fields[0].value) + 1
                    self.variable_temp[interaction.custom_id] += 1
                    await interaction.response.edit_message(embed=embed, view=view)
                    self.variable_temp['participants'].append(interaction.user.name)
        else:
            async def buttons_callback(interaction: discord.Interaction):
                if interaction.user.name in self.variable_temp['participants']:
                    await interaction.response.send_message("You already voted!", ephemeral=True)
                elif interaction.custom_id == "yes":
                    embed.fields[0].value += interaction.user.name + "\n"
                    await interaction.response.edit_message(embed=embed, view=view)
                    self.variable_temp['participants'].append(interaction.user.name)
                else:
                    embed.fields[1].value += interaction.user.name + "\n"
                    await interaction.response.edit_message(embed=embed, view=view)
                    self.variable_temp['participants'].append(interaction.user.name)

        async def on_timeout():
            # int in test are broken
            if self.variable_temp['participants'].__len__() == 0:
                embed.clear_fields()
                embed.add_field(
                    name="Résultat",
                    value="Aucun Vote"
                )
            elif int(embed.fields[0].value) > int(embed.fields[1].value):
                embed.clear_fields()
                embed.add_field(
                    name="Résultat",
                    value="Yes"
                )
            elif int(embed.fields[0].value) < int(embed.fields[1].value):
                embed.clear_fields()
                embed.add_field(
                    name="Résultat",
                    value="No"
                )
            else:
                embed.clear_fields()
                embed.add_field(
                    name="Résultat",
                    value="Tie"
                )
            await message.edit_original_response(embed=embed, view=None)
            self.variable_temp.clear()

        view.on_timeout = on_timeout

        for button in buttons:
            button.callback = buttons_callback
            view.add_item(button)

        message = await ctx.respond(embed=embed, view=view)

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
