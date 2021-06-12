import discord
from discord.ext import commands

from utils.database import Database
from messages import member_events_msg


class Member(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if info[0] == member.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                member_events_msg.member_join_en(member) if config_lang == 'en'
                else member_events_msg.member_join_th(member)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if info[0] == member.guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                member_events_msg.member_remove_en(member) if config_lang == 'en'
                else member_events_msg.member_remove_th(member)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        info = await Database.find_info(guild.id)

        if info is None:
            return

        if info[0] == guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                member_events_msg.member_ban_en(guild, user) if config_lang == 'en'
                else member_events_msg.member_ban_th(guild, user)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        info = await Database.find_info(guild.id)

        if info is None:
            return

        if info[0] == guild.id:
            # Seek Logs Channel of guild
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            # Set language version of embed message
            embed = (
                member_events_msg.member_unban_en(guild, user) if config_lang == 'en'
                else member_events_msg.member_unban_th(guild, user)
            )

            await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_member_update')
    async def member_name_update(self, before: discord.Member, after: discord.member):
        if before.activity != after.activity:
            return
        if before.status != after.status:
            return

        info = await Database.find_info(before.guild.id)

        if info is None:
            return

        if info[0] == before.guild.id:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.display_name != after.display_name:
                # Set language version of embed message
                embed = (
                    member_events_msg.member_name_update_en(before, after) if config_lang == 'en'
                    else member_events_msg.member_name_update_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_member_update')
    async def member_role_update(self, before: discord.Member, after: discord.member):
        if before.activity != after.activity:
            return
        if before.status != after.status:
            return

        info = await Database.find_info(before.guild.id)

        if info is None:
            return

        if info[0] == after.guild.id:
            guild_log = self.client.get_guild(info[0])
            logs_channel = guild_log.get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.roles != after.roles:
                for guild in after.guild.roles:
                    if guild not in guild_log.roles:
                        return

                # Set language version of embed message
                embed = (
                    member_events_msg.member_role_update_en(before, after) if config_lang == 'EN'
                    else member_events_msg.member_role_update_th(before, after)
                )

                await logs_channel.send(embed=embed)

    @commands.Cog.listener('on_voice_state_update')
    async def member_voice_chat_join(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.self_mute != after.self_mute:
            return
        if before.self_deaf != after.self_deaf:
            return

        if before.channel != after.channel:
            if before.channel is None and after.channel is not None:
                pass
            else:
                return

        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if member.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.channel is not after.channel:
                channel = self.client.get_channel(after.channel.id)
                embed = None

                if isinstance(channel, discord.VoiceChannel):
                    embed = (
                        member_events_msg.member_join_voice_chat_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_join_voice_chat_th(member, channel)
                    )
                elif isinstance(channel, discord.StageChannel):
                    embed = (
                        member_events_msg.member_join_stage_chat_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_join_stage_chat_th(member, channel)
                    )

                await logs_channel.send(embed=embed)
                return

    @commands.Cog.listener('on_voice_state_update')
    async def member_voice_chat_leave(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.self_mute != after.self_mute:
            return
        if before.self_deaf != after.self_deaf:
            return

        if before.channel != after.channel:
            if before.channel is not None and after.channel is None:
                pass
            else:
                return

        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if member.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.channel != after.channel:
                channel = self.client.get_channel(before.channel.id)
                embed = None

                if isinstance(channel, discord.VoiceChannel):
                    embed = (
                        member_events_msg.member_leave_voice_chat_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_leave_voice_chat_th(member, channel)
                    )
                elif isinstance(channel, discord.StageChannel):
                    embed = (
                        member_events_msg.member_leave_stage_chat_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_leave_stage_chat_th(member, channel)
                    )

                await logs_channel.send(embed=embed)
                return

    @commands.Cog.listener('on_voice_state_update')
    async def member_voice_chat_change(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.self_mute != after.self_mute:
            return
        if before.self_deaf != after.self_deaf:
            return

        if before.channel != after.channel:
            if before.channel is not None and after.channel is not None:
                pass
            else:
                return

        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if member.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'en' if info is None else info[2]

            if before.channel != after.channel:
                before = self.client.get_channel(before.channel.id)
                after = self.client.get_channel(after.channel.id)

                embed = (
                    member_events_msg.member_change_voice_chat_en(member, before, after) if config_lang == 'en'
                    else member_events_msg.member_change_voice_chat_th(member, before, after)
                )

                await logs_channel.send(embed=embed)
                return

    @commands.Cog.listener('on_voice_state_update')
    async def member_guild_voice_status_update(
            self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.self_mute != after.self_mute:
            return
        if before.self_deaf != after.self_deaf:
            return
        if before.mute == after.mute:
            if before.deaf == after.deaf:
                return
            else:
                pass

        info = await Database.find_info(member.guild.id)

        if info is None:
            return

        if member.guild.id == info[0]:
            logs_channel = self.client.get_guild(info[0]).get_channel(info[1])
            config_lang = 'EN' if info is None else info[2]

            channel = self.client.get_channel(after.channel.id)

            if before.deaf is after.deaf:
                if after.mute is False:
                    embed = (
                        member_events_msg.member_guild_voice_unmute_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_guild_voice_unmute_th(member, channel)
                    )

                    await logs_channel.send(embed=embed)
                    return

                elif after.mute is True:
                    embed = (
                        member_events_msg.member_guild_voice_mute_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_guild_voice_mute_th(member, channel)
                    )

                    await logs_channel.send(embed=embed)
                    return

            if before.deaf is not after.deaf:
                if after.deaf is False:
                    embed = (
                        member_events_msg.member_guild_voice_undeaf_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_guild_voice_undeaf_th(member, channel)
                    )

                    await logs_channel.send(embed=embed)
                    return

                elif after.deaf is True:
                    embed = (
                        member_events_msg.member_guild_voice_deaf_en(member, channel) if config_lang == 'en'
                        else member_events_msg.member_guild_voice_deaf_th(member, channel)
                    )

                    await logs_channel.send(embed=embed)
                    return


def setup(client):
    client.add_cog(Member(client))
