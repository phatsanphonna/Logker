import discord
from discord.ext import commands
from utils.database import Database


def help_en():
    embed = discord.Embed(
        title='Lists of Logker Commands!',
        color=discord.Color.gold(),
        description='List of Commands. Full version [here](https://github.com/ssuniie/Logker/tree/main/docs/en)'
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
        name='config',
        inline=False,
        value=(
            'Show config of your server\n'
            '**Usage**: `|config`\n'
            '**Aliases**: settings'
        )
    )
    embed.add_field(
        name='config language',
        inline=False,
        value=(
            'Switch language between Thai and English\n'
            '**Usage**: `|config language`\n'
            '**Aliases**: lang'
        )
    )
    embed.add_field(
        name='config channel',
        inline=False,
        value=(
            'Change channel that logs store in\n'
            '**Usage**: `|config lc <channel>`\n'
            '**Aliases**: logs, lc, logschannel'
        )
    )
    embed.add_field(
        name='config changePrefix',
        inline=False,
        value=(
            'Change prefix of Logker (default is |)\n'
            '**Usage**: `|config changePrefix <prefix>`\n'
            '**Aliases**: prefix, changeprefix'
        )
    )
    return embed


def help_th():
    embed = discord.Embed(
        title='คำสั่งทั้งหมดของ Logker',
        color=discord.Color.gold(),
        description='คำสั่งทั้งหมดแบบเต็มๆ [ที่นี่](https://github.com/ssuniie/Logker/tree/main/docs/th)'
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
        name='config',
        inline=False,
        value=(
            'แสดงการตั้งค่าของเซิฟเวอร์\n'
            '**การใช้งาน**: `|config`\n'
            '**คำเหมือน**: settings'
        )
    )
    embed.add_field(
        name='config language',
        inline=False,
        value=(
            'เปลี่ยนแปลงการตั้งค่าระหว่าง ภาษาไทย กับ ภาษาอังกฤษ\n'
            '**การใช้งาน**: `|config language`\n'
            '**คำเหมือน**: lang'
        )
    )
    embed.add_field(
        name='config channel\n',
        inline=False,
        value=(
            'เปลี่ยนช่องในการเก็บ log\n'
            '**การใช้งาน**: `|config channel <channel>`\n'
            '**คำเหมือน**: logs, lc, logschannel'
        )
    )
    embed.add_field(
        name='config changePrefix',
        inline=False,
        value=(
            'เปลี่ยนคำนำหน้าของ Logker (ค่าเริ่มต้นคือ |)\n'
            '**การใช้งาน**: `|config changePrefix <prefix>`\n'
            '**คำเหมือน**: prefix, changeprefix'
        )
    )
    return embed


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        if ctx.guild is None:
            config_lang = 'en'
        else:
            db = Database(ctx.guild.id)  # Create a new instance

            info = await db.find_info()

            # Seek config of guild
            config_lang = 'en' if info is None else info['logs_language']

        # Set language version of embed message
        embed = help_en() if config_lang == 'en' else help_th()

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
