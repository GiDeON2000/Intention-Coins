import discord
from discord.ext import commands
import psycopg2

conn = psycopg2.connect(dbname='Intention-CoinsBot', user='postgres',
                        password='postgres', host='localhost')
cursor = conn.cursor()


class Get:
    def money(self, ctx, member):
        cursor.execute("""CREATE TABLE IF NOT EXISTS eco(
            guild_id BIGINT,
            member_id BIGINT,
            cash BIGINT
        )""")

        cursor.execute(f"SELECT member_id FROM eco WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}")

        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO eco(guild_id, member_id, cash) VALUES ({ctx.guild.id}, {member.id}, 0)")
        
        conn.commit()

        cursor.execute(f"SELECT cash FROM eco WHERE guild_id = {ctx.guild.id} AND member_id = {member.id}")

        money_count = cursor.fetchone()[0]
        return money_count

# ============================================================

class Set:
    def add_rem_money(self, ctx, member, how_many, type):
        cursor.execute("""CREATE TABLE IF NOT EXISTS eco(
            guild_id BIGINT,
            member_id BIGINT,
            cash BIGINT
        )""")

        conn.commit()
        cursor.execute(f"SELECT member_id FROM eco WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}")

        if cursor.fetchone() is None:
            cursor.execute(f"INSERT INTO eco(guild_id, member_id, cash) VALUES ({ctx.guild.id}, {member.id}, 0)")
        
        conn.commit()
        if type == 'add':
            cursor.execute(f"UPDATE eco SET cash = cash + {int(how_many)} WHERE guild_id = {ctx.guild.id} AND member_id = {member.id}")
        elif type == 'remove':
            cursor.execute(f"UPDATE eco SET cash = cash - {int(how_many)} WHERE guild_id = {ctx.guild.id} AND member_id = {member.id}")


        conn.commit()

# ============================================================

class Delete:
    pass