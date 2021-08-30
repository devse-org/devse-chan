import asyncio
import time
import confuse
import re
from devsechan.irc import IRC
from devsechan.discord import Discord


class DevSEChan:

    def __init__(self):
        self.config = confuse.Configuration('devsechan')
        self.loop = asyncio.get_event_loop()
        self.irc = IRC(self, self.config['irc'])
        self.discord = Discord(self, self.config['discord'])

    async def to_discord(self, nick, message):
        await self.discord.send(nick, message)

    def to_irc(self, author, msg_list):
        for msg in msg_list:
            if len(msg) > 0:
                time.sleep(1)
                self.irc.send(author, msg)
                time.sleep(2)

    def run(self):
        self.loop.create_task(self.irc.start())
        self.loop.create_task(self.discord.start())
        self.loop.run_forever()
