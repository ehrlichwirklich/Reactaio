import json
import os
import typing
from typing import List

import discord
from discord.ext import commands

embeds = []

class Embed(commands.Cog):

    client: commands.Bot

    def __init__(self, client: commands.Bot):
        self.client = client
        for fileName in os.listdir('embeds'):
            if fileName.endswith('.json') and os.path.isfile(fileName):
                with open(fileName, mode = 'r') as f:
                    data = json.load(f)
                    embeds.append(discord.Embed.from_dict(data))


    def elements(self, k: int, n: int, a: list):
        element = ''
        for i in range(k, n):
            element = element + a[i] + ' '
        return element
    
    @commands.command()
    async def embed(self, ctx: commands.Context, command: str, *args):
        if command in ['create', 'c']:
            self.name = args[0]
            embeds.append([self.name, discord.Embed()])
            with open(f'/embeds/{self.name}.json', mode = 'w') as f:
                json.dump(embeds[-1].to_dict(), f)
        elif command in ['update', 'u', 'edit', 'e']:
            self.name = args[0]
            prop = args[1]
            if prop == 'title':
                self.title = self.elements(2, args.__len__(), args)
                for embed in embeds:
                    if embeds[0] == self.name:
                        embeds[1].title = self.title
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop == 'description':
                self.description = self.elements(2, args.__len__(), args)
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].description = self.description
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop == 'author':
                self.author = args[2]
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].author = self.author
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop == 'image':
                self.image = args[2]
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].image = self.image
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop == 'thumbnail':
                self.thumbnail = args[2]
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].thumbnail = self.thumbnail
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop in ['color', 'colour']:
                self.color = args[2]
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].color = self.color
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
            elif prop == 'footer':
                self.footer = self.elements(2, args.__len__(), args)
                for embed in embeds:
                    if embed[0] == self.name:
                        embed[1].footer = self.footer
                        with open(f'embeds/{self.name}.json', mode = 'w') as f:
                            json.dump(embed[1].to_dict(), f)
                        return
        elif command in ['remove', 'r', 'delete', 'd']:
            for embed in embeds:
                i = embeds.index([self.name, embed[1]])
                if(embed[0] == self.name):
                    embeds[i][0] = None
                    embeds[i][1] = None
                    if(os.path.exists(f'embeds/{embed[0]}.json')):
                        os.remove(f'embeds/{embed[0]}.json')
                    return
        elif command in ['setchannel', 'setch']:
            self.channel = ctx.author.guild.get_channel(args[2].id)
            self.name = args[1]
            for embed in embeds:
                if embed[0] == self.name:
                    self.client.get_channel(self.channel.id).message.send(embed[1])
                    return
            
def setup(client):
    client.add_cog(Embed(client))
