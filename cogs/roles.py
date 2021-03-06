import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog


class Roles(Cog):
    
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: Bot = bot
    
    @commands.command()
    async def role(self, ctx: commands.Context, val, key: str, *args):
        if(isinstance(val, discord.Role)):
            for member in ctx.guild.members:
                if val in member.roles:
                    for role in args:
                        if key in ['add', '+']:
                            await member.add_roles(role)
                        elif key in ['remove', 'rem', '-']:
                            await member.remove_roles(role)
        elif isinstance(val, discord.Member):
            for role in args:
                if key in ['add', '+']:
                    await val.add_roles(role)
                elif key in ['remove', 'rem', '-']:
                    await val.remove_roles(role)
    
    @commands.command()
    async def roles(self, ctx: commands.Context, member: discord.Member):
        description: str = ''
        if member is None:
            member = ctx.author
        embed: discord.Embed = discord.Embed(title = f'{member}\'s roles', color = 0x00ff00)
        embed.footer = ctx.guild.name
        for role in member.roles:
            description += role + '\n'
        embed.description = description
    

def setup(bot: Bot):
    bot.add_cog(Roles(bot))

        
    
