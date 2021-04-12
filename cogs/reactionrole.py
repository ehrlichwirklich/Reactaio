import discord
from discord.ext import commands
from discord.ext.commands import Context
import enum

from enum import IntEnum

class ReactionRoles(commands.Cog):

    client: commands.Bot

    reaction_roles = []

    class ReactionRole():

        class ReactionType(IntEnum):
            GIVE = 1,
            TAKE = 2,
            GIVEONLY = 3,
            TAKEONLY = 4,
            GIVEANDTAKE = 5,

        channel: discord.Guild
        message: discord.Message
        unique: bool
        type: ReactionType
        emoji: discord.Emoji
        role: discord.Role
        role2: discord.Role

        

        def __init__(self, channel: discord.TextChannel, message: discord.Message, unique:bool, type: ReactionType, emoji: discord.Emoji, role: discord.Role, role2: discord.Role = None):
            self.channel = channel
            self.message = message
            self.unique = unique
            self.type = type
            self.emoji = emoji
            self.role = role
            self.role2 = role2

    def __init__(self, client):
        self.client = client
        with open('rr data/reactroles.data', mode = 'r') as f:
            for line in f:
                data = line.split(',|')
                self.reaction_roles.append(data[0])
                self.reaction_roles.append(data[1])
                self.reaction_roles.append(data[2])
                self.reaction_roles.append(data[3])
                self.reaction_roles.append(data[4])
                self.reaction_roles.append(data[5] if len(data) == 6 else None)


    @commands.command(aliases = ['rr', 'reactrole'])
    async def reactionrole(self, ctx: Context, command: str , unique: bool = False, channel: discord.TextChannel = None, message: discord.Message = None, type: ReactionRole.ReactionType = None, emoji: discord.Emoji = None, role: discord.Role = None, role2: discord.Role = None):
        if command in ['create', 'c', 'make', 'm']:
            if channel is None:
                channel = ctx.channel
            if message != None and type != None and emoji != None and role != None:
                self.reaction_roles.append(self.ReactionRole(channel = channel, message = message, unique = unique, type = type, emoji = str(emoji), role = role, role2 = role2))
                await self.client.add_reaction(channel.fetch_message(message.id), emoji = str(emoji))
                ctx.send(embed = discord.Embed(title = 'Success!', description = f'Successfully ctreated reaction {str(emoji)} with the role(s): {role.mention}{role2.mention}.', color = 0x00ffaa, footer = {ctx.guild}))
                with open('rr data/reactroles.data', mode = 'x') as f:
                    f.write(f'{channel},|{message},|{unique},|{type},|{str(emoji)},|{role}{f",|{role2}" if role2 != None else ""}')
            elif message is None:
                await ctx.send('Message id cannot be empty.')
            elif type is None:
                await ctx.send('Please specify the reaction type.')
            elif emoji is None:
                await ctx.send('Please specify the reaction emoji.')
            else:
                await ctx.send('Please specify the role you plan to assign/take.')
        elif command in ['remove', 'r', 'delete', 'd']:
            if channel is None:
                channel = ctx.channel
            if message != None:
                for reactions in self.reaction_roles:
                    if reactions.message == message:
                        self.reaction_roles.remove(reactions)
                        with open('rr data/reactroles.data', mode = 'r') as f:
                            data = []
                            for line in f:
                                if line.split(',|')[1] == message:
                                    line = ''
                                    break
                                data.append(line)
                        with open('rr data/reactroles.data', mode = 'w') as f:
                            for d in data:
                                f.write(f'{d}\n')
            else:
                ctx.send('Please specify the message id.')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        for reaction in self.reaction_roles:
            if reaction.message == payload.message_id and str(reaction.emoji) == str(payload.emoji):
                if reaction.unique == False:
                    if reaction.type in [
                        ReactionRoles.ReactionRole.ReactionType.GIVE,
                        ReactionRoles.ReactionRole.ReactionType.GIVEONLY,
                    ]:
                        await payload.member.add_roles(reaction.role)
                    elif reaction.type == ReactionRoles.ReactionRole.ReactionType.TAKE:
                        await payload.member.remove_roles(reaction.role2)
                    elif reaction.type == ReactionRoles.ReactionRole.ReactionType.GIVEANDTAKE:
                        await payload.member.add_roles(reaction.role)
                        await payload.member.remove_roles(reaction.role2)
                else:
                    for reaction in self.reaction_roles:
                        if reaction.user.id == payload.message.author.id:
                            self.reaction_roles.remove(reaction)
                            await payload.member.remove_roles(reaction.role)
                            break
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        for reaction in self.reaction_roles:
            if reaction.message == payload.message_id and str(reaction.emoji) == str(payload.emoji):
                if reaction.type in [
                    ReactionRoles.ReactionRole.ReactionType.TAKE,
                    ReactionRoles.ReactionRole.ReactionType.TAKEONLY,
                ]:
                    await payload.member.add_roles(reaction.role)
                elif reaction.type == ReactionRoles.ReactionRole.ReactionType.GIVE:
                    await payload.member.remove_roles(reaction.role2)
                elif reaction.type == ReactionRoles.ReactionRole.ReactionType.GIVEANDTAKE:
                    await payload.member.add_roles(reaction.role2)
                    await payload.member.remove_roles(reaction.role)
                return
def setup(client: commands.Bot):
    client.add_cog(ReactionRoles(client))