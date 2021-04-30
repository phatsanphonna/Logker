import discord
from discord.ext import commands
from events.find_info import find_guild_info
import events.client_events as client_events


class Client(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        uptime_channel = self.client.get_channel(833140105820242020)
        embed = client_events.uptime_restart()

        await uptime_channel.send(embed=embed)
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name=f'|help'))
        print('Client is online!')

    @commands.command()
    @commands.is_owner()
    async def logout(self, _):
        print('Client Logout!')
        await self.client.close()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                owner = self.client.get_user(254515724804947969)
                await channel.send(embed=client_events.guild_join(owner))
            break

    @commands.command()
    async def info(self, ctx):
        info = await find_guild_info(ctx.guild.id)
        config_lang = 'EN' if info is None else info['logs_language']
        owner = self.client.get_user(254515724804947969)
        client = self.client

        embed = client_events.info_en(ctx, owner, client) if config_lang == 'EN' else client_events.info_en(ctx, owner, client)

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':ping_pong: **Logker** latency is {round(self.client.latency * 1000)}ms!')

    @commands.Cog.listener('on_message')
    async def member_mention_client(self, message: discord.Message):
        # Prevent client responds to itself
        if message.author is self.client.user:
            return
        if message.author.bot:
            return
        if self.client.user.mentioned_in(message):
            info = await find_guild_info(message.guild.id)
            config_lang = 'EN' if info is None else info['logs_language']

            if '@here' in message.content:
                return
            if '@everyone' in message.content:
                return

            await message.channel.send(
                'I saw you mention me! Type `|help` if you really need help!' if config_lang == 'EN'
                else 'เราเห็นแกต้องการความช่วยเหลือนะ พิมพ์ `|help` เพื่อดูคำสั่งทั้งหมด!'
            )

    @commands.command()
    async def faq(self, ctx):
        owner = self.client.get_user(254515724804947969)
        embed = client_events.faq(owner)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Client(client))
