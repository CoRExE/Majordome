#  Copyright (c) 2023.
#  Ceci est une propriété de CoRE.ExE, vous êtes autorisés à l'intégration de ce produit.
#  Il est formellement interdit de monétiser ce contenu.
#  Toute infraction aux règles précédemment citée pourra engager des poursuites.

import discord
from discord.ext import commands
from discord.ui import Button, View


def setup(bot):
    bot.add_cog(SoulLink(bot))


class Pokemon:
    def __init__(self, lieu: str, surnom: str, specie: str | None = None):
        self.specie: str = specie
        self.surnom: str = surnom
        self.lieu: str = lieu


class Dresseur:
    def __init__(self, member: discord.Member, link_trainer: discord.Member):
        self.id: discord.Member = member
        self.squad: list[Pokemon] = []
        self.linked_trainer: discord.Member = link_trainer

    def __add__(self, other: Pokemon):
        self.squad.append(other)


class SoulLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.link_players: list[tuple[discord.Member, ...]] = []
        self.players: dict[str] = {}

    @commands.slash_command()
    async def soul_link_rules(self, ctx):
        embed_rules = discord.Embed(title="Règles du Soul Link", color=0xff0000)

        embed_rules.set_thumbnail(url="https://cdn.discordapp.com/attachments/1122876630948380702/1134982895933603960"
                                      "/4PWmR6k74DiTcAAAAASUVORK5CYII.png")

        embed_rules.add_field(name="__Règle 1__", value="Le premier pokémon de Zone")
        embed_rules.add_field(name="__Règle 2__", value="Chaque pokémon est lié au pokémon de la même zone de l'autre "
                                                        "dresseur")
        embed_rules.add_field(name="__Règles 3__", value="Pas de pokémon identique dans une équipe")

        embed_rules.set_footer(text="_Capture des Chromatiques Autorisé_")

        await ctx.respond(embed=embed_rules)

    @commands.slash_command()
    async def soul_link(self, ctx, dresseur: discord.Member | None = None):
        """
        Génère une association entre deux membres
        :param dresseur:
        :param ctx:
        :return:
        """
        soul1 = ctx.author

        join_button = Button(style=discord.ButtonStyle.blurple, label="Link !", custom_id="accept")

        link = discord.ui.button(label="Link", emoji=":knot:")

        await ctx.respond("Command Not Finish")
