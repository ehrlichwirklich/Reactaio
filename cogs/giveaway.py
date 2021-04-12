import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context


class Giveaway(Cog):

    def __init__(self, client: Bot):
        self.client: Bot = client

    @commands.command(aliases = ['gstart'])
    @commands.has_role('Owner')
    async def giveawaystart(self, ctx: Context, time: str, *, prize: str):
        seconds: int = 0
        if time.endswith('y'):
            seconds = int(time[:-1]) * 365 * 24 * 60 * 60
        elif time.endswith('d'):
            seconds = int(time[:-1]) * 24 * 60 * 60
        elif time.endswith('h'):
            seconds = int(time[:-1]) * 60 * 60
        elif time.endswith('m'):
            seconds = int(time[:-1]) * 60
        elif time.endswith('s'):
            seconds = int(time[:-1])
        embed: discord.Embed = discord.Embed(title = f'{prize} giveaway', color = 0x00ffdd, timestamp = True)
        embed.add_field(name = 'Starts in:',value = datetime.datetime.now(), inline = False)
        embed.add_field(name = 'Ends in:', value = datetime.datetime.now() + datetime.timedelta(seconds = seconds), inline = False)
        embed.footer = 'React with the 🎉 emoji to access the giveaway.'
        message = await ctx.send(embed = embed)

        message.add_reaction('🎉')

        await asyncio.sleep(delay = seconds)

        newmsg: discord.Member = await ctx.channel.fetch_message(message.id)

        users = newmsg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        users.pop(ctx.author)

        winner: discord.Member = random.choice(users)

        win: discord.Embed = discord.Embed(title = 'Winner', color = 0xff0000, timestamp = True)
        win.footer = 'Best of wishes to them. DM Arshia Aghaei#0617 to claim their prize!'
        win.description = f'Congratulations, {winner.mention}! You have won {prize}!'
        win.author = 'Giveaway bot'

        await ctx.send(embed = win)


def setup(client: Bot):
    client.add_cog(Giveaway(client))
