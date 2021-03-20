""" mac
python3 -m pip install -U discord.py
windows
py -3 -m pip install -U discord.py """

# Import discord library and logging library
import discord
import logging
import json
import os
import csv
from discord.ext import commands

# funcitons


def validate(modulo, dia, magIA):
    # modulo no existe
    if(not(modulo in magIA)):
        return False, 'Ese módulo no existe, porfavor intente de nuevo'

    # formato de dia es incorrecto
    try:
        int(dia[0])
        int(dia[1])
    except:
        return False, 'Tu formato de dia es incorrecto, porfavor intenta de nuevo'

    # formato de mes es incorrecto
    if(not(dia[2:] == 'marzo' or dia[2:] == 'abril' or dia[2:] == 'mayo')):
        return False, 'Tu formato de mes es incorrecto, porfavor intenta de nuevo'

    return True, "Se ha salvado exitosamenre"


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


# boot up
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


with open('./magIAObject.json') as myObject:
    magIA = json.load(myObject)


@bot.command()
async def getCode(ctx, modulo, dia):

    validated, message = validate(modulo, dia, magIA)
    if validated:
        await ctx.send('El código de {} {} es {}'.format(modulo, dia, magIA[modulo][dia]))
        return
    else:
        await ctx.send(message)


@bot.command()
async def setCode(ctx, modulo, dia, codigo):

    validated, message = validate(modulo, dia, magIA)
    if validated:

        # El codigo ya existe
        if(dia in magIA[modulo]):
            await ctx.send('Este código ya fue almacenado, para acceder a él usa el comando `$getCode`')
            return
        else:
            # almacenar código
            magIA[modulo][dia] = codigo

            # save code
            with open('./magIAObject.json', 'w') as myObject:
                json.dump(magIA, myObject)

            await ctx.send('El código de {} {} ha sido salvado correctamente'.format(modulo, dia))
            return
    else:
        await ctx.send(message)


@bot.command()
async def getLink(ctx):
    await ctx.send(content='Link de registro <http://registromagiajuvenil.southcentralus.cloudapp.azure.com/>', embed=None)


@bot.command()
async def contactInfo(ctx):
    await ctx.send(content='contacto_magiajuvenil@frskills.com')


@bot.command()
async def modulo(ctx, modulo=None):
    if modulo:
        modulo = str(modulo)
        with open("./InfoModulos/modulos.csv") as csv1:
            Modulos = csv.reader(csv1, delimiter=',', quotechar='|')
            content = ''
            for row in Modulos:
                if row[0] == modulo:
                    try:
                        content += row[2] + ' '+row[3] + ' ' + row[4] + \
                            "\n" + '<' + row[6] + '>' + "\n\n"
                    except:
                        print(row[5])
            print((len(content)))
            await ctx.send(embed=discord.Embed(title="Módulo"+modulo, description=content, colour=discord.Colour.purple()))

    else:
        description = """
        Modulo1 - Conoce el mundo de GitHub
        Modulo2 - Aprendiendo a Programar
        Modulo3 - El poder de los servidores
        Modulo4 - Fundamentos de Inteligencia Artificial
        """
        await ctx.send(embed=discord.Embed(title="Contenido de Modulos de magIA", description=description, colour=discord.Colour.purple()))

# run locally
with open('./config.json') as myObject:
    token = json.load(myObject)

bot.run(token)

# run on heroku
# bot.run(os.environ.get("DPY_TOKEN"))
