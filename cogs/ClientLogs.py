from discord.ext import commands
from datetime import datetime, timedelta


class ClientLogs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: ClientReady: Client is online.'
        )

    @commands.Cog.listener()
    async def on_disconnect(self):
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: ClientDisconnected: Client disconnected.'
        )

    @commands.Cog.listener()
    async def on_resumed(self):
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: ClientResume: Client resumed connection.'
        )

    @commands.Cog.listener()
    async def on_error(self, event):
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: {event}'
        )

    @commands.Cog.listener()
    async def on_command_error(self, _, error):
        await self.client.get_channel(846230758996967454).send(
            f'{(datetime.now() + timedelta(hours=7)).strftime("%B %d, %Y @%H:%M:%S")}\n'
            f':regional_indicator_x: {type(error).__name__}: {error}'
        )

        # Ignore some errors
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, commands.NoPrivateMessage):
            pass
        else:
            raise error


def setup(client):
    client.add_cog(ClientLogs(client))
