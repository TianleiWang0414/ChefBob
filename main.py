from random import randint
import os
from dotenv import load_dotenv
import discord
import utils
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="+", intents=intents)





#bot commands
@bot.command()
async def sing(ctx):
    print("sing command invoked")
    await ctx.send("来左边儿 跟我一起画个龙~\n在你右边儿 画一道彩虹~")


@bot.command()
async def clear(ctx, num):
    msg = []
    number = 0
    try:
        number = int(num)
    except ValueError:
        await ctx.send("老B不明白你在说什么")
        return
    if number <= 0:
        return
    async for x in ctx.channel.history(limit=number):
        msg.append(x)
    await ctx.channel.delete_messages(msg)
    await ctx.send("Chef老B 清档成功 此消息5秒后自我销毁", delete_after=5)


@bot.command(name="change")
async def move(ctx, *arg):

    goto = utils.getChannelByName(ctx, " ".join(arg))
    if goto is None:
        print("Channel not found")
        return
    members = ctx.message.author.voice.channel.members
    channel = ctx.message.author.voice.channel
    if channel.name!=goto.name:
        for x in members:
            await x.move_to(goto)
            await ctx.send("转移成功", delete_after=5)
    else:
        await ctx.send("原地传送最为致命", delete_after=5)
@bot.command(pass_cibtext=True,aliases=['move'])
async def ch(ctx, *arg):
    await move(ctx,*arg)
@bot.command(name="roll")
async def rng(ctx,arg):
    number = 0
    print("roll invoked")
    try:
        number = int(arg)+1
    except ValueError:
        await ctx.send("老B不明白你在说什么")
        return
    member = ctx.message.author
    number= randint(1,number)
    string="<@"+str(member.id)+"> 点数："+ str(number)

    await ctx.send(string)

#bot events
@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
    except discord.ext.commands.errors:
        print("an error has occurred")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Bob挠了挠头.jpg")

@bot.event
async def on_ready():
    print("**{0.user.name}** 踩着七彩祥云来去你狗命了".format(bot))
bot.run(TOKEN)
