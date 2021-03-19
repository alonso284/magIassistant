# Welcome, to the TI club discord bot code.

# introduction

""" mac
python3 -m pip install -U discord.py
windows
py -3 -m pip install -U discord.py """

# Import discord library and logging library
import discord
import logging
#import intents
from discord.ext import commands
# Import JSON
import json
import os


# Set up logging
""" logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler) """

# setup intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

# client = discord.Client()
bot = commands.Bot(command_prefix='$')

# fix boot
# boot up


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

""" 
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('hello'):
#         await message.channel.send('Hello!') """

with open('./magIAObject.json') as myObject:
    magIA = json.load(myObject)

""" with open('./config.json') as myObject:
    token = json.load(myObject) """


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def getCode(ctx, modulo, dia):

    # modulo no existe
    if(not(modulo in magIA)):
        await ctx.send('Ese módulo no existe, porfavor intente de nuevo')
        return

    # formato de dia es incorrecto
    try:
        int(dia[0])
        int(dia[1])
    except:
        await ctx.send('Tu formato de dia es incorrecto, porfavor intenta de nuevo')
        return

    # formato de mes es incorrecto
    if(not(dia[2:] == 'marzo' or dia[2:] == 'abril' or dia[2:] == 'mayo')):
        await ctx.send('Tu formato de mes es incorrecto, porfavor intenta de nuevo')
        return

    await ctx.send('El código es {}'.format(magIA[modulo][dia]))
    return


@bot.command()
async def setCode(ctx, modulo, dia, codigo):

    # modulo no existe
    if(not(modulo in magIA)):
        await ctx.send('Ese módulo no existe, porfavor intente de nuevo')
        return

    # formato de dia es incorrecto
    try:
        int(dia[0])
        int(dia[1])
    except:
        await ctx.send('Tu formato de dia es incorrecto, porfavor intenta de nuevo')
        return

    # formato de mes es incorrecto
    if(not(dia[2:] == 'marzo' or dia[2:] == 'abril' or dia[2:] == 'mayo')):
        await ctx.send('Tu formato de mes es incorrecto, porfavor intenta de nuevo')
        return

    # El codigo ya existe
    if(dia in magIA[modulo]):
        await ctx.send('Este código ya fue almacenado, para acceder a él usa el comando `$getCode`')
        return

    # almacenar código
    magIA[modulo][dia] = codigo
    with open('./magIAObject.json', 'w') as myObject:
        json.dump(magIA, myObject)
    await ctx.send('El código de {} {} ha sido salvado correctamente'.format(modulo, dia))
    return


@bot.command()
async def getLink(ctx):
    await ctx.send(content='Link de registro <http://registromagiajuvenil.southcentralus.cloudapp.azure.com/>', embed=None)


@bot.command()
async def contactInfo(ctx):
    await ctx.send(content='contacto_magiajuvenil@frskills.com')


bot.run(os.environ.get("DPY_TOKEN"))
