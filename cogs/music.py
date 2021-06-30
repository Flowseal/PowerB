from tools.client_init import *

from cogs.music_modules.youtube_dl import *
from cogs.music_modules.song import *
from cogs.music_modules.controller import *

guild_states = {}

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

        bot.loop.create_task(self.scan_errors())

    async def scan_errors(self):
        while True:
            for id in guild_states:
                vs = self.voice_states.get(int(id))
                if vs is not None:
                    if guild_states[id]['leave']:
                        vs.skip()
                        await vs.stop()
                        vs.play_next_song()

                        guild_states[id]['leave'] = False


            await asyncio.sleep(5.0)


    async def get_music_channel(self, ctx: commands.Context):
        with open('files/music.json') as f:
            table = json.load(f)
        
        id = str(ctx.guild.id)
        if id not in table:
            await ctx.send('Set the music channel first!', hidden=True)
            raise Exception('Music channel not setted')

        return ctx.guild.get_channel(table[id])

    async def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)

        if not state:
            state = VoiceState(self.bot, ctx, await self.get_music_channel(ctx))
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context): 
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = await self.get_voice_state(ctx)

    async def cog_after_invoke(self, ctx: commands.Context):
        self.voice_states[ctx.guild.id] = ctx.voice_state

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send(f'An error occurred: `{str(error)}`')

    settings.commands['Music']['set-music-channel'] = False
    @cog_ext.cog_slash(name='set-music-channel',
                description='Sets music bot channel',
                options=[
                create_option(
                 name="channel",
                 description="Tag the needed text channel with '#'",
                 option_type=SlashCommandOptionType.CHANNEL,
                 required=True,
                )
                ])
    async def set_music_channel (self, ctx, channel):
        if not await is_admin_notify(ctx):
            return False

        if not hasattr(channel, 'last_message'):
            emb = discord.Embed( title = 'You need to tag text channel', description = '', colour = discord.Color.red() )
            await ctx.send(embed=emb, hidden=True)
            return

        with open('files/music.json') as f:
            table = json.load(f)

        id = str(ctx.guild.id)
        table[id] = channel.id

        with open('files/music.json', 'w') as f:
            json.dump(table, f)

        state = VoiceState(self.bot, ctx, await self.get_music_channel(ctx))
        self.voice_states[ctx.guild.id] = state
        ctx.voice_state = state

        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )
        await ctx.send(embed=emb, hidden=True)


    settings.commands['Music']['music join'] = False
    @cog_ext.cog_subcommand(base="music", name='join',
                description='Music bot joins the channel',           
                options=[
                create_option(
                 name="channel",
                 description="Tag the needed voice channel with '#'",
                 option_type=SlashCommandOptionType.CHANNEL,
                 required=False,
                )
                ])
    async def join (self, ctx, channel=None):
        await self.cog_before_invoke(ctx)

        if channel and not hasattr(channel, 'voice_states'):
            emb = discord.Embed( title = 'You need to tag voice channel', description = '', colour = discord.Color.red() )
            await ctx.send(embed=emb, hidden=True)
            return
        
        if ctx.author.voice or channel:
            destination = channel or ctx.author.voice.channel
        else:
            emb = discord.Embed( title = 'You are not connected to any voice channel', description = '', colour = discord.Color.red() )
            return await ctx.send(embed=emb, hidden=True)


        if ctx.voice_state.voice:
            if destination.id == ctx.voice_state.voice.channel.id:
                emb = discord.Embed( title = 'Bot already exists', description = '', colour = discord.Color.red() )
                return await ctx.send(embed=emb, hidden=True)

            await ctx.voice_state.voice.disconnect()
            
        ctx.voice_state.voice = await destination.connect()

        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

    
    settings.commands['Music']['music leave'] = False
    @cog_ext.cog_subcommand(base="music", name='leave',
                description='Music bot leaves current channel',
                )
    async def leave (self, ctx):
        await self.cog_before_invoke(ctx)

        await ctx.voice_state.stop()
        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

    
    settings.commands['Music']['music volume'] = False
    @cog_ext.cog_subcommand(base="music", name='volume',
                description='Sets volume of tracks',              
                options=[
                create_option(
                 name="volume",
                 description="New volume value [0; 100]",
                 option_type=SlashCommandOptionType.STRING,
                 required=True,
                )
                ])
    async def volume (self, ctx, volume):
        await self.cog_before_invoke(ctx)

        volume = int(volume)
        if (volume < 0) or (volume > 100):
            emb = discord.Embed( title = 'Invalid volume value! (0 <= volume <= 100)', description = '', colour = discord.Color.red() )
            return await ctx.send(embed=emb, hidden=True)

        ctx.voice_state.volume = volume / 100.0
        ctx.voice_state.current.source.volume = volume / 100.0
        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)
    

    settings.commands['Music']['music pause'] = False
    @cog_ext.cog_subcommand(base="music", name='pause',
                description='Pause music bot',
                )
    async def pause (self, ctx):
        await self.cog_before_invoke(ctx)

        emb = discord.Embed( title = 'Music bot has been already stopped', description = '', colour = discord.Color.red() )

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )

        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)
    

    settings.commands['Music']['music resume'] = False
    @cog_ext.cog_subcommand(base="music", name='resume',
                description='Resume music bot',
                )
    async def resume (self, ctx):
        await self.cog_before_invoke(ctx)

        emb = discord.Embed( title = 'Music bot is playing', description = '', colour = discord.Color.red() )

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )
        
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

    
    settings.commands['Music']['music stop'] = False
    @cog_ext.cog_subcommand(base="music", name='stop',
                description='Stop music bot',
                )
    async def stop (self, ctx):
        await self.cog_before_invoke(ctx)

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()

        await ctx.voice_state.message.edit(embed=ctx.voice_state.empty_embed())

        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )   
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

    
    settings.commands['Music']['music loop'] = False
    @cog_ext.cog_subcommand(base="music", name='loop',
                description='Loop current song',
                )
    async def loop (self, ctx):
        await self.cog_before_invoke(ctx)

        if not ctx.voice_state.is_playing:
            emb = discord.Embed( title = 'Nothing is playing now', description = '', colour = discord.Color.red() )
            return await ctx.send(embed=emb, hidden=True)

        ctx.voice_state.loop = not ctx.voice_state.loop
        emb = discord.Embed( title = 'Successful', description = '', colour = discord.Color.green() )   
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

    
    settings.commands['Music']['music skip'] = False
    @cog_ext.cog_subcommand(base="music", name='skip',
                description='Vote skip current song',
                )
    async def skip (self, ctx):
        await self.cog_before_invoke(ctx)

        if not ctx.voice_state.is_playing:
            emb = discord.Embed( title = 'Nothing is playing now', description = '', colour = discord.Color.red() )
            return await ctx.send(embed=emb, hidden=True)

        autoskip = is_admin(ctx.author) or ctx.author == ctx.voice_state.current.requester

        if autoskip:
            await ctx.voice_state.message.edit(embed=ctx.voice_state.empty_embed())
            ctx.voice_state.skip()
            emb = discord.Embed( title = 'Successful!', description = '', colour = discord.Color.green() )
            await self.cog_after_invoke(ctx)
            return await ctx.send(embed=emb, hidden=True)

        if ctx.author.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.append(ctx.author.id)

        votes = len(ctx.voice_state.skip_votes)
        if votes >= math.ceil(len(ctx.voice_state.voice.members) / 3):
            await ctx.voice_state.message.edit(embed=ctx.voice_state.empty_embed())
            ctx.voice_state.skip()

        emb = discord.Embed( title = 'Successful', description = f'Votes: {len(ctx.voice_state.skip_votes)}/{math.ceil(len(ctx.voice_state.voice.members) / 3)}', colour = discord.Color.green() )   
        await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)

   
    settings.commands['Music']['music play'] = False
    @cog_ext.cog_subcommand(base="music", name='play',
                description='Request song',                
                options=[
                create_option(
                 name="source",
                 description="URL or song keywords",
                 option_type=SlashCommandOptionType.STRING,
                 required=True,
                )
                ])
    async def play (self, ctx:SlashContext, source:str):
        await self.cog_before_invoke(ctx)
        await ctx.defer(hidden=True)

        if not ctx.voice_state.voice:
            if ctx.author.voice:
                ctx.voice_state.voice = await ctx.author.voice.channel.connect()
            else:
                emb = discord.Embed( title = 'Bot doesn\'t connected to any voice channel', description = '', colour = discord.Color.red() )
                return await ctx.send(embed=emb, hidden=True)

        try:
            source = await YTDLSource.create_source(ctx, source, loop=self.bot.loop)
        except YTDLError as e:
            await ctx.send('An error occurred while processing this request: {}'.format(str(e)), hidden=True)
        else:

            song = Song(source)
            await ctx.voice_state.songs.put(song)

            emb = discord.Embed( title = 'Successful!', description = f'{str(source)} added in a queue', colour = discord.Color.green() )
            await ctx.send(embed=emb, hidden=True)

        await self.cog_after_invoke(ctx)
    

    settings.commands['Music']['music queue'] = False
    @cog_ext.cog_subcommand(base="music", name='queue',
                description='Song requests list',
                options=[
                create_option(
                 name="page",
                 description="Page number",
                 option_type=SlashCommandOptionType.STRING,
                 required=False,
                )
                ])
    async def queue (self, ctx, page:str=''):
        await self.cog_before_invoke(ctx)

        if len(ctx.voice_state.songs) <= 0:
            emb = discord.Embed( title = 'Songs queue is empty', description = '', colour = discord.Color.red() )
            return await ctx.send(embed=emb, hidden=True)

        if not page:
            page = 1
        page = int(page)

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        if (page > pages):
            page = pages
                       
        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(title='Songs queue', description='**{} songs:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                .set_footer(text='Page {}/{}'.format(page, pages)))

        await ctx.send(embed=embed, hidden=True)

        await self.cog_after_invoke(ctx)


''' To fix some unexpected errors due to bot leaves/crash '''
async def on_voice_state_update(member, before, after):
    if member.id != client.user.id:
        return
    
    if after.channel is None:
        pass
    else: return

    id = str(before.channel.guild.id)

    global guild_states
    if id not in guild_states:
        guild_states[id] = {}

    guild_states[id]['leave'] = True


def setup(client: commands.Bot):
    client.add_cog(Music(client))