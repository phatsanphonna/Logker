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

        # Seek info of guild
        info = await Database.find_info(message.guild.id)

        if info is None:
            return

        # Check if guild_id is equal to message.guild.id
        if info[0] == message.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

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

        # Seek info of guild
        info = await Database.find_info(payload.guild_id)

        if info is None:
            return

        # Check if guild_id is equal to message.guild.id
        if info[0] == payload.guild_id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

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

        # Seek info of guild
        info = await Database.find_info(before.guild.id)

        if info is None:
            return

        # Check if guild_id is equal to message.guild.id
        if info[0] == after.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

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

        # Seek info of guild
        info = await Database.find_info(payload.guild_id)

        if info is None:
            return

        # Check if guild_id is equal to payload.guild.id
        if info[0] == payload.guild_id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                message_events_msg.raw_message_edit_en(payload.cached_message) if config_lang == 'en'
                else message_events_msg.raw_message_edit_th(payload.cached_message)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Message(client))
