# bot.py
import os

import discord
from dotenv import load_dotenv
import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
# cred = credentials.Certificate("./cred.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# Needed for local dev
# load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents(messages=True, members=True, guilds=True)
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

def create_message(name1, name2):
    return "**Hey " + name1 + "!**\n\nHere's an opportunity to get to meet " + name2 + " this week! Feel free to find some time together and hangout!\n\nI recommend finding 30 minutes in the next week to say hello on Zoom, Hangouts, or whatever works :)"  

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if "testing content" in message.content:
        channel = message.channel
        await channel.send("up and running!")
        return

    if "make hangouts" in message.content:
        channel = message.channel
        
        members = await message.guild.fetch_members(limit=150).flatten()

        filtered_members = []
        # ivan = ""

        # there's a .roles field
        for member in members:
            names = [role.name for role in member.roles]
            if "fellow" in names:
                filtered_members.append(member)
        
        # doc = db.collection(u'servers').document(u'Reboot-Fellowship-2022')
        # curr_doc = doc.get()
        # data = ""
        # if (curr_doc.exists):
        #     data = curr_doc.to_dict()

        # print(data)


        # doc.set({u'matched_names': { "ivan": ["lucas"]}})
        pairs = {}

        while len(filtered_members) > 1:
            # Using the randomly created indices, respective elements are popped out
            r1 = random.randrange(0, len(filtered_members))
            elem1 = filtered_members.pop(r1)

            r2 = random.randrange(0, len(filtered_members))
            elem2 = filtered_members.pop(r2)

            # now the selecetd elements are paired in a dictionary 
            pairs[elem1] = elem2
        
        for person1, person2 in pairs.items():
            dm_channel1, dm_channel2 = "", ""
            if (person1.dm_channel):
                dm_channel1 = person1.dm_channel
            else:
                dm_channel1 = await person1.create_dm()
            
            if (person2.dm_channel):
                dm_channel2 = person2.dm_channel
            else:
                dm_channel2 = await person2.create_dm()

            message1 = create_message(person1.display_name, person2.display_name)
            message2 = create_message(person2.display_name, person1.display_name)
            print(message1)
            print(message2)
            await channel.send(person1.name + " " + person2.name)
            await dm_channel1.send(message1)
            await dm_channel2.send(message2)


        # Code for dm'ing
        # dm_channel = ""
        # if ivan.dm_channel:
        #     dm_channel = ivan.dm_channel
        # else:
        #     dm_channel = await ivan.create_dm()
        # print(dm_channel)

        # message = "**Hey " + ivan.name + "!**\n\nThis is your weekly meetup note that you're meeting with " + ivan.name + " this week! Feel free to find some time together and hangout!"  
        # await dm_channel.send(message)


        await channel.send("Completed!")
        return

client.run(TOKEN)