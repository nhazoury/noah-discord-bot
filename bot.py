# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
MY_USER = os.getenv('DISCORD_USER')

intents = discord.Intents.all()
# client = discord.Client(intents=intents)
command_prefix = '£'
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

bot.im_dad = False

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
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

    imList = ['im', 'i\'m', 'Im', 'I\'m']
    # add events here

    if message.content == 'raise-exception':
        raise discord.DiscordException
    elif any(im in message.content for im in imList):
        if bot.im_dad and message.content != (command_prefix + 'imdad'):
            cut_message = message.content
            for i in range(0, len(imList)):
                cut_message = cut_message.split('im', 1)[-1]
            response = 'Hi,' + cut_message + ', I\'m dad!'
            await message.channel.send(response)
    
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

# run cat err.log to view the error message if it has been raised
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise



bot.run(TOKEN)
