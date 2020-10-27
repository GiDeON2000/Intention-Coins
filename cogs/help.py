import discord
from discord.ext import commands 
import json
import config

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(
        name='help',
        aliases=['Help', 'HELP', 'хелп', 'Хелп', 'ХЕЛП'],
        brief='Информация о всех командах'
    )
    async def _help(self, ctx):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        PREFIX = prefixes[str(ctx.guild.id)]
        embed_all = discord.Embed(
            title="Навигация по командам бота!",
            color=config.COLORS["BASE"],
            description=f'Это экономический бот для сервера __** :maple_leaf: intentionXi | GAMING CENTRE**__\nСсылка: [клик](https://discord.gg/P4uzbuY)'
        )

        cog = self.client.cogs['экономика']

        name = cog.qualified_name
        commands = cog.get_commands()

        if name is not None:
            comm_list = []
            for command in commands:
                if not command.hidden:
                    comm_list.append(f"`{PREFIX}{command.name}`")

            embed_all.add_field(
                name=f"**__Все команды бота:__**",
                value=f"** **{', '.join(comm_list)}",
                inline=False)

        embed_all.set_footer(text=f'Запросил: {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_all)



def setup(client):
    client.add_cog(Help(client))