import discord
from discord import client
from discord.ext import commands


class Info(commands.Cog):

    afks = []
    client: commands.Bot


    class AFK:
        member: discord.Member
        reason: str

        def __init__(self, member: discord.Member, reason: str):
            self.member = member
            self.reason = reason

    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client
        with open('afks/afks.data', mode = 'r') as f:
            for line in f:
                self.afks.append(self.AFK(line.split(',|')[0], line.split(',|')[1]))
    
    @commands.command(aliases = ['test'])
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! {self.client.latency * 1000}ms')

    @commands.command()
    async def humans(self, ctx: commands.Context):
        members = ctx.guild.members
        count = sum(not member.bot for member in members)
        await ctx.send(f'{ctx.guild.name} has {count} non-bot members.')

    @commands.command()
    async def bots(self, ctx: commands.Context):
        members = ctx.guild.members
        count = sum(1 for member in members if member.bot)
        await ctx.send(f'{ctx.guild.name} has {count} bots.')
    
    @commands.command(aliases = ['info', 'memberinfo', 'lookup', 'search'])
    async def whois(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        info: discord.Embed = discord.Embed(title = f'{member.display_name}\'s info', color = 0x0000ff)
        general: discord.TextChannel = member.guild.get_channel(812314425318440969)
        acknowledgements: str
        if member.guild.owner == member :
            acknowledgements = 'Server Owner'
        elif member.guild_permissions.administrator == True:
            acknowledgements = 'Server Administrator'
        elif member.guild_permissions.manage_guild == True:
            acknowledgements = 'Server Manager'
        elif member.guild_permissions.ban_members == True or member.guild_permissions.kick_members == True:
            acknowledgements = 'Server Moderator'
        else:
            acknowledgements = 'Server Member'
        info.author = f'{member.name}#{member.discriminator}'
        info.add_field('Nickname:', member.display_name, False)
        info.add_field('Joined at:', member.joined_at, False)
        info.add_field('Created at:', member.created_at, False)
        info.add_field('Roles:', member.roles, False)
        info.add_field('Premium Since:', member.premium_since, False)
        info.add_field('Permissions:', member.permissions_in(general), False)
        info.add_field('Acknowledgements:', acknowledgements, False)
        info.thumbnail = member.avatar
        await ctx.send(embed = info)

    @commands.command()
    async def afk(self, ctx: commands.Context, *, reason: str = None):
        nick = ctx.author.nick
        ctx.author.nick = '[AFK]' + ctx.author.nick
        embed: discord.Embed = discord.Embed(title = 'AFK', color = 0x00ff00, timestamp = True)
        embed.author = ctx.author
        embed.description = f'Successfully set your AFK status, {ctx.author}! Reason: {reason}'
        embed.footer = f'This status will be gone on next message from {ctx.author}'
        await ctx.send(embed)
        self.afks.append(ctx.author)
        with open('afks/afks.data', mode = 'w') as f:
            for afk in self.afks:
                f.write(f'{afk.member},|{afk.reason}\n')

    @commands.Cog.listener()
    async def on_message(self, ctx: commands.Context):
        for afk in self.afks:
            if ctx.author == afk.member:
                await ctx.send(f'{ctx.author.mention}, welcome back! I\'ve removed your AFK status.')
                self.afks.remove(afk)
                with open('afks/afks.data', mode = 'w') as f:
                    for afk in self.afks:
                        f.write(f'{afk.member},|{afk.reason}\n')
            if afk.member.mention in ctx.message:
                await ctx.send(f'**{afk.member.name}#{afk.member.discriminator}** is AFK, reason: {afk.reason}')

def setup(client: commands.Bot):
    client.add_cog(Info(client))




