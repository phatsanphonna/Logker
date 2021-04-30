from discord.ext import commands
import events.message_events as message_events
from events.find_info import find_guild_info


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        # Seek info of guild
        info = await find_guild_info(message.guild.id)

        # Check if guild_id is equal to message.guild.id
        if info['guild_id'] == message.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events.message_delete_en(message) if config_lang == 'EN'
                else message_events.message_delete_th(message)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.cached_message:
            return

        # Seek info of guild
        info = await find_guild_info(payload.guild_id)

        # Check if guild_id is equal to message.guild.id
        if info['guild_id'] == payload.guild_id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events.raw_message_edit_en(payload.cached_message) if config_lang == 'EN'
                else message_events.raw_message_edit_th(payload.cached_message)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        # Seek info of guild
        info = await find_guild_info(after.guild.id)

        # Check if guild_id is equal to message.guild.id
        if info['guild_id'] == after.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            if before.content != after.content:
                # Set language version of embed message
                embed = (
                    message_events.message_edit_en(before, after) if config_lang == 'EN'
                    else message_events.message_edit_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload.cached_message:
            return

        # Seek info of guild
        info = await find_guild_info(payload.guild_id)

        # Check if guild_id is equal to payload.guild.id
        if info['guild_id'] == payload.guild_id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                message_events.raw_message_edit_en(payload.cached_message) if config_lang == 'EN'
                else message_events.raw_message_edit_th(payload.cached_message)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Message(client))
