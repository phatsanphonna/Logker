import discord
from discord.ext import commands
import events.reaction_events as reaction_events
from events.find_info import find_guild_info


class Reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_reaction_add')
    async def reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        info = await find_guild_info(user.guild.id)

        if user.guild.id == info['guild_id']:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            embed = (
                reaction_events.reaction_add_en(reaction, user) if config_lang == 'EN'
                else reaction_events.reaction_add_th(reaction, user)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_reaction_remove')
    async def reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        info = await find_guild_info(user.guild.id)

        if user.guild.id == info['guild_id']:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'EN' if info is None else info['logs_language']

            embed = (
                reaction_events.reaction_remove_en(reaction, user) if config_lang == 'EN'
                else reaction_events.reaction_remove_th(reaction, user)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Reaction(client))
