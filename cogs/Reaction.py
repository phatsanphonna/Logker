import discord
from discord.ext import commands
from messages import reaction_events_msg
from utils.database import Database


class Reaction(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener('on_reaction_add')
    async def reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot:
            return

        db = Database(user.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == user.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            embed = (
                reaction_events_msg.reaction_add_en(reaction, user) if config_lang == 'en'
                else reaction_events_msg.reaction_add_th(reaction, user)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_reaction_remove')
    async def reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot:
            return

        db = Database(user.guild.id)  # Create a new instance

        if not await db.info_exists():  # Check if that server has Logker setup?
            return

        info = await db.find_info()

        if info['guild_id'] == user.guild.id:
            logs_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])
            config_lang = 'en' if info is None else info['logs_language']

            embed = (
                reaction_events_msg.reaction_remove_en(reaction, user) if config_lang == 'en'
                else reaction_events_msg.reaction_remove_th(reaction, user)
            )

            await logs_channel.send(embed=embed)


def setup(client):
    client.add_cog(Reaction(client))
