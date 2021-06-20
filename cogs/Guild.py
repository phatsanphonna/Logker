import discord
from discord.ext import commands
from utils.database import Database
from messages import guild_events_msg


class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_guild_update')
    async def guild_name_update(self, before: discord.Guild, after: discord.Guild):
        db = Database(before.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == after.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            if before.name != after.name:
                # Set language version of embed message
                embed = (
                    guild_events_msg.guild_name_update_en(before, after) if config_lang == 'en'
                    else guild_events_msg.guild_name_update_en(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_update')
    async def guild_afk_channel_update(self, before: discord.Guild, after: discord.Guild):
        db = Database(before.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == after.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            if before.afk_channel != after.afk_channel:
                # Set language version of embed message
                embed = (
                    guild_events_msg.guild_afk_channel_update_en(before, after) if config_lang == 'en'
                    else guild_events_msg.guild_afk_channel_update_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        db = Database(invite.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == invite.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                guild_events_msg.guild_invite_create_en(invite) if config_lang == 'en'
                else guild_events_msg.guild_invite_create_th(invite)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        db = Database(invite.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == invite.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                guild_events_msg.guild_invite_delete_en(invite) if config_lang == 'en'
                else guild_events_msg.guild_invite_delete_th(invite)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Guild(client))
