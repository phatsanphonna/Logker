import discord
from discord.ext import commands
from datetime import datetime
from events.find_info import find_guild_info


def userinfo_en(ctx, member):
    embed = discord.Embed(
        title='Person Inspector',
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='Display Name', value=member.display_name)
    embed.add_field(name='Joined at (DD/MM/YYYY)', inline=False,
                    value=member.joined_at.strftime("%d/%m/%Y"))
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    return embed


def userinfo_th(ctx, member):
    embed = discord.Embed(
        title='Person Inspector',
        color=discord.Color.gold(),
        timestamp=datetime.utcnow()
    )
    embed.add_field(name='ชื่อที่แสดง', value=member.display_name)
    embed.add_field(name='วันที่เข้าร่วม (DD/MM/YYYY)', inline=False,
                    value=(member.joined_at.replace(
                        year=member.joined_at.year + 543)).strftime("%d/%m/%Y"))
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)

    return embed


class MemberInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(view_audit_log=True)
    async def userinfo(self, ctx, member: discord.Member):
        info = await find_guild_info(ctx.guild.id)
        config_lang = 'EN' if info is None else info['logs_language']

        embed = (
            userinfo_en(ctx, member) if config_lang == 'EN'
            else userinfo_th(ctx, member)
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MemberInfo(client))
