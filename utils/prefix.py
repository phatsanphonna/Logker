import discord
from utils.database import Database


async def command_find_prefix(_, message):
    if message.channel.type is discord.ChannelType.private:
        return '|'
    else:
        db = Database(message.guild.id)
        prefix = await db.find_prefix()

        if prefix is None:
            return '|'
        else:
            return prefix
