import asyncio
import confuse
import re
from devsechan.irc import IRC
from devsechan.discord import Discord
import discord as ds


class DevSEChan:

    def __init__(self):
        self.config = confuse.Configuration('devsechan')
        self.loop = asyncio.get_event_loop()
        self.irc = IRC(self, self.config['irc'])
        self.discord = Discord(self, self.config['discord'])

    def get_guild(self):
        return self.discord.get_guild(self.config['discord']['guild'].get())

    def get_member_ping_to_id(self, nickname):
        member = self.get_guild().get_member_named(nickname)
        if member is not None:
            return f"<@{member.id}>"
        return None

    def get_guild_channel(self, name):
        for channel in self.get_guild().channels:
            if(channel.name == name):
                return channel

    def convert_irc_mentions_to_discord(self, message):
        mentions_regex = r"(?<=@)[a-zA-Z0-9]*"
        mentions_match = re.finditer(mentions_regex, message, re.MULTILINE)

        for mention in mentions_match:
            nickname = mention.group()
            member_id = self.get_member_ping_to_id(nickname)
            if member_id is not None:
                message = message.replace('@' + nickname, member_id)

        return message

    async def to_discord(self, nick, message):
        channel = self.get_guild_channel(self.config['discord']['irc_channel'].get())
        converted_message = self.convert_irc_mentions_to_discord( message)
        await channel.send(f"**<{nick}>** {converted_message}")

    def to_irc(self, author, msg_list):
        target = self.config['irc']['channel'].get()
        for msg in msg_list:
            if len(msg) > 0:
                self.irc.send('PRIVMSG', target=target,
                    message=f"<\x036{author}\x0F> {msg}")

    def run(self):
        token = self.config['discord']['token'].get()
        self.loop.create_task(self.irc.connect())
        self.loop.create_task(self.discord.start(token))
        self.loop.run_forever()
