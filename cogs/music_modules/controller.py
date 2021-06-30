from tools.client_init import *
from cogs.music_modules.song import SongQueue
from cogs.music_modules.youtube_dl import YTDLSource, VoiceError

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context, channel: discord.TextChannel):
        self.bot = bot  
        self._ctx = ctx

        self.channel = channel
        self.message = None
        bot.loop.create_task(self.prepare_channel())

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())
        

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    def empty_embed(self):
        embed = (discord.Embed(title='Nothing is playing now', color=discord.Color.magenta())
                .add_field(name='🎶 Request song', value='Use `/music play` to request your song')
                .set_thumbnail(url='https://icons.iconarchive.com/icons/bokehlicia/pacifica/128/multimedia-audio-player-icon.png')
                .set_author(name='Music bot', icon_url=self.bot.user.avatar_url)
                .set_footer(text='you can get other\'s commands using `/music ...`'))
        return embed

    async def prepare_channel(self):
        await self.channel.purge(limit=100)
        self.message = await self.channel.send(embed=self.empty_embed())

    async def audio_player_task(self):
        while True:
            self.next.clear()
            self.now = None

            if not self.message:
                await asyncio.sleep(2.0)
                continue

            await self.message.edit(embed=self.empty_embed())

            if self.loop == False:
                try:
                    async with timeout(180):
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return
                
                self.skip_votes.clear()
                self.current.source.volume = self._volume
                self.voice.play(self.current.source, after=self.play_next_song)
                await self.message.edit(embed=self.current.create_embed())
            
            elif self.loop == True:
                self.now = discord.FFmpegPCMAudio(self.current.source.stream_url, **YTDLSource.FFMPEG_OPTIONS)
                self.voice.play(self.now, after=self.play_next_song)
                await self.message.edit(embed=self.current.create_embed())
            
            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None

        if self.message:
            await self.message.edit(embed=self.empty_embed())
