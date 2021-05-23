from tools.client_init import *
from bs4 import BeautifulSoup
import re
import requests

url = requests.get('https://discordpy.readthedocs.io/en/stable/api.html#discord.VoiceRegion')
soup = BeautifulSoup(url.content, 'html.parser')

rs = soup.find_all('dt', id = re.compile('discord.VoiceRegion.'))
regions_list = [reg.code.text for reg in rs]
regions_choices = [create_choice(
                    name=rg,
                    value=rg) for rg in regions_list]


settings.commands['Server']['region_change'] = True
settings.commands['Server']['region'] = False

@slash.slash(name="region_change",
             description="Changes the server region",
             options=[
               create_option(
                 name="state",
                 description="name of the region",
                 option_type=SlashCommandOptionType.STRING, # string to give a choice
                 required=True,
                 choices=regions_choices,
               )
             ])
             
async def region_change (ctx, state:str):
  if not await is_admin_notify(ctx):
    return False

  rg = state.replace('_', '-')
  old_region = str(ctx.guild.region).replace('_', '-')

  if (rg == old_region):
    emb = discord.Embed( title = '☔  Nothing happened?', description = '', colour = discord.Color.light_grey() )
    await ctx.send(embed=emb, hidden=True)
    return False

  await ctx.guild.edit(region=discord.VoiceRegion(rg))

  emb = discord.Embed( title = f"✅ Region changed from {old_region} to {str(ctx.guild.region)}!", description = '', colour = discord.Color.green() )
  await ctx.send(embed=emb, hidden=True)

@slash.slash(name="region",
             description="Returns current server region")
async def region (ctx):
    emb = discord.Embed( title = 'Current region:', description = f'🌍 {str(ctx.guild.region)}', colour = discord.Color.light_grey() )
    await ctx.send(embed=emb, hidden=True)