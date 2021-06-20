from discord.ext import commands
from messages import message_events_msg
from utils.database import Database


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        db = Database(message.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        # Check if guild_id is equal to message.guild.id
        if info['guild_id'] == message.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events_msg.message_delete_en(message) if config_lang == 'en'
                else message_events_msg.message_delete_th(message)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message:
            return

        db = Database(payload.guild_id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        # Check if guild_id is equal to payload.guild.id
        if info['guild_id'] == payload.guild_id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events_msg.raw_message_edit_en(payload.cached_message) if config_lang == 'en'
                else message_events_msg.raw_message_edit_th(payload.cached_message)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        db = Database(before.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        # Check if guild_id is equal to message.guild.id
        if info['guild_id'] == after.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            if before.content != after.content:
                # Set language version of embed message
                embed = (
                    message_events_msg.message_edit_en(before, after) if config_lang == 'en'
                    else message_events_msg.message_edit_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.cached_message:
            return

        db = Database(payload.guild_id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        # Check if guild_id is equal to payload.guild.id
        if info['guild_id'] == payload.guild_id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events_msg.raw_message_edit_en(payload.cached_message) if config_lang == 'en'
                else message_events_msg.raw_message_edit_th(payload.cached_message)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Message(client))
