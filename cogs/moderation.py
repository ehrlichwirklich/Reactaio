
import datetime
from asyncio import tasks
import asyncpg

import discord
from asyncpg.connection import Connection
from discord.channel import TextChannel
from discord.embeds import Embed
from discord.errors import Forbidden
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.member import Member
from discord.utils import get


class Moderation(Cog):

    bot: commands.Bot

    connection: Connection

    def __init__(self, bot: Bot):
        self.bot = bot
        self.tempbancheck.start()
        self.tempmutecheck.start()
        
        
    @tasks.loop(seconds = 5.0)
    async def tempbancheck(self):
        async with self.bot.pool.acquire() as self.connection:
            async with self.connection.transaction():
                times = await self.connection.fetch('SELECT End FROM "Temp Bans"')               
                for time in times:
                    if datetime.datetime.strptime(date_string = time, format = '%m/%d/%Y, %H:%M:%S') <= datetime.datetime.utcnow():
                        member: Member = await self.connection.fetchval('SELECT "User Id" FROM "Temp Bans" WHERE End = %1', (time, ))
                        guild: discord.Guild = self.bot.get_guild(id = 812314425318440961)
                        await guild.unban(user = member)
                        await self.connection.execute('DELETE FROM "Temp Bans" WHERE End = %1', (time, ))

    @tasks.loop(seconds = 5.0)
    async def tempmutecheck(self):           
        async with self.bot.pool.acquire() as self.connection:
            async with self.connection.transaction():
                times = await self.connection.fetch('SELECT End FROM "Temp Mutes"')        
                for time in times:
                    if datetime.datetime.strptime(format = '%m/%d/%Y, %H:%M:%S') <= datetime.datetime.utcnow():
                        guild: discord.Guild = self.bot.get_guild(id = 812314425318440961)
                        muted = get(guild.roles, name = 'Muted')
                        member: Member = await self.connection.fetchval('SELECT "Member Id" FROM "Temp Mutes" WHERE End = %1', (time, ))
                        await member.remove_roles(muted)
                        await self.connection.execute('DELETE FROM "Temp Mutes" WHERE End = %1', (time, ))

    
        
                
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx: commands.Context, member: discord.Member , *, reason = None):
        embed = discord.Embed(title = 'Kicked', colour = discord.Colour.from_rgb(0, 255, 127), thumbnail = ctx.guild.banner_url)
        embed.set_author(ctx.author)
        embed.set_thumbnail(ctx.guild.icon)
        embed.description = f'**{member.name}#{member.discriminator} was kicked from {ctx.guild.name}.Reason: {reason}'
        await member.kick(reason = reason)
        await ctx.send(embed)

       
                    
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx: commands.Context, user: discord.User = None , duration = None, *, reason = None):
        if user is None:
            embed: discord.Embed = discord.Embed(title = 'Ban', color = 0x00ffaa, thumbnail = ctx.guild.banner_url)
            embed.description = f'{self.bot.command_prefix}ban [user] <duration> <reason>\n'
            embed.add_field(name = 'Example', value = f'{self.bot.command_prefix}ban 1230231032 10m very cool')
            await ctx.send(embed = embed)
            return
        embed = discord.Embed(title = 'Banned', color = 0x00ffaa, thumbnail = ctx.guild.banner_url)
        try:
            print(int(duration[:-1]))
        except:
            reason = f'{duration} {reason}'
            duration = 0
        if duration is None:
            duration = 0
        if duration == 0:
            val = ''
        else:    
            if duration.endswith('y'):
                hours = int(duration[:-1]) * 365 * 24
                val = f' for {duration[:-1]} years.'
            elif duration.endswith('m'):
                hours = int(duration[:-1]) * 30 * 24
                val = f' for {duration[:-1]} months.'
            elif duration.endswith('d'):
                hours = int(duration[:-1]) * 24
                val = f' for {duration[:-1]} days.'
            elif duration.endswith('h'):
                hours = int(duration[:-1]) 
                val = f' for {duration[:-1]} hours.'
        embed.description = f'**{user.display_name}** was banned from {ctx.guild.name}{val}. Reason: {reason}'
        await ctx.guild.ban(user = user, delete_message_days = 0, reason = reason)
        await ctx.send(embed = embed)
        try:
            await user.send(discord.Embed(title = 'Banned', description = f'You were banned from {ctx.message.guild}{val}. Reason: {reason}. Moderator: {ctx.author}'))
        except Forbidden:
            pass
        if hours:
            now: datetime.datetime = datetime.datetime.utcnow()
            delta: datetime.timedelta = datetime.timedelta(hours = int(hours))
            end = now + delta
            async with self.bot.pool.acquire() as self.connection:
                async with self.connection.transaction():
                    await self.connection.execute('INSERT INTO "Temp Bans" ("User Id", End, Reason) VALUES (%1, %2, %3)', (user.id, end.strftime(format = '%m/%d/%Y, %H:%M:%S'), reason))

    @commands.command(aliases = ['strike'])
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: str):
        warning: discord.Embed = discord.Embed(title = 'Warning', color = 0xff00000, description = f'You\'ve been warned in {ctx.guild}. Reason: {reason}. Moderator: {ctx.author}')
        warning.set_footer(text = member.guild.name)
        await member.send(embed = warning)
        async with self.bot.pool.acquire() as self.connection:
            async with self.connection.transaction():
                await self.connection.execute('INSERT INTO Warnings VALUES ("Member Id", Warned At, Reason) VALUES (%1, %2, %3)', (member.id, datetime.datetime.utcnow().strftime(), reason))

    @commands.command(aliases = ['strikes', 'warns'])
    @commands.has_permissions(kick_members = True)
    async def warnings(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
            self.connection.execute('SELECT COUNT(Id) FROM Warnings')
            count = self.cursor.fetchone()
            if(count == 0):
                await ctx.send(f'User **{member.display_name}** has no warnings.')
            else:
                async with self.bot.pool.acquire() as self.connection:
                    async with self.connection.transaction():
                        await self.connection.fetch('SELECT * FROM Warnings WHERE User == %1', (member, ))
                warns = self.cursor.fetchall()
                warnings: discord.Embed = discord.Embed(title = f'{member}\'s Warnings', color = 0x00ffaa, timestamp = datetime.datetime.utcnow())
                warnings.set_footer(text = ctx.guild.name)
                id: int = 1
                for warn in warns:
                    warnings.add_field(name = f'Warning #{id}: ', value = warn)
                    id += 1   
                await ctx.send(embed = warnings)     


    @commands.command(aliases = ['delwarn', 'delstrike', 'deletestrike', 'deletewarn'])
    @commands.has_permissions(kick_members = True)
    async def deletewarning(self, ctx: commands.Context, id: int):
        try:
            async with self.bot.pool.acquire() as self.connection:
                async with self.connection.transaction():
                    await self.connection.execute('DELETE FROM warns WHERE Id = %1', (id, ))
            await ctx.send("Warning successfully removed.")
        except:
            await ctx.send('Warning not found, please try again with another id.')
    
    @commands.command()
    @commands.has_permissions(manage_channels = True)
    async def lock(self, ctx: Context, channel: TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(channel.guild.default_role, view_channel = True, send_message = False, embed_links = False, add_reactions = False)
        embed: Embed = Embed(title = 'Locked', color = 0x00ffaa, )

    @commands.command(aliases = ['uban', 'rban', 'removeban'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx: Context, member: discord.Member, *, reason: str = None):
        await ctx.guild.unban(discord.Object(id = member.id))
        try:
            async with self.bot.pool.acquire() as self.connection:
                async with self.connection.transaction():
                    await self.cursor.execute('DELETE FROM "Temp Bans" WHERE User = %1', (member.id, ))
        except:
            pass
        await ctx.send(f'**{member.display_name}** was unbanned.')

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mute(self, ctx: commands.Context, member: discord.Member,  duration, *, reason: str = None):
        muted = discord.utils.get(member.guild.roles, name = 'Muted')
        await member.add_roles(muted)
        try:
            print(int(duration[:-1]))
        except:
            reason = f'{duration} {reason}'
            duration = 0
        if duration is None:
            duration = 0
        if duration == 0:
            val = ''
        elif duration.endswith('d'):
            val = f' for {duration[:-1]} days.'
            minutes = duration[:-1] * 24 * 60
        elif duration.endswith('h'):
            val = f' for {duration[:-1]} hours.'
            minutes = duration[:-1] * 60
        elif duration.endswith('m'):
            val = f' for {duration[:-1]} minutes.'
            minutes = duration[:-1]
        elif duration.endswith('y'):
            minutes = duration[:-1] * 365 * 24 * 60
            val = f' for {duration[:-1]} years.'    
        description = f"**{member}** was muted by **{ctx.message.author}**{val}. Reason: {reason}"
        await member.send( embed = discord.Embed(title = 'Muted', author = ctx.message.author, description = f'You were muted in {ctx.message.guild}{val}. Reason: {reason}'))
        embed = discord.Embed(title = "Muted", description = description, color = 0x00ffaa)
        await ctx.send(embed = embed)
        if minutes:
            print('Seems like the duration exists uwu\n')
            now: datetime.datetime = datetime.datetime.utcnow()
            delta: datetime.timedelta = datetime.timedelta(minutes = int(minutes))
            end = now + delta
            async with self.bot.pool.acquire() as self.connection:
                async with self.connection.transaction():
                    await self.connection.execute('INSERT INTO "Temp Mutes" ("Member Id", End, Reason) VALUES(%1, %2, %3)', (member.id, end.strftime('%m/%d/%Y, %H:%M:%S'), reason))
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: discord.Member, *, reason = None):
        role = discord.utils.get(member.guild.roles, name = 'Muted')
        await member.remove_roles(role)
        description = f"**{member}** was umuted by **{ctx.message.author}**. Reason: {reason}"
        embed = discord.Embed(title = "Unmuted", description = description, color = 0x00ffaa)
        await member.send(embed = discord.Embed(title = 'Unmuted', author = ctx.message.author, description = f'You were unmuted in {ctx.message.guild}. Reason: {reason}'))
        await ctx.send(embed = embed)
        try:
            async with self.bot.pool.acquire() as self.connection:
                async with self.connection.transaction():
                    await self.connection.execute('DELETE FROM "Temp Mutes" WHERE "Member Id" = %1', (member.id, ))
        except:
            pass    

    @commands.command()
    async def bans(self, ctx: commands.Context):
        bans = await ctx.guild.bans()
        await ctx.send('Banned users list:\n')
        string: str = ''
        for ban in bans:
           string += f'{ban.user}\n'
        await ctx.send(string)

    @commands.command(aliases = ['clear', 'clean'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, count = 10):
        await ctx.channel.purge(limit = count + 1)


def setup(bot: Bot):
    bot.add_cog(Moderation(bot))
