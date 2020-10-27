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

client = commands.Bot(command_prefix=func.get_prefix)
client.remove_command('help')

ConnectionMain = False


@client.event
async def on_ready():
    global ConnectionMain

    if not ConnectionMain:
        print("\n======================")
        print("Подключились к Discord\n")
        print(f"Количество Шардов: {client.shard_count}")
        print(f"Тег бота: {client.user.name}#{client.user.discriminator}")
        print(f"ID: {str(client.user.id)}")
        print("======================\n")

        ConnectionMain = True

    else:
        print("\n======================")
        print("ERROR: Бот ивент on_ready сработал ещё раз!")
        print("======================\n")



@client.event
async def on_disconnect():
    print("\n======================")
    print("ERROR: Бот отключился от Discord'a!")
    print("======================\n")


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = config.settings["DEFAULT_PREFIX"]

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command(
    name='поменять-префикс',
    aliases=['change-prefix']
)
@commands.has_permissions(administrator=True)
async def _change_prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(embed = discord.Embed (title = "Изменено", color=config.COLORS["BASE"], description = f"Префикс изменён на: {prefix}") )



@client.event
async def on_command_error(ctx, err):
    try:
        if isinstance(err, errors.CommandNotFound):
            await ctx.message.add_reaction('❌')

        elif isinstance(err, errors.BotMissingPermissions):
            await ctx.send(
                embed=discord.Embed(color=config.COLORS['ERROR'],
                                    description=f"У бота отсутствуют права: {' '.join(err.missing_perms)}\nВыдайте их ему для полного функционирования бота"))
        elif isinstance(err, errors.MissingPermissions) or isinstance(err, errors.CheckFailure):
            await ctx.send(embed=discord.Embed(color=config.COLORS['ERROR'],
                                               description=f"У вас недостаточно прав для запуска этой команды или она отключена!"))
        elif isinstance(err, errors.UserInputError):
            await ctx.send(embed=discord.Embed(color=config.COLORS['ERROR'],
                                               description=f"Правильное использование команды `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`"))

        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(color=config.COLORS['ERROR'],
                                               description=f"У вас еще не прошел кулдаун на команду `{ctx.prefix}{ctx.command}`!\nПодождите еще {err.retry_after:.2f} секунд"))
        elif isinstance(err, discord.Forbidden):
            await ctx.send(embed=discord.Embed(color=config.COLORS['ERROR'],
                                               description=f"У бота нет прав на запуск этой команды!"))
        else:
            await ctx.send(embed=discord.Embed(color=config.COLORS['ERROR'],
                                               description=f"Произошла неизвестная ошибка: \n`{err}`"))
            raise err

    except dpy_errors.Forbidden:
        pass

for file in os.listdir('./cogs'):
    if file.endswith(".py"):
        client.load_extension(f'cogs.{file[:-3]}')
        print(f"Загружен ког - {file[:-3]}")


client.run(config.settings['TOKEN'])