import asyncio
import datetime
import os
from operator import index
from sys import prefix

import discord
from discord import reaction
from discord.colour import Color
from discord.ext import commands, tasks


class Moderation(commands.Cog):

    client: commands.Bot

    def __init__(self, client: commands.Bot):
        self.client = client
        fname: str
        for fname in os.listdir('warns'):
            if os.path.isfile(fname) and fname.endswith('.data'):
                with open(fname, mode = 'r') as f:
                    line: str
                    for line in f:
                        member, reason = line.split(': ')
                        self.warns.append(self.Warn(member, reason))
                    

    class Warn:
        member: discord.Member
        __count__: int = 0
        reasons = []
        time = []

        def __init__(self, member: discord.Member, reason: str):
            self.member = member
            self.__count__ = 1
            self.reasons.append(reason)
            self.time.append(datetime.datetime.now())
        
        def addwarn(self, reason: str):
            self.__count__ += 1
            self.reasons.append(reason)
            self.time.append(datetime.datetime.now())
        
        def removewarn(self, id: int):
            self.__count__ -= 1
            del self.time[id]
            del self.reasons[id]
    
    warns = []
                

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx: commands.Context, member: discord.Member , *, reason = 'No reason provided.'):
        embed = discord.Embed(title = 'Kicked', colour = discord.Colour.from_rgb(0, 255, 127), thumbnail = ctx.guild.banner_url)
        embed.set_author(ctx.author)
        embed.set_thumbnail()
        embed.description = f'**{member.name}#{member.discriminator} was kicked from {ctx.guild.name}.Reason: {reason}'
        await member.kick(reason = reason)
        await ctx.send(embed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx: commands.Context, member: discord.Member , duration = 0, *, reason = None):
        if ctx is None:
            embed: discord.Embed = discord.Embed(title = 'Ban', color = 0x00ffaa, thumbnail = ctx.guild.banner_url)
            embed.description = f'{self.client.get_prefix()}ban [member] <duration> <reason>\n'
            embed.add_field(name = 'Example', value = f'{self.client.get_prefix()}ban 1230231032 10m very cool')
        embed = discord.Embed(title = 'Banned', color = 0x00ffaa, thumbnail = ctx.guild.banner_url)
        embed.set_author(name = member.display_name)
        if(duration == 0):
            val = ''
        else:
            if duration.endswith('y'):
                seconds = duration[:-1] * 365 * 24 * 60 * 60
                val = f' for {duration[:-1]} years.'
            elif duration.endswith('m'):
                seconds = duration[:-1] * 30 * 24 * 60 * 60
                val = f' for {duration[:-1]} months.'
            elif duration.endswith('d'):
                seconds = duration[:-1] * 24 * 60 * 60
                val = f' for {duration[:-1]} days.'
            elif duration.endswith('h'):
               seconds = duration[:-1]  * 60 * 60
               val = f' for {duration[:-1]} hours.'
        embed.description = f'**{member.name}#{member.discriminator} was banned from {ctx.guild.name}{val}.Reason: {reason}'
        await member.ban(reason = reason, delete_message_days = 0)
        await member.send(discord.Embed(title = 'Banned', author = ctx.message.author, description = f'You were banned from {ctx.message.guild}{val}. Reason: {reason}. Moderator: {ctx.author}'))
        await ctx.send(embed = embed)
        if('seconds' in locals):
            await asyncio.sleep(delay = seconds)
            await member.unban(ctx.message.server)

    @commands.command(aliases = ['strike'])
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx: commands.Context, member: discord.Member, reason: str):
        for warn in self.warns:
            if member == warn.member:
                warn.addwarn(reason)
                await member.send(f'You\'ve been warned in {ctx.guild}. Reason: {reason}. Moderator: {ctx.author}')
                with open(f'warns/{member.id}.data', mode = 'w') as f:
                    for reason in warn.reasons:
                        f.write(f'{warn.reasons.index(reason)}: {reason}\n')
                return
        warn = self.Warn(member, reason)
        await member.send(f'You\'ve been warned in {ctx.guild}. Reason: {reason}. Moderator: {ctx.author}')
        with open(f'warns/{member.id}.data', mode = 'w') as f:
            for reason in warn.reasons:
                f.write(f'{warn.reasons.index(reason)}: {reason}\n')
        
    @commands.command(aliases = ['strikes', 'warns'])
    @commands.has_permissions(kick_members = True)
    async def warnings(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        for warn in self.warnings:
            if warn.member == member:
                embed: discord.Embed = discord.Embed(title = f'{member.id}\'s wrnings: ', color = 0x00ffdd, timestamp = True)
                embed.author = ctx.author
                reason: str
                for index in range(warn.reasons.len()):
                    embed.add_field(name = f'Warn #{index}: ', value = f'Reason: {warn.reasons[index]} at {warn.time[index]}', inline = False)
                await ctx.send(embed = embed)
                return
        await ctx.send(f'User **{member.display_name}** has no warnings.')


    @commands.command(aliases = ['delwarn', 'delstrike', 'deletestrike', 'deletewarn'])
    @commands.has_permissions(kick_members = True)
    async def deletewarning(self, ctx: commands.Context, member: discord.Member, id: int):
        for warn in self.warnings:
            if warn.member == member:
                warn.removewarn(id)
                await ctx.send(f'Warning #{id} from user {member.display_name} has been removed successfully.')
                return
        await ctx.send('warning not found, please try again with a different id or member.')



    @commands.command(aliases = ['uban', 'rban', 'removeban'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member):
        bans =  await ctx.guild.bans()
        name, descriminator = member.split('#')
        for entry in bans:
            user = entry.user
            if(user.name, user.descriminator) == (name, descriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'**{name}#{descriminator}** was unbanned.')
                return

    @commands.command()
    @commands.has_permissions(mute_members = True)
    async def mute(self, ctx, member, *, duration = 0, reason = None):
        muted = discord.utils.get(member.server.roles, name='Muted', timestamp = True)
        await ctx.add_roles(member, muted)
        if duration == 0:
            val = ''
        elif duration.endswith('d'):
            val = f' for {duration[:-1]} days.'
            seconds = duration[:-1] * 24 * 60 * 60
        elif duration.endswith('h'):
            val = f' for {duration[:-1]} hours.'
            seconds = duration[:-1] * 60 * 60
        elif duration.endswith('m'):
            val = f' for {duration[:-1]} minutes.'
            seconds = duration[:-1] * 60
        elif duration.endswith('y'):
            seconds = duration[:-1] * 365 * 24 * 60 * 60
            val = f' for {duration[:-1]} years.'    
        description = f"**{member}** was muted by **{ctx.message.author}**{val}.Reason: {reason}"
        await member.send(discord.Embed(title = 'Banned', author = ctx.message.author, description = f'You were muted in {ctx.message.guild}{val}. Reason: {reason}'))
        embed = discord.Embed(title = "Muted", description = description, color = 0x00ffaa)
        await ctx.send(embed = embed)
        if 'seconds' in locals:
            asyncio.sleep(delay = seconds)
            await ctx.remove_roles(member, muted)
    
    @commands.command()
    @commands.has_permissions(mute_members = True)
    async def unmute(self, ctx, member, reason = 'No reason provided.'):
        role = discord.utils.get(member.server.roles, name = 'Muted', timestamp = True)
        await ctx.remove_roles(member, role)
        description = f"**{member}** was umuted by **{ctx.message.author}**.Reason: {reason}"
        embed = discord.Embed(title = "Unmuted", description = description, color = 0x00ffaa)
        await member.send(discord.Embed(title = 'Unmuted', author = ctx.message.author, description = f'You were unmuted in {ctx.message.guild}. Reason: {reason}'))
        await ctx.send(embed = embed)    

    @commands.command()
    async def bans(self, ctx):
        bans = await ctx.guild.bans()
        print('Banned users list:\n')
        for ban in bans:
            print (f'{bans.user}\n')

    @commands.command(aliases = ['clear', 'clean'])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, count = 10):
        await ctx.channel.purge(limit = count + 1)

        

def setup(client):
    client.add_cog(Moderation(client))
