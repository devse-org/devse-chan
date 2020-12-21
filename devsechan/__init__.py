import asyncio
import confuse
from devsechan.irc import IRC
from devsechan.discord import Discord


class DevSEChan:

    def __init__(self):
        self.config = confuse.Configuration('devsechan')
        self.loop = asyncio.get_event_loop()
        self.irc = IRC(self, self.config['irc'])
        self.discord = Discord(self, self.config['discord'])

    async def to_discord(self, nick, message):
        channel_id = self.config['discord']['channel'].get()
        channel = self.discord.get_channel(channel_id)
        await channel.send(f"**<{nick}>** {message}")

    def to_irc(self, author, msg_list):
        target = self.config['irc']['channel'].get()
        for msg in msg_list:
            self.irc.send('PRIVMSG', target=target, message=f"<{author}> {msg}")

    def run(self):
        token = self.config['discord']['token'].get()
        self.loop.create_task(self.irc.connect())
        self.loop.create_task(self.discord.start(token))
        self.loop.run_forever()
