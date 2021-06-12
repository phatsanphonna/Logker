import psutil
import discord
from os import system, listdir
from discord.ext import commands
from datetime import datetime, timedelta


def get_size(b, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor


class Owner(commands.Cog):
    """Only owner can use this list of commands."""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['reload'])
    @commands.is_owner()
    async def _reload(self, ctx):
        """Cogs Reload"""

        system('clear')  # Clear the screen of client CLI

        for f in listdir('cogs'):
            if f.endswith('.py'):
                self.client.unload_extension(f'cogs.{f[:-3]}')
                self.client.load_extension(f'cogs.{f[:-3]}')
                print(f'cogs.{f[:-3]} loaded')

        await ctx.send(embed=discord.Embed(
            description='🔄 Cogs Reload!',
            color=discord.Color.gold()
        ))
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: Cogs: Cogs Reload'
        )

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        print('Client Logout!')
        await ctx.send('Client Logout!')

        await self.client.close()

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def system(self, ctx):
        embed = discord.Embed(
            title='System Info',
            timestamp=datetime.utcnow(),
            color=discord.Colour.gold()
        )

        svmem = psutil.virtual_memory()
        cpufreq = psutil.cpu_freq()
        partitions = psutil.disk_partitions()

        embed.add_field(
            name='CPU', inline=False,
            value=f'Total Cores: `{psutil.cpu_count(logical=False)}/{psutil.cpu_count(logical=True)}`'
                  f'\nFrequency: ```{cpufreq.current:,.2f}Mhz ({psutil.cpu_percent()})%```'

        )
        embed.add_field(
            name='Memory', inline=False,
            value=f'Usage: ```{get_size(svmem.used)}/{get_size(svmem.total)} ({svmem.percent}%)```'
        )
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue

            embed.add_field(
                name=f'Disk', inline=False,
                value=f'\nUsed: ```{get_size(partition_usage.used)}/{get_size(partition_usage.total)} '
                      f'({partition_usage.percent}%)```'
            )
            break

        await ctx.send(embed=embed)

    @commands.command(aliases=['clientinfo', 'cinfo'])
    async def client_info(self, ctx):
        embed = discord.Embed(
            title='Client Info',
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        embed.add_field(name='Total Guilds', value=f'{str(len(self.client.guilds))} guilds')
        embed.add_field(name='Ping', value=f'{round(self.client.latency*1000)} ms')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Owner(client))
