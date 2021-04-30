import discord
from discord.ext import commands
import events.guild_events as guild_events
from events.find_info import find_guild_info


class Guild(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_guild_update')
    async def guild_name_update(self, before: discord.Guild, after: discord.Guild):
        info = await find_guild_info(after.id)

        if info['guild_id'] == after.id:

            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            if before.name != after.name:
                # Set language version of embed message
                embed = (
                    guild_events.guild_name_update_en(before, after) if config_lang == 'EN'
                    else guild_events.guild_name_update_en(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_guild_update')
    async def guild_afk_channel_update(self, before: discord.Guild, after: discord.Guild):
        info = await find_guild_info(after.id)

        if info['guild_id'] == after.id:

            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            if before.afk_channel != after.afk_channel:
                # Set language version of embed message
                embed = (
                    guild_events.guild_afk_channel_update_en(before, after) if config_lang == 'EN'
                    else guild_events.guild_afk_channel_update_th(before, after)
                )

                await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Guild(client))
