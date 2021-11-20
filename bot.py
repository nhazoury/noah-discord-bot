# bot.py
import os
import ast

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MY_USER = os.getenv('DISCORD_USER')
DESTINY_BOT = os.getenv('DISCORD_DESTINY_BOT')
DESTINY_BOT_CHANNEL = os.getenv('DISCORD_DESTINY_BOT_CHANNEL')
DESTINY_PLAYERS = ast.literal_eval(os.environ['DISCORD_DESTINY_PLAYERS'])

intents = discord.Intents.all()
# client = discord.Client(intents=intents)
command_prefix = '£'
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

bot.im_dad = False
destiny_events = {}

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')

# direct messages whoever just joined
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the server!'
    )

@bot.event
async def on_message(message):
    # so that only non-bots can trigger this
    if message.author == bot.user:
        return

    imList = ['im ', 'i\'m ', 'Im ', 'I\'m ', 'IM ', 'I\'M ']
    # add events here

    if message.content == 'raise-exception':
        raise discord.DiscordException
    elif any(im in message.content for im in imList):
        if bot.im_dad and message.content != (command_prefix + 'imdad'):
            cut_message = message.content
            for i in range(0, len(imList)):
                cut_message = cut_message.split(imList[i], 1)[-1]
            response = 'Hi, ' + cut_message + ', I\'m dad!'
            await message.channel.send(response)
    # for using the Discord bot Charlemagne (https://warmind.io/). This way, when organising
    # events in #lfg, the event message generated is now pinned to the channel
    elif str(message.author) == DESTINY_BOT and str(message.channel) == DESTINY_BOT_CHANNEL:
        fireteam = message.embeds[0].fields[4]
        eventid = message.embeds[0].fields[3].value
        discord_team = []
        if 'Guardians Joined: ' in fireteam.name:
            await message.pin()
            for bungie_name in [*DESTINY_PLAYERS]:
                if bungie_name in fireteam.value:
                    discord_team.append(DESTINY_PLAYERS[bungie_name])
            destiny_events[eventid] = discord_team 

    await bot.process_commands(message)

@bot.command(name='imdad', help='Toggles the \'Hi, ..., I\'m dad!\' functionality')
async def im_dad(ctx):
    if str(ctx.message.author) == MY_USER:
        bot.im_dad = not bot.im_dad
        await ctx.send('Terrible dad jokes enabled? ' + str(bot.im_dad))

@bot.command(name='joke', help='Tells a very, very bad joke')
# ctx is short for context
async def bad_joke(ctx):
    response = 'We know that 6 is afraid of 7 because 7 8 9, but why did 7 eat 9?\nBecause you should eat 3 squared meals a day!'
    await ctx.send(response)


@bot.command(name='spam', help='Need to get someone\'s attention? Use this to spam them in their DMs. £spam num person')
async def spam(ctx, num, person: discord.Member = None):
    if person == bot.user or int(num) > 50:
        return
    await person.create_dm()
    for i in range(0, int(num)):
        await person.dm_channel.send(
            f'Hi {person.name}, {ctx.message.author.name} seems to be trying to get your attention...'
        )
    await ctx.send('Done spamming!')

@bot.command(name='destiny', help='Use to @ people for a Destiny 2 event, such as changing schedule, or a reminder')
async def destiny(ctx, eventid: str):
    team_members = destiny_events[eventid]
    update = 'Update for event ' + eventid + ': '
    for name in team_members:
        split_name = name.split('#')
        user = discord.utils.get(ctx.guild.members, name=split_name[0], discriminator=split_name[1])
        update += (f"{user} ")
    await ctx.send(update)

# @bot.command(name='remind', help='To remind people of some event')

# run cat err.log to view the error message if it has been raised
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise



bot.run(TOKEN)
