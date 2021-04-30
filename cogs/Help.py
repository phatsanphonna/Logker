import discord
from discord.ext import commands
from events.find_info import find_guild_info


def help_en():
    embed = discord.Embed(
        title='Lists of Logker Commands!',
        color=discord.Color.gold()
    )
    embed.add_field(
        name='help',
        inline=False,
        value=(
            'Show lists of command!\n'
            '**Usage**: `|help`'
        )
    )
    embed.add_field(
        name='info',
        inline=False,
        value=(
            'Show information about bot\n'
            '**Usage**: `|info`'
        )
    )
    embed.add_field(
        name='config/setting',
        inline=False,
        value=(
            'Show config of your server\n'
            '**Usage**: `|config` or `|setting`'
        )
    )
    embed.add_field(
        name='config language/lang',
        inline=False,
        value=(
            'Switch language between Thai and English\n'
            '**Usage**: `|config language` or `|config lang`'
        )
    )
    embed.add_field(
        name='config channel/logschannel\n',
        inline=False,
        value=(
            'Change channel that logs store in\n'
            '**Usage**: `|config channel {channel}` or `|config logschannel {channel}`'
        )
    )
    return embed


def help_th():
    embed = discord.Embed(
        title='คำสั่งทั้งหมดของ Logker',
        color=discord.Color.gold()
    )
    embed.add_field(
        name='help',
        inline=False,
        value=(
            'แสดงคำสั่งทั้งหมด!\n'
             + '**Usage**: `|help`'
        )
    )
    embed.add_field(
        name='info',
        inline=False,
        value=(
            'แสดงรายละเอียดเกี่ยวกับบอท\n'
            + '**Usage**: `|info`'
        )
    )
    embed.add_field(
        name='config/setting',
        inline=False,
        value=(
            'แสดงการตั้งค่าของเซิฟเวอร์\n'
            + '**การใช้งาน**: `|config` or `|setting`'
        )
    )
    embed.add_field(
        name='config language/lang',
        inline=False,
        value=(
            'เปลี่ยนแปลงการตั้งค่าระหว่าง ภาษาไทย กับ ภาษาอังกฤษ\n'
            + '**การใช้**: `|config language` or `|config lang`'
        )
    )
    embed.add_field(
        name='config channel/logschannel\n',
        inline=False,
        value=(
            'เปลี่ยนช่องในการเก็บ log\n'
            + '**การใช้งาน**: `|config channel {channel}` or `|config logschannel {channel}`'
        )
    )
    return embed


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(view_audit_log=True)
    async def help(self, ctx):
        info = await find_guild_info(ctx.guild.id)

        if ctx.guild.id == info['guild_id']:
            # Seek config of guild
            config_lang = 'EN' if info is None else info['logs_language']

            # Set language version of embed message
            embed = help_en() if config_lang == 'EN' else help_th()

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
