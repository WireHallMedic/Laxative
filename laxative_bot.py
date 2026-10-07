import discord
import discord.ext
from discord.ext.commands import Bot
import json
import os
import re
import sys
import time
import socket
import laxative_engine

ADD_REGEX = re.compile("^add .*", re.IGNORECASE)
REMOVE_REGEX = re.compile("^remove .*", re.IGNORECASE)

# change cwd in case this is called from shell script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# let's load some things from files
token = open("token.txt", "r").read()
lax_engine = laxative_engine.LaxativeEngine()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = Bot(command_prefix = "!", intents = intents, case_insensitive = True)

@client.event
async def on_ready():
   print(f'{client.user} has connected to Discord')

# handle bad unrecognized command names
@client.event
async def on_command_error(ctx, error):
   print("Bad command for {}: {}".format(os.path.basename(__file__), str(error)), file = sys.stderr)

# handle messages
@client.event
async def on_message(message):
   # don't respond to self or empty messages
   if message.author == client.user or \
      len(message.content) == 0:
      return
   
   # format input
   content = cleanMessage(message.content)
   out_str = None
   authorName = re.sub("#.*", "", str(message.author))
   authorID = str(message.author.id)
   
   if content == "laxative":
      out_str = "I'm Laxative; I make Poopling easier. If you post a four-letter word, I'll list every word that is one letter off.\n\nPoople uses a private dictionary that is much smaller than the full list of four-letter English words; words I give you are not guaranteed to be in their dictionary."
   elif re.search(ADD_REGEX, content):
      search_results = re.search(ADD_REGEX, content).group(0).split()
      out_str = ""
      for i in range(1, len(search_results)):
         word = search_results[i].strip().upper()
         if len(word) != 4:
            out_str += f"{word} is not 4 letters long.\n"
         elif lax_engine.is_in_word_list(word):
            out_str += f"{word} already in dictionary.\n"
         else:
            lax_engine.add(word)
            out_str += f"Added {word}.\n"
   elif re.search(REMOVE_REGEX, content):
      search_results = re.search(REMOVE_REGEX, content).group(0).split()
      out_str = ""
      for i in range(1, len(search_results)):
         word = search_results[i].strip().upper()
         if not lax_engine.is_in_word_list(word):
            out_str += f"{word} not in dictionary.\n"
         else:
            lax_engine.remove(word)
            out_str += f"Removed {word}.\n"
   elif len(content) == 4:
      out_str = lax_engine.get_reply_message(content)
      
   # print results
   if out_str != None:
      await message.channel.send(out_str)

#strip message for processing
def cleanMessage(str):
   newStr = str
   if newStr[0] == "!":
      newStr = newStr[1:]
   newStr = newStr.lower()
   newStr = newStr.strip()
   return newStr

# fire this bad boy up
client.run(token, reconnect=True)