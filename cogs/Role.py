import discord
from messages import role_events_msg
from discord.ext import commands
from utils.database import Database


class Role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        db = Database(role.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == role.guild.id:
            logs_channel = self.client.get_guild(
                info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                role_events_msg.guild_role_create_en(role) if config_lang == 'en'
                else role_events_msg.guild_role_create_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        db = Database(role.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == role.guild.id:
            logs_channel = self.client.get_guild(
                info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                role_events_msg.guild_role_delete_en(role) if config_lang == 'en'
                else role_events_msg.guild_role_delete_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_role_update')
    async def guild_role_name_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        db = Database(before.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == after.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            if before.name != after.name:
                # Set language version of embed message
                embed = (
                    role_events_msg.guild_role_name_update_en(before, after) if config_lang == 'en'
                    else role_events_msg.guild_role_name_update_en(before, after)
                )

                await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Role(client))
