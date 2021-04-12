import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context, Cog

class Emoji(Cog):

    def __init__(self, client: Bot):
        self.client: Bot = client

    @commands.has_permissions(manage_emojis = True)
    @commands.command(aliases = ['steal', 'addemote', 'add'])
    async def addemoji(self, ctx: Context, emoji: discord.Emoji, *, name: str):
        ctx.guild.create_custom_emoji(name, str(emoji.url))
        await ctx.send(f'Added emoji {str(emoji)} with the name {name}')

    @commands.has_permissions(manage_emojis = True)
    @commands.command(aliases = ['delete', 'del', 'delemote'])
    async def deleteemoji(self, ctx: Context, emoji: discord.Emoji):
        await ctx.send(f'Successfully deleted the custom emoji {str(emoji)}.')
        emoji.delete()


def setup(client: Bot):
    client.add_cog(Emoji(client))

