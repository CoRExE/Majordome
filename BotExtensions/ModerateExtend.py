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
        await ctx.respond("Suppression lancée !")
        msgs = await ctx.channel.history(limit=num + 1).flatten()
        for msg in msgs:
            await msg.delete()

    @commands.command()
    async def rules(self, ctx):
        await ctx.send("Les règles:\n1. Pas d'Insultes\n2.Pas de Doubles Compte\n3.Pas de Spam")
        print(ctx.author)

    @commands.command()
    async def def_rules(self, ctx):
        await ctx.send("Les règles sont faites pour être Rompu")

    @commands.command()
    async def bienvenue(self, ctx, nouveau_membre: discord.Member):
        pseudo = nouveau_membre.mention
        await ctx.send(f"Bienvenue à {pseudo}, soit près, ici tes données te seront ta seul monnaie")

    # verifier l'erreur
    @bienvenue.error
    async def on_command_error(self, ctx, error):
        # detect this error
        if isinstance(error, commands.MissingRequiredArgument):
            # envoyer un message
            await ctx.send("Tu dois faire $bienvenue @pseudo\nJeune Duelist")

    @commands.command()
    async def joined(self, ctx, *, member: discord.Member):
        await ctx.send('{0} joined on {0.joined_at}'.format(member))
