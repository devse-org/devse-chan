import asyncio
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

    def get_member_ping_to_id(self, nickname, guild):
        return '<@' + str(guild.get_member_named(nickname).id) + '>'

    def convert_irc_mentions_to_discord(self, message, guild):
        mentions_regex = r"(?<=@)[a-zA-Z0-9]*"
        mentions_match = re.finditer(mentions_regex, message, re.MULTILINE)

        for mention in mentions_match:
            nickname = mention.group()
            message = message.replace('@' + nickname,
                                      self.get_member_ping_to_id(nickname, guild))

        return message

    async def to_discord(self, nick, message):
        channel_id = self.config['discord']['channel'].get()
        channel = self.discord.get_channel(channel_id)
        guild = channel.guild
        converted_message = self.convert_irc_mentions_to_discord(
            message, guild)
        await channel.send(f"**<{nick}>** {converted_message}")

    def to_irc(self, author, msg_list):
        target = self.config['irc']['channel'].get()
        for msg in msg_list:
            self.irc.send('PRIVMSG', target=target,
                          message=f"<\x036{author}\x0F> {msg}")

    def run(self):
        token = self.config['discord']['token'].get()
        self.loop.create_task(self.irc.connect())
        self.loop.create_task(self.discord.start(token))
        self.loop.run_forever()
