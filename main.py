from random import randint
import os
from dotenv import load_dotenv
import discord
import utils
from discord.ext import commands
import datetime as dt
import json
import aiofiles
import multiprocessing

intents = discord.Intents.default()
intents.members = True
load_dotenv()
lock = multiprocessing.Lock()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="+", intents=intents)
dps_role = []
job_list = ['gbb', 'dnc', 'rep', 'drk', 'sch', 'whm', 'sge', 'rdm', 'war', 'sam', 'drg', 'mok', 'smn', 'nin',
            'brd', 'pld', 'mch', 'blm', 'ast']


# bot commands
@bot.command(name="event")
async def create_event(ctx, title, description, time, limit_people):
    lock.acquire()
    channel = ctx.message.channel.name
    if channel != 'events':
        await ctx.send(':no_entry:Please use event command under **events** channel.', delete_after=5)
        return
    try:
        date_time_obj = dt.datetime.strptime(time, '%Y/%m/%d')
    except Exception as e:
        print(e)
        await ctx.send(e)
        return
    async with aiofiles.open('event.json') as f:
        contents = await f.read()
        # print(contents)
    json_file = json.loads(contents)

    event = utils.form_event(title, description, time)
    message = await ctx.send(event)

    json_file[(message.id)] = {'members': [], 'role': [], 'title': title, 'desc': description, 'time': time,
                               'limit': limit_people}

    async with aiofiles.open('event.json', mode='w') as f:
        str = json.dumps(json_file)
        print(str)
        await f.write(str)
    print('event invoked')
    lock.release()


def role_string(member: list, role: list) -> str:
    role_str = ""

    for i in range(len(member)):
        emoji = discord.utils.get(bot.emojis, name=role[i])
        role_str += "%s %s\n" % (member[i], emoji)
    return role_str


@bot.event
async def on_reaction_add(reaction, user):
    lock.acquire()
    channel = reaction.message.channel
    message = reaction.message
    emoji = reaction.emoji
    print(message)
    async with aiofiles.open('event.json') as f:
        contents = await f.read()
    json_file = json.loads(contents)
    # print(type(message.id))

    if user.name not in json_file[str(message.id)]['members'] and \
            len(json_file[str(message.id)]['members']) < int(json_file[str(message.id)]['limit']):
        json_file[str(message.id)]['members'].append(user.name)
        try:
            if emoji.name not in job_list:
                return
        except:
            return

        json_file[str(message.id)]['role'].append(emoji.name)
        new_str = utils.form_event(json_file[str(message.id)]['title'],
                                   json_file[str(message.id)]['desc'],
                                   json_file[str(message.id)]['time']) + \
                  role_string(json_file[str(message.id)]['members'],
                              json_file[str(message.id)]['role'])
        await message.edit(content=new_str)
    else:
        error = '<@%s>  :no_entry:\nPossible cause:\n1. Party full\n2. Already in this party' % (user.id)
        await message.channel.send(error, delete_after=15)
    print(json_file)
    async with aiofiles.open('event.json', mode='w') as f:
        new_str = json.dumps(json_file)
        await f.write(new_str)
    lock.release()


@bot.event
async def on_reaction_remove(reaction, user):
    lock.acquire()
    channel = reaction.message.channel
    message = reaction.message
    async with aiofiles.open('event.json') as f:
        contents = await f.read()
    json_file = json.loads(contents)
    # print(type(message.id))
    try:

        index = json_file[str(message.id)]['members'].index(user.name)
        if json_file[str(message.id)]['role'][index] != reaction.emoji.name:
            return
        json_file[str(message.id)]['members'].remove(user.name)
        json_file[str(message.id)]['role'].pop(index)
        new_str = utils.form_event(json_file[str(message.id)]['title'],
                                   json_file[str(message.id)]['desc'],
                                   json_file[str(message.id)]['time']) + \
                  role_string(json_file[str(message.id)]['members'],
                              json_file[str(message.id)]['role'])
        await message.edit(content=new_str)
    except:
        pass
    print(json_file)
    async with aiofiles.open('event.json', mode='w') as f:
        new_str = json.dumps(json_file)
        await f.write(new_str)
    lock.release()


@bot.command(name="唱")
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


@bot.command(name="换区")
async def move(ctx, *arg):
    goto = utils.getChannelByName(ctx, " ".join(arg))
    if goto is None:
        print("Channel not found")
        await ctx.send("未能找到频道", delete_after=5)
        return
    try:
        members = ctx.message.author.voice.channel.members
        channel = ctx.message.author.voice.channel
    except AttributeError:
        await ctx.send("X 未在语音频道", delete_after=5)
        return
    if (channel.name != goto.name) and type(channel) is discord.VoiceChannel:
        for x in members:
            await x.move_to(goto)
        await ctx.send("转移成功", delete_after=5)
    else:
        await ctx.send("原地传送最为致命", delete_after=5)


@bot.command(pass_cibtext=True, aliases=['move', 'change'])
async def ch(ctx, *arg):
    await move(ctx, *arg)


@bot.command(name="骰子")
async def rng(ctx, arg):
    number = 0
    print("roll invoked")
    try:
        number = int(arg) + 1
    except ValueError:
        await ctx.send("老B不明白你在说什么")
        return
    member = ctx.message.author
    number = randint(1, number)
    string = "<@" + str(member.id) + "> 点数：" + str(number)

    await ctx.send(string)


@bot.command(pass_cibtext=True, aliases=['rng', 'roll'])
async def r(ctx, arg):
    await rng(ctx, arg)


# bot events
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


@create_event.error
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Bob表示你的活动有点问题。\n +event title description time people_limit(int)", delete_after=15)


@bot.event
async def on_ready():
    print("**{0.user.name}** 踩着七彩祥云来取你狗命了".format(bot))


bot.run(TOKEN)
