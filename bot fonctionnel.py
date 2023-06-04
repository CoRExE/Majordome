from discord.ext import commands
import random
from BotExtentions.addPack import jeton
from BotExtentions.Personal_Modals import *

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
async def MPsomeone(ctx, mention: discord.Member):
    await mention.send('MP message from `!MPsomeone` command by : ' + str(ctx.author))
    print(str(ctx.author) + " Used the MPsomeone command on : " + str(mention))


@bot.command()
async def secret(ctx, *, message):
    print(ctx.author)
    await ctx.author.send(message)


@bot.command()
async def randomize(ctx, *, msg):
    msg = msg.split('-')
    await ctx.send(random.choice(msg))


@bot.command()
async def roll(ctx, *, msg):
    msg = int(msg)
    if random.randint(0, 99) == 0:
        await ctx.reply('https://youtu.be/dQw4w9WgXcQ')
    else:
        await ctx.reply(random.randint(0, msg), mention_author=False)


@bot.command()
async def pile_face(ctx):
    await ctx.reply(random.choice(['Pile', 'Face']), mention_author=False)


@bot.command()
async def pfc(ctx):
    """
    TODO With Button
    :param ctx:
    :return:
    """


# any reaction
@pfc.error
async def on_pfc_error(ctx, error):
    if isinstance(error, AssertionError):
        await ctx.send("You can only put {p,f,c}")


@bot.command()
async def calc(ctx, *, msg):
    num = []
    syb = []
    for pee in msg:
        pass


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
    await ctx.send(pound)


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


# TROLL COMMAND


@bot.command()
async def yes(ctx):
    await ctx.send('https://tenor.com/view/jojo-anime-yes-yes-yes-yeah-its-a-yes-gif-17161748')
    await ctx.message.delete()


@bot.command()
async def noice(ctx):
    await ctx.send('https://tenor.com/view/noice-nice-click-gif-8843762')
    await ctx.message.delete()


@bot.command()
async def rick(ctx):
    await ctx.send('https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173')
    await ctx.message.delete()


@bot.command()
async def Ooh(ctx):
    await ctx.send('https://tenor.com/view/%D1%81%D1%80%D1%81%D0%BC-%D0%B1%D0%B5%D0%BB%D0%B0-%D0%B8%D0%BD%D0%B5%D0%BD'
                   '%D0%B0%D0%B4%D0%B0-%D0%B8%D0%B7%D0%BD%D0%B5%D0%BD%D0%B0%D0%B4%D0%B0-%D1%81%D0%BC%D1%8F%D1%85-gif'
                   '-24523449')
    await ctx.message.delete()


@bot.command()
async def yeet(ctx):
    await ctx.send("https://tenor.com/view/whats-a-yeet-playing-gif-15038419")
    await ctx.message.delete()


@bot.command()
async def groult(ctx):
    await ctx.send(
        'https://cdn.vox-cdn.com/thumbor/yzPdGsXFWCHbNMlDWHhPROUzVeI=/1400x1400/filters:format('
        'jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/8378039/baby-groot-guardians.0.jpg')
    await ctx.message.delete()


@bot.command()
async def send_modal(ctx):
    await ctx.send(view=MyView())

bot.load_extension("ModerateExtend")

bot.run(jeton)
