import discord
from discord.ext import commands
from utils.database import Database


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = Database(guild.id)  # Create a new instance

        if not await db.prefix_exists():  # Check if that server has Logker setup?
            return

        await db.insert_prefix()

    @commands.Cog.listener('on_message')
    async def prefix_find(self, message: discord.Message):
        if message.author is self.client.user:
            return
        if message.author.bot:
            return

        if "Logker, What is your prefix?" in message.content:
            if message.guild is None:
                await message.channel.send(f'Logker prefix of this DM is **|**')
                return

            db = Database(message.guild.id)  # Create a new instance
            guild_prefix = await db.find_prefix()

            await message.channel.send(f'Logker prefix of this server is **{guild_prefix}**')

        if "Logker, prefix ของแกคืออะไร" in message.content:
            if message.guild is None:
                await message.channel.send(f'prefix ของ Logker สำหรับแชทส่วนตัวนี้คือ **|**')
                return

            db = Database(message.guild.id)  # Create a new instance
            guild_prefix = await db.find_prefix()
            
            await message.channel.send(f'prefix ของ Logker สำหรับเซิฟเวอร์นี้คือ **{guild_prefix}**')


def setup(client):
    client.add_cog(Prefix(client))
