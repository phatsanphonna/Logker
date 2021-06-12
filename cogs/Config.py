import discord
from discord.ext import commands
from utils.database import Database


def config_info_en(ctx, channel, prefix):
    embed = discord.Embed(
        title=f"Server Config of {ctx.guild.name}",
        color=discord.Colour.orange()
    )
    embed.add_field(name='Language', value='English :flag_gb:')
    embed.add_field(name='Logs Channel', value=channel.mention)
    embed.add_field(name='Prefix', value=prefix)
    return embed


def config_info_th(ctx, channel, prefix):
    embed = discord.Embed(
        title=f"การตั้งค่าของ {ctx.guild.name}",
        color=discord.Colour.orange()
    )
    embed.add_field(name='ภาษา', value='ไทย :flag_th:')
    embed.add_field(name='ห้องเก็บ logs', value=channel.mention)
    embed.add_field(name='Prefix', value=prefix)
    return embed


def missing_perms():
    embed = discord.Embed(
        title='Missing Permissions',
        color=discord.Color.red(),
        description='You are not allowed to use this commands.'
    )
    embed.add_field(
        name='Permission',
        value='```[✘] View Audit Log```'
    )
    return embed


def setup_not_found():
    embed = discord.Embed(
        color=discord.Color.red(),
        description=(
            'Please setup Logker before use config commands!\n'
            '\nโปรดทำการตั้งค่าครั้งแรกให้กับ Logker ก่อนถึงจะสามารถใช้งานตั้งค่าได้!'
        )
    )
    return embed


def use_in_guild():
    f = discord.File('assets/hyewon_confused.gif')
    embed = discord.Embed(
        color=discord.Color.gold(),
        description='Please use this command in server text channels.'
    )

    return embed, f


class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['settings', 'setting'], invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(view_audit_log=True)
    async def config(self, ctx):
        # Seek info, config and logs channel of guild
        info = await Database.find_info(ctx.guild.id)
        guild_prefix = await Database.find_prefix(ctx.guild.id)

        if info is None:
            await ctx.send(embed=setup_not_found())
            return

        channel = self.client.get_guild(info[0]).get_channel(info[1])
        config_lang = 'en' if info is None else info[2]

        embed = config_info_en(ctx, channel, guild_prefix) if config_lang == 'en'\
            else config_info_th(ctx, channel, guild_prefix)

        await ctx.send(embed=embed)

    @config.group(aliases=['lang'])
    @commands.guild_only()
    @commands.has_guild_permissions(view_audit_log=True)
    async def language(self, ctx):
        info = await Database.find_info(ctx.guild.id)

        if info is None:
            await ctx.send(embed=setup_not_found())
            return

        new_lang = 'en' if info[2] == 'th' else 'th'
        await Database.update_language(ctx.guild.id, new_lang)

        await ctx.send(
            f'**Updated**: Logker language changed from'
            f'**Thai** :flag_th: to **English** :flag_gb:.' if new_lang == 'en'
            else f'**อัพเดท**: ภาษาของ Logker ได้เปลี่ยนจาก **อังกฤษ** :flag_gb: เป็น **ไทย** :flag_th: แล้ว'
        )

    @config.group(aliases=['lc', 'logs', 'logschannel', 'logchannel'])
    @commands.guild_only()
    @commands.has_guild_permissions(view_audit_log=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        info = await Database.find_info(ctx.guild.id)
        old_channel = self.client.get_guild(info[0]).get_channel(info[1])

        if info is None:
            await ctx.send(embed=setup_not_found())
            return

        await Database.update_channel(ctx.guild.id, channel.id)

        await channel.send(
            f'**Updated**: Logker changed logs channel from {old_channel.mention} to {channel.mention}.'
            if info[2] == 'en'
            else f'**อัพเดท**: Logker ได้เปลี่ยนช่องเก็บ logs จาก {channel.mention} ไปที่ '
                 f'{old_channel.mention} เรียบร้อยแล้ว'
        )

    @config.group(aliases=['changePrefix', 'changeprefix', 'prefix'])
    @commands.guild_only()
    @commands.has_guild_permissions(view_audit_log=True)
    async def change_prefix(self, ctx, new_prefix: str):
        prefix = await Database.find_prefix(ctx.guild.id)
        info = await Database.find_info(ctx.guild.id)

        if info is None:
            await ctx.send(embed=setup_not_found())
            return

        await Database.update_prefix(ctx.guild.id, new_prefix)

        await ctx.send(
            f'Prefix changed from {prefix} to {new_prefix}' if info[2] == 'en'
            else f'ได้ทำการเปลี่ยนเครื่องหมายนำหน้าจาก {prefix} เป็น {new_prefix} เรียบร้อยแล้ว'
        )

    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=missing_perms())
        elif isinstance(error, commands.NoPrivateMessage):
            embed, file = use_in_guild()

            await ctx.send(embed=embed)
            await ctx.send(file=file)
        else:
            raise error

    @language.error
    async def language_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=missing_perms())
        elif isinstance(error, commands.NoPrivateMessage):
            embed, file = use_in_guild()

            await ctx.send(embed=embed)
            await ctx.send(file=file)
        else:
            raise error

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=missing_perms())
        elif isinstance(error, commands.NoPrivateMessage):
            embed, file = use_in_guild()

            await ctx.send(embed=embed)
            await ctx.send(file=file)
        else:
            raise error

    @change_prefix.error
    async def change_prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=missing_perms())
        elif isinstance(error, commands.NoPrivateMessage):
            embed, file = use_in_guild()

            await ctx.send(embed=embed)
            await ctx.send(file=file)
        else:
            raise error


def setup(client):
    client.add_cog(Config(client))
