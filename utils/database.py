import motor.motor_asyncio

db = ''

with open('_token_/mongotoken.txt') as f:
    db = motor.motor_asyncio.AsyncIOMotorClient(f.readline()).LogBot


class Database:
    def __init__(self, guild_id):
        self.guild_id = guild_id
    
    async def info_exists(self):
        data = await db.guild_info.find_one({'guild_id': self.guild_id})
        return True if data is not None else False

    async def prefix_exists(self):
        data = await db.guild_prefix.find_one({'guild_id': self.guild_id})
        return True if data is not None else False

    async def find_info(self):
        return await db.guild_info.find_one({'guild_id': self.guild_id})

    async def find_prefix(self):
        data = await db.guild_prefix.find_one({'guild_id': self.guild_id})
        return data['prefix']

    async def update_prefix(self, prefix):
        await db.guild_prefix.update_one({'guild_id': self.guild_id}, {'$set': {'prefix': prefix}})

    async def update_channel(self, channel_id):
        await db.guild_info.update_one({'guild_id': self.guild_id}, {'$set': {'channel_id': channel_id}})

    async def update_language(self, language):
        await db.guild_info.update_one({'guild_id': self.guild_id}, {'$set': {'logs_language': language}})

    async def insert_prefix(self):
        await db.guild_prefix.insert_one({'guild_id': self.guild_id, 'prefix': '|'})

    async def setup(self, channel_id):
        await db.guild_info.insert_one({'guild_id': self.guild_id, 'channel_id': channel_id, 'logs_language': 'en'})
        return True
