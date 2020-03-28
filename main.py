#!/usr/bin/env python3

import asyncio
import logging
import os
import sys

import argparse

from pykeybasebot import Bot
from poem_generator import GedichtenGenerator

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--user', help='Keybase username')
parser.add_argument('--key', help='Keybase paper key')
parser.add_argument('--model', help='GPT2 model (file path)')
parser.add_argument('--tokenizer', help='GPT2 tokenizer (file path)')
args = parser.parse_args()

textgenerator = GedichtenGenerator(args.model, args.tokenizer)

def get_message(inittext, memory_len=5):
    textlist = [inittext]

    iteration = 0
    end_poem = False
    while not end_poem:
        text = ""
        for i in range(0, min(len(textlist),memory_len)):
            text += textlist[i]
            if i==memory_len-1:
                textlist.pop(0)
            
        (message, end_poem) = textgenerator.generate_sentence(text)
        iteration += 1
        if iteration > 200:
            end_poem = True
        
        message = message.replace('/','').strip()
        textlist.append(message)
    return " ".join(textlist)
    
 class Handler:
    def __init__(self):
        self.lock = asyncio.Lock()
        
    async def __call__(self, bot, event):
        async with self.lock:
            channel = event.msg.channel
            msg_id = event.msg.id
            if event.msg.content.type_name == 'text':
                if event.msg.content.text.body.startswith('!sinterklaas'):
                    sentence = event.msg.content.text.body.split()[1:]
                    if not sentence:
                        sentence = ["Beste"]
                    await bot.chat.send(channel, "Sint: even denken...")
                    poem = get_message(" ".join(sentence))
                    await bot.chat.send(channel, poem)


listen_options = {
    "local": True,
    "wallet": False,
    "dev": False,
    "hide-exploding": False,
    "convs": True,
    "filter_channel": None,
    "filter_channels": None,
}

bot = Bot(
    username=args.user, paperkey=args.key, handler=Handler()
)

asyncio.run(bot.start(listen_options))
