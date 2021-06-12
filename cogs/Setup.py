import discord
from discord.ext import commands
from utils.database import Database


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


def missing_channel():
    embed = discord.Embed(
        title='Missing Channel',
        color=discord.Color.red(),
        description='You have to specific text channel to setup.'
    )

    return embed


class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(view_audit_log=True)
    async def setup(self, ctx, channel: discord.TextChannel):
        info = await Database.find_info(ctx.guild.id)

        if info is None:
            logs_setup = await Database.setup(ctx.guild.id, channel.id)

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
                await (ctx if channel is None else channel).send(
                    file=discord.File('assets/yujin_wonyoung_thumbs_up.gif'))

                main_server = self.client.get_channel(833224379562590218)
                await main_server.send(f'Logker has setup in {ctx.guild.name}!')

                await msg.add_reaction('✅')
        else:
            lang = 'en' if info is None else info[2]
            embed = already_setup_en(ctx) if lang == 'en' else already_setup_th(ctx)

            await ctx.send(embed=embed)

    @setup.error
    async def setup_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=missing_perms())
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=missing_channel())


def setup(client):
    client.add_cog(Setup(client))
