import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import re

class Discord:

    def __init__(self, parent, config):
        self.config = config

        intents = discord.Intents.default()
        intents.members = True
        self.bot = discord.Client(intents=intents)
        self.log_channel = None
        self.guild = None

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            if message.webhook_id:
                return
            if message.channel.id != self.config['channel'].get():
                return
            parent.to_irc(message.author, self.__format_message_for_irc(message))

        @self.bot.event
        async def on_message_delete(message):
            if message.channel == self.log_channel:
                return

            files = []

            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    files.append(f"<File    > {attachment.url}")

            files.append("```")

            data = "\n".join(["```markdown", "# Message Deleted",
                f"[{message.created_at}](#{message.channel})",
                f"< {message.author} >",
                f"<Message > {message.clean_content.replace('```', '')}"]
                + files)

            await self.log_channel.send(data)

        @self.bot.event
        async def on_ready():
            channel = self.bot.get_channel(self.config['channel'].get())
            self.guild = channel.guild
            self.log_channel = self.bot.get_channel(self.config['channel-log'].get())

    async def send(self, nick, message):
        avatar_url = None
        member = self.__member_from_nick(nick)
        if member is not None:
            avatar_url = member.avatar_url
        message = self.__format_message_for_discord(message)

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                self.config['webhook'].get(),
                adapter=AsyncWebhookAdapter(session))
            await webhook.send(message, username=nick, avatar_url=avatar_url)

    def __member_from_nick(self, nick):
        if self.guild is None:
            return None
        return self.guild.get_member_named(nick)

    def __format_message_for_discord(self, message):
        message = self.__convert_irc_mentions_to_discord(message)
        return message

    def __convert_irc_mentions_to_discord(self, message):
        mentions_regex = r"(?<=@)[a-zA-Z0-9]*"
        mentions_match = re.finditer(mentions_regex, message, re.MULTILINE)

        for mention in mentions_match:
            nick = mention.group()
            member = self.__member_from_nick(nick)
            if member is not None:
                message = message.replace('@' + nickname, f"<@{member.id}>")
        return message

    def __format_message_for_irc(self, message):
        content = message.content
        for user in message.mentions:
            substitute = f"@{user.name}#{user.discriminator}"
            content = content.replace(f"<@!{user.id}>", substitute)
            content = content.replace(f"<@{user.id}>", substitute)
        for channel in message.channel_mentions:
            content = content.replace(f"<#{channel.id}>", f"#{channel.name}")
        msg_list = content.split('\n')
        attachments_count = len(message.attachments)
        for i in range(attachments_count):
            msg_list.append(message.attachments[i].url)
        return msg_list

    async def start(self):
        return await self.bot.start(self.config['token'].get())
