import discord
from messages import role_events_msg
from discord.ext import commands
from utils.database import Database


class Role(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        info = await Database.find_info(role.guild.id)

        if info is None:
            return

        if info[0] == role.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                role_events_msg.guild_role_create_en(role) if config_lang == 'en'
                else role_events_msg.guild_role_create_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        info = await Database.find_info(role.guild.id)

        if info is None:
            return

        if info[0] == role.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                role_events_msg.guild_role_delete_en(role) if config_lang == 'en'
                else role_events_msg.guild_role_delete_th(role)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_role_update')
    async def guild_role_name_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        info = await Database.find_info(after.guild.id)

        if info is None:
            return

        if info[0] == after.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.name != after.name:
                # Set language version of embed message
                embed = (
                    role_events_msg.guild_role_name_update_en(before, after) if config_lang == 'en'
                    else role_events_msg.guild_role_name_update_en(before, after)
                )

                await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Role(client))
