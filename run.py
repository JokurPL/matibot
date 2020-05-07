import discord
from discord.ext import commands
from discord.utils import get
import io
import aiohttp
import youtube_dl
import os
import shutil

client = commands.Bot(command_prefix='m!')

@client.command()
async def info(ctx, member:discord.Member = None):
    if not member:
        embed = discord.Embed(
            title='Informacje o ```{}```'.format(ctx.author.display_name),
            description=None,
            colour=discord.Color.blue(),
        )
        embed.set_author(name=ctx.author.display_name, url=ctx.author.avatar_url, icon_url=ctx.author.avatar_url)
        embed.set_image(url=ctx.author.avatar_url)
        roles = ctx.author.roles
        i = 1
        for role in roles:
            embed.add_field(name=str(i), value="{}".format(role), inline=False)
            i += 1
    else:
        embed = discord.Embed(
            title='Informacje o {}'.format(member.display_name),
            description=None,
            colour=discord.Color.blue()
        )
        embed.set_author(name=member.display_name, url=member.avatar_url, icon_url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        roles = member.roles
        i = 1
        for role in roles:
            embed.add_field(name=str(i), value="{}".format(role), inline=False)
            i += 1
    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member: discord.Member):
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.avatar_url)) as resp:
            if resp.status != 200:
                return await ctx.send('Wystąpił błąd :/')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'cool_image.png'))

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Życie jest czadowe'))
    print("Im ready")

@client.command()
async def weeb(ctx):
    await ctx.send('Weeby do wora \nwur do jeziora \nwur wyłowiony \nweeb utopiony')
    await ctx.send("<:PeepoGlad:691962186024747008>")

@client.command()
async def clear(ctx, *, ammount):
    await ctx.channel.purge(limit=int(ammount))

@client.command()
async def join(ctx):
    if ctx.author.id == 443066496277807125 or ctx.author.id == 707196919688200224:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('Nie masz permisji, aby używać tego bota :)')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()

@client.command()
async def play(ctx, music: str):
    def check_queue():
        queue_infile = os.path.isdir("./Queue")
        if queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')
                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.7
            else:
                queues.clear()
                return
        else:
            queues.clear()

    song_1 = os.path.isfile("song.mp3")
    try:
        if song_1:
            os.remove("song.mp3")
            queues.clear()
    except PermissionError:
        await ctx.send("Coś poszło nie tak :/")
        return

    queue_infile = os.path.isdir("./Queue")
    try:
        queue_folder = "./Queue"
        if queue_infile is True:
            shutil.rmtree(queue_folder)
    except:
        print("XD")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([music])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.7
    nname = name.rsplit("-", 2)
    embed = discord.Embed(
        title='Teraz leci: {}'.format(nname[0]),
        colour=discord.Color.red()
    )
    await ctx.send(embed=embed)

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(
        title='Zatrzymujemy muzyczke <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    embederror = discord.Embed(
        title='Nie możemy zatrzymać muzyczki <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=embederror)
@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(
        title='Wznawiamy muzyczke <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    embederror = discord.Embed(
        title='Nie możemy wznowić muzyczki <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=embederror)

@client.command()
async def stop(ctx):
    embed = discord.Embed(
        title='Stopujemy muzyczke <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    embederror = discord.Embed(
        title='Nie możemy zstopwoać muzyczki <:PeepoGlad:691962186024747008>',
        colour=discord.Color.red()
    )
    voice = get(client.voice_clients, guild=ctx.guild)
    queues.clear()
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=embederror)

queues = {}

@client.command()
async def queue(ctx, url: str):
    queue_infile = os.path.isdir("./Queue")
    if queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue= False
            queues[q_num] = q_num
    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet' : True,
        'outtmpl' : queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    embed = discord.Embed(
        title='Dodaje ' + str(q_num) + "muzyczek",
        colour= discord.Color.red()
    )
    await ctx.send(embed=embed)

@client.command()
async def jestem(ctx):
    if ctx.author.id == 443066496277807125 or ctx.author.id == 707196919688200224:
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("jestem.mp3"), after=lambda e: print(f"No siema"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1
        await ctx.send("jestem")
    else:
        await ctx.send('Nie masz permisji, aby używać tego bota :)')

@client.command()
async def zw(ctx):
    if ctx.author.id == 443066496277807125 or ctx.author.id == 707196919688200224:
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("dotoalety.mp3"), after=lambda e: print(f"No nie ma"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1
        await ctx.send("do toalety ide")
    else:
        await ctx.send('Nie masz permisji, aby używać tego bota :)')

@client.event
async def on_message(ctx):
    if ctx.author.id == 692467190120710165:
            pepog = client.get_emoji(691963063313760267)
            await ctx.add_reaction(pepog)
    if ctx.author.id == 443066496277807125:
            pogyou = client.get_emoji(694153494906798150)
            await ctx.add_reaction(pogyou)
    if ctx.author.id == 513776637318397993:
            ayaya = client.get_emoji(692026877329670195)
            await ctx.add_reaction(ayaya)
    if ctx.author.id == 319898909147136001:
            peepoBeer = client.get_emoji(706782004309655653)
            await ctx.add_reaction(peepoBeer)
    if ctx.author.id == 691975307170807909:
            poop = '\U0001F4A9'
            await ctx.add_reaction(poop)
    if ctx.channel.id != 693036333005799444 and ctx.channel.id != 693071130717585498 and ctx.channel.id != 702783189877260418 and ctx.channel.id != 694596047917547550:
        if ctx.author.id == 415062677023490055:
                d = '\U0001F1E9'
                z = '\U0001F1FF'
                i = '\U0001F1EE'
                a = '\U0001F1E6'
                d2 = client.get_emoji(707275996390359181)
                await ctx.add_reaction(d)
                await ctx.add_reaction(z)
                await ctx.add_reaction(i)
                await ctx.add_reaction(a)
                await ctx.add_reaction(d2)
        if ctx.author.id == 310724070633373698:
                n = '\U0001F1F3'
                i = '\U0001F1EE'
                g = '\U0001F1EC'
                e = '\U0001F1EA'
                r = '\U0001F1F7'
                await ctx.add_reaction(n)
                await ctx.add_reaction(i)
                await ctx.add_reaction(g)
                await ctx.add_reaction(e)
                await ctx.add_reaction(r)
                # dog = client.get_emoji(694797074730057819)
                # await ctx.add_reaction(dog)
    await client.process_commands(ctx)
client.run('NTI4NTg1OTUwMjUxNDUwMzg0.Xo2Opg.y2Mlhu-BG4VkioHhsgzc3Y1XzGU')