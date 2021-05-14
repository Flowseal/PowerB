from tools.client_init import *

settings.commands['Information']['help'] = False

@slash.slash(name="help",
             description="Print list of commands")
async def help (ctx):
    
    member = ctx.author
    is_admin = member.guild_permissions.administrator

    emb = discord.Embed( title = 'Commands list:', description = '', colour = discord.Color.light_grey() )
    emb.set_author(name = client.user.name, icon_url = client.user.avatar_url)

    for table in settings.commands:
        commands = ''
        for cmd in settings.commands[table]:
            if (settings.commands[table][cmd]) and (not is_admin):
                continue
            commands += f'`{prefix}{cmd}` '
        
        if (commands != ''):
            emb.add_field( name = f'{table}', value = commands, inline=False)

    emb.set_thumbnail(url = "https://icons.iconarchive.com/icons/alecive/flatwoken/128/Apps-Help-icon.png")

    await ctx.send(embed=emb, hidden=True)

