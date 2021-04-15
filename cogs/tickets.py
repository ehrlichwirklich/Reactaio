import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from discord.utils import get


class Tickets(commands.Cog):

    verification_id: discord.Message
    verification_selfie: discord.Message
    verification_video: discord.Message
    transcripts: discord.TextChannel

    tickets = []

    class Ticket:
        channel: discord.TextChannel
        id: int = 0
        user: discord.Member
        name: str
        category: discord.CategoryChannel
        closed: bool = False

        def __init__(self, category: discord.CategoryChannel, user: discord.Member):
            self.category = category
            self.name = self.category + '-' + user.nick + '-' + f'{self.id: dddd}'
            self.id += 1
            self.channel.category = self.category
            self.channel = self.category.create_text_channel(self.name)
            embed: discord.Embed = discord.Embed(title = self.category.name, color = 0x00ff22, description = f'Hello, {user.mention}!\nPlease wait while the associated Staff will see and respond to your ticket.')

            self.transcripts: discord.TextChannel = get(user.guild.channels, name = 'transcripts')

            self.generalticket: discord.CategoryChannel = get(self.channel.guild.categories, id = 824735392267894824)
            self.applyticket: discord.CategoryChannel = get(self.channel.guild.categories, id = 825677447202603068)
            self.verificationticket: discord.CategoryChannel = get(self.channel.guild.categories, id = 824734974191075358)

            owner: discord.Role = get(self.channel.guild.roles, name='Owner')
            headadmin: discord.Role = get(self.channel.guild.roles, name = 'Head Admin')
            admin: discord.Role = get(self.channel.guild.roles, name = 'Admin')
            headmod: discord.Role = get(self.channel.guild.roles, name = 'Head Mod')
            mod: discord.Role = get(self.channel.guild.roles, name = 'Moderator')
            trialmod: discord.Role = get(self.channel.guild.roles, name = 'Trial Mod')

            if category == self.generalticket:
                self.channel.set_permissions([owner, headadmin, admin, headmod, mod, trialmod, user])
            elif category in [self.applyticket, self.verificationticket]:
                self.channel.set_permissions([owner, headadmin, admin, user])
            Tickets.tickets.append(self)

        def close(self):
            owner: discord.Role = get(self.channel.guild.roles, name='Owner')
            headadmin: discord.Role = get(self.channel.guild.roles, name = 'Head Admin')
            admin: discord.Role = get(self.channel.guild.roles, name = 'Admin')
            headmod: discord.Role = get(self.channel.guild.roles, name = 'Head Mod')
            mod: discord.Role = get(self.channel.guild.roles, name = 'Moderator')
            trialmod: discord.Role = get(self.channel.guild.roles, name = 'Trial Mod')

            self.channel.name = f'closed-{self.id:dddd}'
            if self.category == self.generalticket:
                self.channel.set_permissions([owner, headadmin, admin, headmod, mod, trialmod])
            elif self.category in [self.applyticket, self.verificationticket]:
                self.channel.set_permissions([owner, headadmin, admin])
            self.transcripts.send(embed = discord.Embed(title = f'Transcript ticket id: {self.id}: dddd', color = 0xff0000, footer = f'Type: {self.category.name}'), description = self.channel.history(limit = 10000))
            self.closed = True
            Tickets.tickets.remove(self)

        def open(self):
            owner: discord.Role = get(self.channel.guild.roles, name='Owner')
            headadmin: discord.Role = get(self.channel.guild.roles, name = 'Head Admin')
            admin: discord.Role = get(self.channel.guild.roles, name = 'Admin')
            headmod: discord.Role = get(self.channel.guild.roles, name = 'Head Mod')
            mod: discord.Role = get(self.channel.guild.roles, name = 'Moderator')
            trialmod: discord.Role = get(self.channel.guild.roles, name = 'Trial Mod')
            if self.closed == True:
                self.channel.name = self.category + '-' + self.user.nick + '-' + f'{self.id: dddd}'
                if self.category == self.generalticket:
                    self.channel.set_permissions([owner, headadmin, admin, headmod, mod, trialmod, self.user])
                elif self.category in [self.applyticket, self.verificationticket]:
                    self.channel.set_permissions([owner, headadmin, admin, self.user])
                Tickets.tickets.append(self)
            else:
                self.channel.send('Ticket is already open!')

        def delete(self):
            self.channel.delete()

    @commands.has_permissions(administrator = True)
    @commands.command()
    async def setup(self, ctx: Context):
        self.makeaticket: discord.TextChannel = self.bot.get_channel(id = 812678081784315935)
        self.verification: discord.TextChannel = self.bot.get_channel(id = 812677465369214976)

        selfieverification: discord.Embed = discord.Embed(title = 'Selfie Verification', color = 0x00ff22, description = 'Please react to this message with the specified emoji to make a ticket.', footer = self.verification.guild).title
        videoverification: discord.Embed = discord.Embed(title = 'Video Verification', color = 0x00ff22, description = 'Please react to this message with the specified emoji to make a ticket.', footer = self.verification.guild).title
        report: discord.Embed = discord.Embed(title = 'Report a User', color = 0x00ff22, description = 'Please react to this message with the specified emoji to make a ticket.', footer = self.makeaticket.guild).title
        general: discord.Embed = discord.Embed(title = 'General support', color = 0x00ff22, description='Please react to this message with the specified emoji to make a ticket.', footer = self.makeaticket.guild).title
        apply: discord.Embed = discord.Embed(title='Mod/Matchmaker/Bot Technician apply', color = 0x00ff22, description ='Please react to this message with the specified emoji to make a ticket.', footer = self.makeaticket.guild).title
        appeal: discord.Embed = discord.Embed(title = 'Appeal punishment/ban', color = 0x00ff22, description='Please react to this message with the specified emoji to make a ticket.', footer = self.makeaticket.guild).title

        self.selfie: discord.Message = self.verification.send(embed = selfieverification)
        self.video: discord.Message = self.verification.send(embed = videoverification)
        self.report: discord.Message = self.makeaticket.send(embed = report)
        self.support: discord.Message = self.makeaticket.send(embed = general)
        self.apply: discord.Message = self.makeaticket.send(embed = apply)
        self.appeal: discord.Message = self.makeaticket.send(embed = appeal)

        self.selfie.add_reaction('📧')
        self.video.add_reaction('📧')
        self.report.add_reaction('📧')
        self.support.add_reaction('📧')
        self.apply.add_reaction('📧')
        self.appeal.add_reaction('📧')

    def __init__(self, bot: commands.Bot):
        
        self.bot: commands.Bot = bot
        self.makeaticket: discord.TextChannel = self.bot.get_channel(id = 812678081784315935)
        self.verification: discord.TextChannel = self.bot.get_channel(id = 812677465369214976)

        with open('tickets/tickets.data', mode = 'r') as f:
            for line in f:
                self.tickets.append(self.Ticket(line.split(',|')[0], line.split(',|')[1]))

    @commands.command()
    async def close(self, ctx: Context, reason: str = None):
        for ticket in self.tickets:
            if ticket.name == ctx.channel.name:
                ticket.close()
                return

    @commands.command()
    async def open(self, ctx: Context, reason: str = None):
        for ticket in self.tickets:
            if ticket.name == ctx.channel.name:
                ticket.open()
                return

    @commands.command()
    async def claim(self, ctx: Context):
        for ticket in self.tickets:
            if ticket.name == ctx.channel.name:
                ticket.channel.set_permissions([ctx.author, ticket.user])
                return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id in [self.selfie, self.video]:
            ticket: Tickets.Ticket = Tickets.Ticket(self.verification, payload.member)
            self.tickets.append(ticket)
            with open('tickets/tickets.data', mode = 'w') as f:
                for ticket in self.tickets:
                    f.write(f'{ticket.category},|{ticket.user}')
            await self.selfie.remove_reaction('📧', payload.member)
            await self.video.remove_reaction('📧', payload.member)
        elif payload.message_id in [self.apply, self.appeal, self.support, self.report]:
            await self.report.remove_reaction('📧', payload.member)
            await self.appeal.remove_reaction('📧', payload.member)
            await self.apply.remove_reaction('📧', payload.member)
            await self.support.remove_reaction('📧', payload.member)
            ticket: Tickets.Ticket = Tickets.Ticket(self.makeaticket, payload.member)
            self.tickets.append(ticket)
            with open('tickets/tickets.data', mode = 'w') as f:
                for ticket in self.tickets:
                    f.write(f'{ticket.category},|{ticket.user}')

def setup(bot: Bot):
    bot.add_cog(Tickets(bot))
