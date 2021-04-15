import operator

import discord
from discord import client
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from discord.ext.commands.cog import Cog

#text channels
staff_room = 812369644152422440
staff_activity = 827300967573356554
staff_issues = 824070693712560158
council_meeting = 825640284473262080
introductions = 812913559847305267
events = 816870454778134539
general = 812314425318440969
verified_lounge = 813108084330987520
vent = 812488484617977886
vent_no_response = 828875733580382238
ask_to_dm = 812948187588460564
rp = 826852369178296351
suggestions = 828848514054094888
female_only = 822614108100362271
bois = 827107245468680194
bot_request = 812467901390127146
complaints = 826887289233342464
confessions_reactions = 813004709458870292
selfies = 812495695494774814
selfies_reactions = 822234403652501604
media = 812487796102135818
media_reactions = 823192462767816724
writings = 826416489003352085
art_room = 812477606968033320
nsfw = 812497772069912588
horny_jail = 821872432028844103
nsfw_male = 814634822110674985
nsfw_female = 812498125322584095
verified_vc = 827214077046292531
gean_simps = 826816336465494046
nev_moonbeams = 823939808120274944
panther_inspiration = 827095861044576266
arshia_idea_dump = 827161540918640670
vc_text = 812986121461825556

text_channels = [staff_room, staff_activity, staff_issues, council_meeting, introductions, events, general, verified_lounge, vent, vent_no_response, ask_to_dm, rp, suggestions, female_only, bois, bot_request, complaints, confessions_reactions, selfies, selfies_reactions, media, media_reactions, writings, art_room, nsfw, horny_jail, nsfw_male, nsfw_female, verified_vc, gean_simps, nev_moonbeams, panther_inspiration, arshia_idea_dump, vc_text]


text_levels = []
voice_levels = []

#voice channels
council_meeting_voice = 820514912744898591
join_to_create = 823993497278349372
lounge_voice = 812506797092896829
verified_voice = 813108490654580756
public_i = 826848694540042301
public_ii = 827881646392213514
public_iii = 827881692685271060
private_i = 826848752891461733
private_ii = 826848849720508446
private_iii = 828852588283559946
music_i = 827221843617251338
music_ii = 827221921799864411
music_iii = 827221970625101914
stream_1 = 816870513660919838
stream_2 = 816870573116227584
among_us = 816870764770230283
cah = 828853568026574849
jack_box = 816870693588435034
scribblo = 816870764770230283
movie_night = 816870944740081694
karakoe = 816871092735442965
show = 828707826896863243
voice_1v1 = 828707922623070228
waiting = 828707985886543922

level_up = 812549913820790784

voice_channels = [council_meeting_voice, join_to_create, lounge_voice, verified_voice, public_i, public_ii, public_iii, private_i, private_ii, private_iii, music_i, music_ii, music_iii, stream_1, stream_2, among_us, cah, scribblo, jack_box, movie_night, karakoe, show, voice_1v1, waiting]

class Levels(Cog):

    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Leveling system active!\n')
        with open('xps/xps.data', mode = 'r') as f:
            for line in f:
                id = line.split(',')[0]
                xp = line.split(',')[1]
                self.text_levels.append([id, xp])
        with open('xps/vxps.data', mode = 'r') as f:
            for line in f:
                id = line.split(',')[0]
                xp = line.split(',')[1]
                self.voice_levles.append([id, xp])

    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.guild.id not in text_channels:
            return

        member: discord.Member
        for member, xp in self.text_levels:
            if self.member == message.author:
                mindex = self.text_levels.index(self.member)
                self.text_levels[mindex][1] = self.text_levels[mindex][1] + 10
                with open('xps/xps.data', mode = 'a') as f:
                    for line in f:
                        if line.split(',')[0] == self.member.id:
                            oldlevel: int = xp / 1000
                            level: int = (xp + 10) / 1000
                            if level != oldlevel:
                                message.guild.get_channel(level_up).send(f'Congrats, **{message.author}** has leveled up to level {level}!')
                            line = f'{self.member.id},{xp + 10},{level}'
                            break
                return
        with open('/xps/xps.data', mode = 'a') as f:
            f.write(f'{self.member.id},10,0')

    @tasks.loop(seconds = 1)
    async def countdown(self, message: discord.Message):
        for member, xp in self.voice_levels:
            if member == message.author:
                mindex = self.voice_levels.index(member)
                self.text_levels[mindex][1] = self.voice_levels[mindex][1] + 10
                with open('xps/vxps.data', mode = 'a') as f:
                    for line in f:
                        if line.split(',')[0] == member.id:
                            oldlevel: int = xp / 1000
                            level: int = (xp + 10) / 1000
                            if level != oldlevel:
                                message.guild.get_channel(level_up).send(
                                    f'Congrats, **{message.author}** has voice leveled up to level {level}!')
                            break
                return
        with open('xps/xps.data', mode='a') as f:
            f.write(f'{self.member.id},10,0')

    @Cog.listener()
    async def on_voice_state_update(self, before, after):
        if before.voice is None and after.voice is None:
            self.countdown.start()
        else:
            self.countdown.stop()

    @commands.command()
    async def rank(self, ctx: Context):
        text_levels = sorted(self.text_levels, key = operator.itemgetter(1), reverse = True)
        voice_levels = sorted(voice_levels, key = operator.itemgetter(1), reverse = True)
        embed = discord.Embed(title = 'Rank', color = 0x00ffaa)
        embed.footer = ctx.guild.name
        embed.add_field( name = 'Text Level', value = text_levels[text_levels.index(ctx.member.id)][1], inline = False)
        embed.add_field(name = 'Voice level: ', value = voice_levels[voice_levels[voice_levels.index(ctx.member.id)][1]], inline = False)
        await self.level_up.send(embed)

    @commands.command(aliases = ['leaderboard', 'lead'])
    async def top(self, ctx: Context):
        text_levels = sorted(self.text_levels, key = operator.itemgetter(1), reverse = True)
        voice_levels = sorted(voice_levels, key = operator.itemgetter(1), reverse = True)
        embed = discord.Embed(title = 'Text Leaderboard', color = 0x00ffaa)
        id = 1
        for level in text_levels:
            uid, xp = level.split(',')
            embed.add_field(name = f'#{id}:)', value = f'{ctx.guild.fetch_member()}, {xp} xp, level: {xp / 100}')
            id += 1
        embd = discord.Embed(title = 'Voice leaderboard: ', color = 0x00ffaa)
        id = 1
        for voice in voice_levels:
            uid, xp = voice.split(',')
            embd.add_field(name = f'#{id}:)', value = f'{ctx.author}, {xp} xp, level: {xp / 100}')

def setup(bot: Bot):
    bot.add_cog(Levels(bot))
