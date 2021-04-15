import os
import random
from asyncio.events import get_event_loop

import discord
from asyncpg.pool import Pool, create_pool
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.utils import get

TOKEN = os.getenv('DISCORD_TOKEN')

bot_prefix = '.'

intent: discord.Intents = discord.Intents.all()
intent.members = True
intent.bans = True
intent.dm_messages = True
intent.guilds = True
intent.reactions = True
bot: Bot = Bot(command_prefix = bot_prefix, intents = intent)

bot.POSTGRES_INFO = {
    'user': 'postgres',
    'password': 'root',
   'database': 'Reactaio',
    'host':'localhost'
}



def ordinal(number: int):
    if number % 10 == 1:
        return 'st'
    if number % 10 == 2:
        return 'nd'
    if number % 10 == 3:
        return 'rd'
    return 'th'

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.online, activity = discord.Game(f'{bot_prefix}help.'))
    print(f' {bot.user} has connected.')


@bot.event
async def on_member_join(member):
    print(f'Welcome, {member}')

@bot.event
async def on_member_remove(member):
    print(f'Goodbye, {member}')

@bot.command()
@commands.has_permissions(mention_everyone = True)
async def revive(ctx: commands.Context):
    await ctx.send(f'**{ctx.author}** has used revive command!')
    revive: discord.Role = get(ctx.guild.roles, id = 813018522082607125)
    await ctx.send(f'{revive.mention} Get active!')

@bot.command(aliases = ['8ball'])
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

@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.has_permissions(administrator = True)
async def unload(ctx: Context, extension):
    bot.unload_extension(f'cogs.{extension}')

for fileName in os.listdir('./cogs'):
    if fileName.endswith('.py'):        
        bot.load_extension(f'cogs.{fileName[:-3]}')

loop = get_event_loop()
bot.pool = loop.run_until_complete(create_pool(**bot.POSTGRES_INFO))

bot.run(TOKEN)
