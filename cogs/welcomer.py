import discord
from discord import user
from discord.ext import commands


class Welcomer(commands.Cog):
    welcomer: discord.Embed

    def __ordinal__(self, number: int):
        if number % 10 == 1:
            return 'st'
        elif number % 10 == 2:
            return 'nd'
        elif number % 10 == 3:
            return 'rd'
        else:
            return 'th'

    def __nonbots__(self, guild: discord.Guild):
        return sum(not member.bot for member in guild.members)

    def __init__(self, bot: commands.Bot):
        server = 812314425318440961
        self.bot: commands.Bot = bot
        

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcomer = discord.Embed(color = 0x00ff33)
        welcomer.set_footer(text = 'We hope you enjoy your stay here!')
        welcomer.set_thumbnail(url = member.guild.icon_url)
        welcomer.set_image(url = member.guild.banner_url)
        nonbots = self.__nonbots__(member.guild)
        count = str(nonbots) + self.__ordinal__(nonbots)
        welcome: discord.TextChannel = member.guild.channels.get_channel(812314425318440965)
        welcomer.title = f'Welcome, {member.display_name}!'
        welcomer.description = f'Welcome to {member.guild.name}! You\'re our {count} member.'
        welcomer.author = member.avatar + f'{member.name}#{member.discriminator}'
        welcome.send(embed = self.welcomer)


def setup(client: commands.Bot):
    client.add_cog(Welcomer(client))



