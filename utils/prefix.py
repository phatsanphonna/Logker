import discord
from utils.database import Database


async def command_find_prefix(_, message):
    if message.channel.type is discord.ChannelType.private:
        return '|'
    else:
        prefix = await Database.find_prefix(message.guild.id)
        if prefix is None:
            return '|'
        else:
            return prefix
