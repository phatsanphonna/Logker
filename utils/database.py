import aiosqlite


class Database:
    @staticmethod
    async def find_info(guild_id):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        cursor = await db.execute(f'SELECT * FROM guild_info WHERE guild_id={guild_id}')
        row = await cursor.fetchone()
        # print(guild_id, row)
        return row

    @staticmethod
    async def find_prefix(guild_id):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        cursor = await db.execute(f'SELECT prefix FROM guild_prefix WHERE guild_id={guild_id}')
        row = await cursor.fetchone()
        # print(row)
        return row[0] if row is not None else row

    @staticmethod
    async def update_language(guild_id, new_lang):
        db = await aiosqlite.connect('db.db', check_same_thread=False)

        await db.execute(
            f'UPDATE guild_info SET logs_language="{new_lang}" WHERE guild_id={guild_id}')
        await db.commit()
        await db.close()

    @staticmethod
    async def update_channel(guild_id, channel_id):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        await db.execute(
            f'UPDATE guild_info SET channel_id={channel_id} WHERE guild_id={guild_id}')
        await db.commit()
        await db.close()

    @staticmethod
    async def update_prefix(guild_id, prefix):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        await db.execute(
            f'UPDATE guild_prefix SET prefix="{prefix}" WHERE guild_id={guild_id}')
        await db.commit()
        await db.close()

    @staticmethod
    async def insert_prefix(guild_id):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        await db.execute(
            f'INSERT INTO guild_prefix VALUES(guild_id={guild_id}, prefix="|")')
        await db.commit()
        await db.close()

    @staticmethod
    async def setup(guild_id, channel_id):
        db = await aiosqlite.connect('db.db', check_same_thread=False)
        await db.execute(
            f'INSERT INTO guild_info VALUES(guild_id={guild_id}, channel_id="{channel_id}, logs_language="en")')
        await db.commit()
        await db.close()

        return True
