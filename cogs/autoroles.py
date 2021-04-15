import discord
from discord import client
from discord.client import Client
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog
from discord.utils import get


class AutoRoles(commands.Cog):
    
    bot: Bot

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: discord.Member):
        verification = get(member.guild.roles, name = '-----------------Verification-----------------')
        age = get(member.guild.roles, name = '-----------------Age-----------------')
        gender = get(member.guild.roles, name = '-----------------Gender-----------------')
        sexuality = get(member.guild.roles, name = '-----------------Sexuality-----------------')
        preferences = get(member.guild.roles, name = '-----------------Preferences-----------------')
        mbti = get(member.guild.roles, name = '-----------------MBTI-----------------')
        ethnicity = get(member.guild.roles, name = '-----------------Ethnicity-----------------')
        zodiac = get(member.guild.roles, name = '-----------------Zodiac Sign-----------------')
        hobbies = get(member.guild.roles, name = '-----------------Hobbies-----------------')
        relationship = get(member.guild.roles, name = '-----------------Relationship-----------------')
        location = get(member.guild.roles, name = '-----------------Location-----------------')
        looking = get(member.guild.roles, name = '-----------------Looking for-----------------')
        dm = get(member.guild.roles, name = '-----------------DM status-----------------')
        pings = get(member.guild.roles, name = '-----------------Pings-----------------')
        games = get(member.guild.roles, name = '-----------------Games-----------------')
        homie = get(member.guild.roles, name = 'Homie')
        newbie = get(member.guild.roles, name = 'Newbie')
        with open(f'members/{member.id}.data', mode = 'w') as f:
            for line in f:
                role = get(member.guild.roles, id = line)
                Client.add_roles(member, role)
        if homie not in member.guild.roles:
            await client.add_roles(member, newbie)
            await client.add_roles(member, verification, age, gender, sexuality, preferences, mbti, ethnicity, zodiac, hobbies, relationship, location, looking, dm, pings, games)
        else:
            await client.add_roles(member, verification, age, gender, sexuality, preferences, mbti, ethnicity, zodiac, hobbies, relationship, location, looking, dm, pings, games, newbie)

    @Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        with open(f'members/{after.id}.data', mode = 'w') as f:
            for role in after.roles:
                f.write(f'{role.id}\n')



def setup(bot: Bot):
    bot.add_cog(AutoRoles(bot))
