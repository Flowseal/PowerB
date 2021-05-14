from tools.client_init import *

settings.commands['Voice rooms']['voice_room_set'] = True

@slash.slash(name="voice_room_set",
             description="Set the room creator from temp voice rooms",
             guild_ids = [621295534971420683],
             options=[
               create_option(
                 name="room_id",
                 description="id of the created voice-channel room-creator",
                 option_type=SlashCommandOptionType.STRING, # idk why but integer fucks up
                 required=True
               )
             ])
async def voice_room_set(ctx, room_id: int):
  with open('files/voice_rooms.json', 'r') as f:
    table = json.load(f)
  
  room_creator = client.get_channel(int(room_id))
  if (not room_creator):
    await ctx.send('Wrong ID :red_circle:', hidden=True)
    return False

  await ctx.send('Successful :green_circle:', hidden=True)
  
  table[str(ctx.guild.id)] = int(room_id)

  with open('files/voice_rooms.json', 'w') as f:
    json.dump(table, f)



async def on_voice_state_update(member, before, after):
  print('trigger')
  if member.bot:
    return False

  with open('files/voice_rooms.json', 'r') as f:
    table = json.load(f)

  guild_id = None
  if (after.channel == None):
    guild_id = before.channel.guild.id
  else:
    guild_id = after.channel.guild.id

  room_creator = client.get_channel(int(table[str(guild_id)]))

  if (not room_creator):
    return False

  # If user joined to the room creator channel
  if after.channel == room_creator:
    channel = await after.channel.guild.create_voice_channel(f'{member.name} room', category=room_creator.category)
    if channel is not None:
      await member.move_to(channel)
      await channel.set_permissions(member, manage_channels=True)
    
  # If user leaved temp room
  if before.channel is not None:
    if before.channel != room_creator and before.channel.category == room_creator.category:
      if len(before.channel.members) == 0:
        await before.channel.delete()

