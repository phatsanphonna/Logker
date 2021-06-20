import discord
from discord.ext import commands
from utils.database import Database
from messages import client_events_msg


class Client(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        uptime_channel = self.client.get_channel(833140105820242020)
        embed = client_events_msg.uptime_restart()

        await uptime_channel.send(embed=embed)
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.listening,
                                      name=f'|help'))
        # await self.client.change_presence(
        #     status=discord.Status.online,
        #     activity=discord.Activity(type=discord.ActivityType.listening,
        #                               name=f'Fixing the bugs!'))
        print('Client is online!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main_server = self.client.get_channel(833224379562590218)

        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                owner = self.client.get_user(254515724804947969)
                await channel.send(embed=client_events_msg.guild_join(owner))
            break

        await main_server.send(f'Logker got into {guild.name}!')

    @commands.Cog.listener('on_message')
    async def member_mention_client(self, message: discord.Message):
        # Prevent client responds to itself
        if message.author is self.client.user:
            return

        if message.author.bot:
            return

        if self.client.user.mentioned_in(message):
            db = Database(message.guild.id)  # Create a new instance

            if not await db.info_exists():  # Check if that server has Logker setup?
                config_lang = 'en'
            else:
                info = await db.find_info()
                config_lang = info[2]

            prefix = await db.find_prefix()

            if '@here' in message.content:
                return
            if '@everyone' in message.content:
                return

            await message.channel.send(
                f'I saw you mention me! Type `{prefix}help` if you really need help!' if config_lang == 'en'
                else f'เราเห็นแกต้องการความช่วยเหลือนะ พิมพ์ `{prefix}help` เพื่อดูคำสั่งทั้งหมด!'
            )


def setup(client):
    client.add_cog(Client(client))
