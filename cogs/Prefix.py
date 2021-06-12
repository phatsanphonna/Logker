import discord
from discord.ext import commands
from utils.database import Database


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_prefix = await Database.find_prefix(guild.id)

        if guild_prefix is None:
            await Database.insert_prefix(guild.id)

    @commands.Cog.listener('on_message')
    async def prefix_find(self, message: discord.Message):
        if message.author is self.client.user:
            return
        if message.author.bot:
            return

        if "Logker, What is your prefix?" in message.content:
            guild_prefix = await Database.find_prefix(message.guild.id)
            await message.channel.send(f'Logker prefix of this server is **{guild_prefix}**')

        if "Logker, prefix ของแกคืออะไร" in message.content:
            guild_prefix = await Database.find_prefix(message.guild.id)
            await message.channel.send(f'prefix ของ Logker สำหรับเซิฟเวอร์นี้คือ **{guild_prefix}**')


def setup(client):
    client.add_cog(Prefix(client))
