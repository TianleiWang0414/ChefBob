import discord
import aiofiles
import json


def getChannelByName(ctx, name):
    channels = ctx.guild.voice_channels

    channelObj = None
    for x in channels:
        # print(name.lower+" "+x.name.lower)
        if name.lower() in x.name.lower():
            channelObj = x
            break
    return channelObj


def form_event(title: str, description: str, time: str) -> str:
    template = "**%s**\n_%s_\n%s\n\n Current member:\n" % (title, time, description)

    return template


def __role_string(member: list, role: list, bot) -> str:
    role_str = ""

    for i in range(len(member)):
        emoji = discord.utils.get(bot.emojis, name=role[i])
        role_str += "%s %s\n" % (member[i], emoji)
    return role_str


def update_event(json_file, message, bot) -> str:
    new_str = form_event(json_file[str(message.id)]['title'],
                         json_file[str(message.id)]['desc'],
                         json_file[str(message.id)]['time']) + \
              __role_string(json_file[str(message.id)]['members'],
                            json_file[str(message.id)]['role'], bot)
    return new_str


async def json_write(json_file):
    async with aiofiles.open('event.json', mode='w') as f:
        new_str = json.dumps(json_file)
        await f.write(new_str)



