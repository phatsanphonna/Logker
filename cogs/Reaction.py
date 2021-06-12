import discord
from discord.ext import commands
from messages import reaction_events_msg
from utils.database import Database


class Reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_reaction_add')
    async def reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        info = await Database.find_info(user.guild.id)

        if info is None:
            return

        if user.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            embed = (
                reaction_events_msg.reaction_add_en(reaction, user) if config_lang == 'en'
                else reaction_events_msg.reaction_add_th(reaction, user)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_reaction_remove')
    async def reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        info = await Database.find_info(user.guild.id)

        if info is None:
            return

        if user.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            embed = (
                reaction_events_msg.reaction_remove_en(reaction, user) if config_lang == 'en'
                else reaction_events_msg.reaction_remove_th(reaction, user)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Reaction(client))
