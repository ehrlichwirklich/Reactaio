import os
import random

import discord
from discord.ext import commands
from discord.flags import Intents

TOKEN = os.getenv('DISCORD_TOKEN')

bot_prefix = '.'

intent: discord.Intents = discord.Intents.all()
intent.members = True
intent.bans = True
intent.dm_messages = True
intent.guilds = True
intent.reactions = True
client = commands.Bot(command_prefix = bot_prefix, intents = intent)


def ordinal(number: int):
    if number % 10 == 1:
        return 'st'
    if number % 10 == 2:
        return 'nd'
    if number % 10 == 3:
        return 'rd'
    return 'th'

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(f'{bot_prefix}help.'))
    print(f' {client.user} has connected.')


@client.event
async def on_member_join(member):
    print(f'Welcome, {member}')

@client.event
async def on_member_remove(member):
    print(f'Goodbye, {member}')


@client.command()
@commands.has_permissions(mention_everyone = True)
async def revive(ctx):
    await ctx.send(f'{ctx.author} has used revive command!')
    await ctx.send('@Chat revive')

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don’t count on it.',
    'It is certain.',
    'It is decidedly so.',
    'Most likely.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Outlook good.',
    'Reply hazy, try again.',
    'Signs point to yes.',
    'Very doubtful.',
    'Without a doubt.',
    'Yes.',
    'Yes – definitely.',
    'You may rely on it.'
    ]
    await ctx.send(f'Question: {question}\n Answer: {random.choice(responses)}')

@client.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for fileName in os.listdir('./cogs'):
    if fileName.endswith('.py'):
        client.load_extension(f'cogs.{fileName[:-3]}')
    
client.run(TOKEN)
