import discord
from discord.ext import commands
from utils.database import Database
from messages import channel_events_msg


class Channel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        info = await Database.find_info(channel.guild.id)

        if info is None:
            return

        if info[0] == channel.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                channel_events_msg.guild_channel_create_en(channel) if config_lang == 'en'
                else channel_events_msg.guild_channel_create_th(channel)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        info = await Database.find_info(channel.guild.id)

        if info is None:
            return

        if info[0] == channel.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                channel_events_msg.guild_channel_remove_en(channel) if config_lang == 'en'
                else channel_events_msg.guild_channel_remove_th(channel)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_channel_update')
    async def guild_channel_name_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        info = await Database.find_info(before.guild.id)

        if info is None:
            return

        if info[0] == after.guild.id:
            if before.name != after.name:
                logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
                config_lang = 'en' if info is None else info[2]

                # Set language version of embed message
                embed = (
                    channel_events_msg.guild_channel_name_update_en(before, after) if config_lang == 'en'
                    else channel_events_msg.guild_channel_name_update_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_channel_update')
    async def guild_channel_role_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        info = await Database.find_info(before.guild.id)

        if info is None:
            return

        if info[0] == before.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.changed_roles != after.changed_roles:
                before_total_roles = []
                for role in before.changed_roles:
                    if role not in after.changed_roles:
                        before_total_roles.append(role)

                after_total_roles = []
                for role in after.changed_roles:
                    if role not in before.changed_roles:
                        after_total_roles.append(role)

                embed = None
                if len(before_total_roles) == 1:
                    # Set language version of embed message
                    embed = (
                        channel_events_msg.guild_channel_role_remove_en(after, before_total_roles) if config_lang == 'EN'
                        else channel_events_msg.guild_channel_role_remove_th(after, before_total_roles)
                    )
                elif len(after_total_roles) == 1:
                    # Set language version of embed message
                    embed = (
                        channel_events_msg.guild_channel_role_append_en(after, after_total_roles) if config_lang == 'EN'
                        else channel_events_msg.guild_channel_role_append_th(after, after_total_roles)
                    )

                await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Channel(client))
