import discord
from discord.ext import commands
import random
from BotExtensions.addPack import jeton
from BotExtensions.Personal_Modals import *
from os.path import exists

intents = discord.Intents.default()
default_intents = discord.Intents.default()

default_intents.members = True
intents.message_content = True

client = discord.Client(intents=default_intents)
bot = commands.Bot(command_prefix='!', intents=intents)

bot_extensions = []


@bot.event
async def on_ready():
    print("My body is ready !")
    await bot.change_presence(status=discord.Status.idle,
                              activity=discord.Game("Dévellopement d'un Bot"))
    print("It's good")


@client.event
async def on_member_join(member):
    print(f"L'utilisateur {member.display_name} a rejoint le serveur !")


@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)


@bot.command()
async def secret(ctx, *, message):
    print(ctx.author)
    await ctx.author.send(message)


def webcheck(abe):
    temp = ''
    for ab in range(len(abe)):
        if abe[ab] == ' ':
            temp += '%20'
        else:
            temp += abe[ab]
    return temp


@bot.command()
async def game_421(ctx):
    pound = []
    for i in range(3):
        pound.append(random.randint(1, 6))
    await ctx.send(pound.sort(reverse=True))


# Internet

@bot.command()
async def search(ctx, *, msg):
    await ctx.send('https://www.google.fr/search?q=' + webcheck(msg))


@bot.command()
async def search_im(ctx, *, msg):
    await ctx.send('https://www.google.fr/search?q=' + webcheck(msg) + '&source=Inms&tbm=isch')


@bot.command()
async def search_v(ctx, *, msg):
    await ctx.send('https://www.google.fr/search?q=' + webcheck(msg) + '&source=Inms&tbm=vid')


@bot.command()
async def translate(ctx, lang1, lang2, *, msg):
    await ctx.send(f'https://translate.google.com/?sl={lang1}&tl={lang2}&text={webcheck(msg)}&op=translate')


# emoji custom <:emoji_name:emoji_id>


@bot.command()
async def test(ctx):
    await ctx.send(str(ctx.author) + ' <:Tim_Coins:944004800369033256>')


@bot.command()
async def send_modal(ctx):
    await ctx.send(view=ModalView())


@bot.command()
@commands.has_permissions(administrator=True)
async def load_extension(ctx, extensions: str):
    if "," in extensions:
        extensions = extensions.split(",")
        for extension in extensions:
            if exists("BotExtensions/" + extension):
                bot.load_extension("BotExtensions/" + extension)
                await ctx.send(f"Extension : {extension} loaded !")
            else:
                await ctx.send(f"L'extension {extension} n'existe pas", ephemeral=True)
    elif exists("BotExtensions/" + extensions):
        bot.load_extension("BotExtensions/" + extensions)
        await ctx.send(f"Extension : {extensions} loaded")
    else:
        await ctx.send(f"L'extension {extensions} n'existe pas", ephemeral=True)


@bot.command()
@commands.has_permissions(administrator=True)
async def reload_extension(ctx, extensions: str | list[str] | None = None):
    if extensions is None:
        for extension in bot.extensions.keys():
            bot.reload_extension(extension)
            for ext in bot.extensions.keys():
                await ctx.send(f"Extensions : {ext}", delete_after=15)


@bot.command()
@commands.has_permissions(administrator=True)
async def unload_extension(ctx, extensions: str | list[str]):
    if type(extensions) is list:
        for extension in extensions:
            if extension in bot.extensions.keys():
                bot.unload_extension(extension)
                await ctx.send(f"Extension {extension} unload", ephemeral=True)
            else:
                await ctx.send(f"Extension {extension} isn't found in actives extensions")
    elif type(extensions) is str and extensions in bot.extensions.keys():
        bot.unload_extension(extensions)
        await ctx.send(f"{extensions} unload !", ephemeral=True)


bot.load_extension("BotExtensions.ModerateExtend")
bot.load_extension("BotExtensions.DiscordMinigames")
# bot.load_extension("BotExtensions.SoulLink")
bot.load_extension("BotExtensions.PokeExtension")
bot.load_extension("BotExtensions.troll")
bot.load_extension("BotExtensions.Economy")
bot.load_extension("BotExtensions.AIExtension")
bot.run(jeton)
