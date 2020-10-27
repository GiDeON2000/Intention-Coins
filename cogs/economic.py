from discord.utils import get
from discord.ext import commands
from discord.ext.commands import errors
from discord import errors as dpy_errors
from Utils import database
from Utils import func
from discord import Embed
import pymongo
import discord
import config
import os
import json
import aiohttp
import random



class Eco(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='coinflip',
        brief='Подбросить монетку',
        usage='coinflip <орёл или решка, о или р>',
        description='Подбросить монетку, игра с ботом'
    )
    async def _coinflip(self, ctx, arg):
        coinfl = ''
        if arg != 'решка' or arg != 'орёл':
            emb = discord.Embed(color=config.COLORS["ERROR"], description=f"Правильное использование команды `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`")
            await ctx.send(embed=emb)
        else:
            num = random.randint(1, 2)
            if num == 1:
                coinfl = 'решка'
            elif num == 2:
                coinfl = 'орёл'
            
            if arg == coinfl:
                emb = discord.Embed(color=config.COLORS["BASE"],
                description=f'У тебя {arg}, и выпал тоже {arg}.\nПоздравляю! Ты победил!')
            elif arg != coinfl:
                emb = discord.Embed(color=config.COLORS["BASE"],
                description=f'У тебя {arg},но мне выпал {coinfl}.\n К сожалению ты проиграл(')
            await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Eco(client))