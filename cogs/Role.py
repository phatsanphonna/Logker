import discord
from discord.ext import commands
import events.role_events as role_events
from events.find_info import find_guild_info


class Role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        info = await find_guild_info(role.guild.id)

        if info['guild_id'] == role.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(
                info['guild_id']).get_channel(info['channel_id'])

            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                role_events.guild_role_create_en(role) if config_lang == 'EN'
                else role_events.guild_role_create_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        info = await find_guild_info(role.guild.id)

        if info['guild_id'] == role.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(
                info['guild_id']).get_channel(info['channel_id'])

            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = (
                role_events.guild_role_delete_en(role) if config_lang == 'EN'
                else role_events.guild_role_delete_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_role_update')
    async def guild_role_name_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        info = await find_guild_info(after.guild.id)

        if info['guild_id'] == after.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(
                info['guild_id']).get_channel(info['channel_id'])

            config_lang = 'EN' if info is None else info['logs_language']

            if before.name != after.name:
                # Set language version of embed message
                embed = (
                    role_events.guild_role_name_update_en(before, after) if config_lang == 'EN'
                    else role_events.guild_role_name_update_en(before, after)
                )

                await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Role(client))
