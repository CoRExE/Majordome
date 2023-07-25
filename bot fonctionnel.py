from discord.ext import commands
import random
from BotExtensions.addPack import jeton
from BotExtensions.Personal_Modals import *

intents = discord.Intents.default()
default_intents = discord.Intents.default()

default_intents.members = True
intents.message_content = True

client = discord.Client(intents=default_intents)
bot = commands.Bot(command_prefix='!', intents=intents)


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


bot.load_extension("BotExtensions.ModerateExtend")
bot.load_extension("BotExtensions.DiscordMinigames")


async def reload_extension(extensions: str | list[str]):
    if type(extensions) is list:
        for extension in extensions:
            bot.reload_extension(extension)


bot.run(jeton)
