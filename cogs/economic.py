from discord.utils import get
from discord.ext import commands
from discord.ext.commands import errors
from discord import errors as dpy_errors
from Utils import database
from Utils import func
from Utils import database as DB
import pymongo
import discord
import config
import os
import json
import aiohttp
import random

# $coinflip - кинуть монетку (шанс 50 на 50)

# $slot - крутить барабан казино (шанс 50 на 50, в случае победы x3 от суммы)

# $add-money - выдать деньги пользователю [для админов]

# $remove-money - снять деньги пользователю [для админов] , как определённую сумму, так и все

# $balance ($bal)

# $money - посмотреть деньги чужого пользователя (в том числе и банк)

# $deposit ($dep) [all/amount] - положить деньги в банк

# $withdraw снять деньги с банка

# $crime - ограбить (шанс на ограбление 40%, на проигрыш 60%)

# $slut(вызвать шлюху) - шанс на (получение бабок 30%, на снятие 70%)

# $give-money - передать другому игроку бабло , как определённую сумму, так и все

# report - жалоба на другого пользователя по шаблону: report [участник] [причина]

# $shop - магазин

# // так же команды для добавление предмета в магазин, его редактирования (названия, добавление роли за предмет в магазине, установку суммы за предмет в магазине, а так же приминения команды после покупки предмета в магазине. То есть если человек купит снятие варна, то последует команда от бота Juniper -снятьпред

# $leaderboard - доска лидеров по деньгам на руках, деньгам в банке

# $set-currency <symbol> - установить символ валюты (НЕ МЕНЯТЬ!)
# $set-start-balance <amount> - установать начальный баланс
# $money-audit-log <enable | disable> [channel] - канал денежного журнала аудита для просмотра транзакций
# $add-money [cash | bank] <member> <amount> - добавить коинов участнику
# $add-money-role [cash | bank] <role> <amount> - добавить коинов всем участникам с определённой ролью
# $remove-money [cash | bank] <member> <amount> - снять коины участнику
# $remove-money-role [cash | bank] <role> <amount> - снять коины всем участникам с определённой ролью
# $economy-stats - экономическая статистика 
# вот пример команд которые могли бы находиться в боте
# Так же команды для установки стартового баланса, для установки эмодзи валюты, и установки самого префикса команд



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
        if arg == 'решка' or arg == 'орёл' or arg == 'орел':
            num = random.randint(1, 2)
            if num == 1:
                coinfl = 'решка'
            elif num == 2:
                coinfl = 'орёл'
            
            
            if arg == coinfl:
                emb = discord.Embed(color=config.COLORS["BASE"],
                description=f'У тебя `{arg}`, и выпал тоже `{arg}`.\nПоздравляю! Ты победил!')
            elif arg != coinfl:
                emb = discord.Embed(color=config.COLORS["BASE"],
                description=f'У тебя `{arg}`,но мне выпал `{coinfl}`.\n К сожалению ты проиграл(')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(color=config.COLORS["ERROR"], description=f"Правильное использование команды `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`")
            await ctx.send(embed=emb)

    @commands.command(
        name='add-money',
        brief='Выдаёт деньги',
        usage='add-money <участник> <кол-во денег>',
        description='Команда для админов, выдаёт определённое кол-во денег пользователю'
    )
    @commands.has_permissions(administrator=True)
    async def _add_money(self, ctx, member: discord.Member, how_many):
        if int(how_many) >= 0:
            DB.Set().add_rem_money(ctx=ctx, member=member, how_many=how_many, type='add')
            emb = discord.Embed(title='Успех!', color=config.COLORS["BASE"],
                                description=f'Пользователю - {member.mention}, было успешно выдано `{how_many}` монет!')
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title='Ошибка!', color=config.COLORS["ERROR"],
                                description='Укажите положительно кол-во денег!')
            await ctx.send(embed=emb)

    @commands.command(
        name='remove-money',
        brief='Снимает деньги',
        usage='remove-money <участник> <кол-во денег(либо, all)>',
        description='Команда для админов, отнимает определённое кол-во денег у пользователя'
    )
    @commands.has_permissions(administrator=True)
    async def _remove_money(self, ctx, member: discord.Member, how_many):
        if how_many == 'all':
            DB.Set().add_rem_money(ctx=ctx, member=member, how_many=DB.Get().money(ctx=ctx, member=member), type='remove')
            emb = discord.Embed(title='Успех!', color=config.COLORS["BASE"],
                                description=f'У пользователя - {member.mention}, было успешно сняты все деньги!')
            await ctx.send(embed=emb)

        elif int(how_many) >= 0:
            if int(how_many) > DB.Get().money(ctx=ctx, member=member):
                emb = discord.Embed(title='Ошибка!', color=config.COLORS["ERROR"],
                                    description=f'У пользователя - {member.mention} всего `{DB.Get().money(ctx=ctx, member=member)}` монет, а вы пытаетесь у него снять целых `{how_many}`')
                await ctx.send(embed=emb)
            else:
                DB.Set().add_rem_money(ctx=ctx, member=member, how_many=how_many, type='remove')
                emb = discord.Embed(title='Успех!', color=config.COLORS["BASE"],
                                    description=f'У пользователя - {member.mention}, было успешно снято `{how_many}` монет!')
                await ctx.send(embed=emb)

        else:
            emb = discord.Embed(title='Ошибка!', color=config.COLORS["ERROR"],
                                description='Укажите положительно кол-во денег!')
            await ctx.send(embed=emb)

    @commands.command(
        name='balance',
        brief='Показывает счёт пользователя',
        usage='balance <участник>',
        description='Показывает сколько денег сейчас находится на счету указанного юзера'
    )
    async def _balance(self, ctx, member: discord.Member):
        emb = discord.Embed(color=config.COLORS["BASE"],
                            description=f'Счёт пользователя {member.mention}, в данный момент составляет - `{DB.Get().money(ctx=ctx, member=member)}`')
        await ctx.send(embed=emb)
    

def setup(client):
    client.add_cog(Eco(client))