def getChannelByName(ctx,name):
    channels = ctx.guild.voice_channels

    channelObj=None
    for x in channels:
       # print(name.lower+" "+x.name.lower)
        if name.lower() in x.name.lower():
            channelObj= x
            break
    return channelObj