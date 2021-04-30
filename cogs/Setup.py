import discord
from discord.ext import commands
from events.find_info import find_guild_info

import project_token
db = project_token.cluster.LogBot.guild_info


async def first_setup(guild_id, channel_id, logs_lang='EN'):
    info = {
        'guild_id': guild_id,
        'channel_id': channel_id,
        'logs_language': logs_lang
    }

    await db.insert_one(info)

    return True


def already_setup_en(ctx):
    embed = discord.Embed(
        title='Logker already setup!',
        color=discord.Colour.red(),
        description=(
            f'{ctx.guild.name} have done first setup already!\n'
            'If you want to change settings, '
            + 'Please type `|config` or `|help` in chat!'
        )
    )
    return embed


def already_setup_th(ctx):
    embed = discord.Embed(
        title='Logker ได้ตั้งค่าไปแล้ว',
        color=discord.Colour.red(),
        description=(
            f'{ctx.guild.name} ได้ทำการตั้งค่าครั้งแรกไปแล้ว\n'
            + 'ถ้าอยากเปลี่ยนแปลงการตั้งค่า '
            + 'ให้พิมพ์ `|config` หรือ `|help` ลงในห้องพูดคุย'
        )
    )
    return embed


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(view_audit_log=True)
    async def setup(self, ctx, channel: discord.TextChannel = None):
        info = await find_guild_info(ctx.guild.id)

        if info is None:
            logs_setup = await first_setup(ctx.guild.id, ctx.guild.id if channel is None else channel.id)
            
            if logs_setup:
                embed = discord.Embed(
                    title='Logker first setup successfully!',
                    color=discord.Colour.green()
                )
                embed.add_field(name='Default Language', value='English')
                embed.add_field(
                    name='Logs Channel',
                    value=(ctx.channel if channel is None else channel).mention
                )

                msg = await (ctx if channel is None else channel).send(embed=embed)
                # await msg.add_reaction('<:white_check_mark:212e30e47232be03033a87dc58edaa95>')
        else:
            lang = 'EN' if info is None else info['logs_language']
            embed = already_setup_en(ctx) if lang == 'EN' else already_setup_th(ctx)
            
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Setup(client))
