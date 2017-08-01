import discord
import asyncio
from os import listdir, path

client = discord.Client()

username = ""
password = ""
selfbot = False
prefix = ""

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def parseLSL(path):
    with open(path) as file:
        data = file.read()
        if data[-1] != '\n':
            data += '\n'

    buf = ""

    commands = []

    for c in data:
        if c != '\n':
            buf += c
        else:
            buf += c
            args = []
            buf2 = ""
            for b in buf:
                if b != ' ' and b != '\n':
                    buf2 += b
                else:
                    args.append(buf2)
                    buf2 = ""
            commands.append(args)
            buf = ""

    return commands

initCommands = parseLSL("init.lsl")
for c in initCommands:
    if c[0] == "user":
        username = c[1]
    elif c[0] == "pass":
        password = c[1]
    elif c[0] == "mode":
        if c[1] == "self":
            selfbot = True
    elif c[0] == "prefix":
        prefix = c[1] + " "

class Command:
    trigger = ""
    response = ""
    def __init__(self, trigger, response):
        self.trigger = trigger
        self.response = response


command_mods = []
for file in listdir("modules"):
    _, ext = path.splitext(file)
    if ext == ".lsl":
        commands = parseLSL("modules/" + file)
        trigger = ""
        response = ""
        for c in commands:
            if c[0] == "trigger":
                trigger = c[1]
            elif c[0] == "response":
                response = c[1]
        command_mods.append(Command(trigger, response))

@client.event
async def on_message(message):
    if selfbot and message.author != client.user:
            return

    if message.content.startswith(prefix):
        content = message.content[len(prefix):]
        for command in command_mods:
            if content.startswith(command.trigger):
                await client.send_message(message.channel, command.response)

client.run(username, password)