import discord
from messages import misc_msg
from discord.ext import commands
from utils.database import Database


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: **Logker** latency is {round(self.client.latency * 1000)}ms!')

    @commands.command()
    async def donate(self, ctx):
        owner = self.client.get_user(254515724804947969)
        await ctx.send(embed=misc_msg.donate(owner))

    @commands.command()
    async def info(self, ctx):
        try:
            db = Database(ctx.guild.id)  # Create a new instance

            info = await db.find_info()
            config_lang = info['logs_language'] if info is not None else 'en'

        except Exception:
            config_lang = 'en'

        owner = self.client.get_user(254515724804947969)

        await ctx.send(
            embed=misc_msg.info_en(ctx, owner, self.client) if config_lang == 'en'
            else misc_msg.info_en(ctx, owner, self.client)
        )

        await ctx.send(file=discord.File('assets/chaewon_muah.gif'))

    @commands.command()
    async def invite(self, ctx):
        owner = self.client.get_user(254515724804947969)
        await ctx.send(embed=misc_msg.invite(owner))

    @commands.command()
    async def github(self, ctx):
        owner = self.client.get_user(254515724804947969)
        await ctx.send(embed=misc_msg.github(owner))


def setup(client):
    client.add_cog(Misc(client))
