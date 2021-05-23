from tools.imports import *

def is_admin(user:discord.Member):
    return user.guild_permissions.administrator

async def is_admin_notify(ctx):
    if (not ctx.author.guild_permissions.administrator):
        emb = discord.Embed( title = "⛔ You cant't access this command!", description = '', colour = discord.Color.red() )
        await ctx.send(embed=emb, hidden=True)
        return False
    
    return True