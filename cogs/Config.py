import discord
from discord.ext import commands
from events.find_info import find_guild_info

import project_token
db = project_token.cluster.LogBot.guild_info


def config_info_en(ctx, channel):
    embed = discord.Embed(
        title=f"Config of {ctx.guild.name}",
        color=discord.Colour.orange()
    )
    embed.add_field(name='Language', value='English :flag_gb:')
    embed.add_field(
        name='Logs Channel',
        value=channel.mention
    )
    return embed


def config_info_th(ctx, channel):
    embed = discord.Embed(
        title=f"การตั้งค่าของ {ctx.guild.name}",
        color=discord.Colour.orange()
    )
    embed.add_field(name='ภาษา', value='ไทย :flag_th:')
    embed.add_field(
        name='ห้องเก็บ logs',
        value=channel.mention
    )
    return embed


class _Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases=['settings', 'setting'], invoke_without_command=True)
    @commands.has_guild_permissions(view_audit_log=True)
    async def config(self, ctx):
        # Seek info, config and logs channel of guild
        info = await find_guild_info(ctx.guild.id)
        channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])

        config_lang = 'EN' if info is None else info['logs_language']

        embed = config_info_en(ctx, channel) if config_lang == 'EN' else config_info_th(ctx, channel)

        await ctx.send(embed=embed)

    @config.error
    async def config_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                'Please setup Logker before use config commands!\n'
                f'**Log Error** > `{error}`'
            )

    @config.group(aliases=['lang'])
    @commands.has_guild_permissions(view_audit_log=True)
    async def language(self, ctx):
        info = await find_guild_info(ctx.guild.id)

        if info is not None:
            old_lang = info['logs_language']
            new_lang = None

            if old_lang == 'TH':
                new_lang = 'EN'
            elif old_lang == 'EN':
                new_lang = 'TH'

            old_update = {
                'guild_id': info['guild_id'],
                'channel_id': info['channel_id'],
                'logs_language': old_lang
            }
            new_update = {
                'guild_id': info['guild_id'],
                'channel_id': info['channel_id'],
                'logs_language': new_lang
            }

            db.replace_one(old_update, new_update)
            await ctx.send(
                f'**Updated**: Logker language changed from'
                f'**Thai** :flag_th: to **English** :flag_gb:.' if new_lang == 'EN'
                else f'**อัพเดท**: ภาษาของ Logker ได้เปลี่ยนจาก **อังกฤษ** :flag_gb: เป็น **ไทย** :flag_th: แล้ว'
            )

    @language.error
    async def language_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                'Please setup Logker before use config commands!\n'
                f'**Log Error** > ``{error}`'
            )

    @config.group(aliases=['lc', 'log', 'logschannel', 'logchannel'])
    @commands.has_guild_permissions(view_audit_log=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        info = await find_guild_info(ctx.guild.id)
        old_channel = self.client.get_guild(info['guild_id']).get_channel(info['channel_id'])

        if info is not None:
            old_update = {
                'guild_id': info['guild_id'],
                'channel_id': old_channel.id,
                'logs_language': info['logs_language']
            }
            new_update = {
                'guild_id': info['guild_id'],
                'channel_id': channel.id,
                'logs_language': info['logs_language']
            }
            db.replace_one(old_update, new_update)

            await channel.send(f'**Updated**: Logker changed logs channel from {old_channel.mention} to {channel.mention}.')

    @channel.error
    async def channel_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send(
                'Please setup Logker before use config commands!\n'
                f'**Log Error** > `{error}`'
            )


def setup(client):
    client.add_cog(_Config(client))
