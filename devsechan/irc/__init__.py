from irc.bot import SingleServerIRCBot, ServerSpec
import asyncio

from devsechan.utils import version, user
from devsechan.irc.channel import ChannelGuard

class IRC(SingleServerIRCBot):

    def __init__(self, parent, config):
        super().__init__(self, [(config['host'].get(), config['port'].get())], config['nick'].get(), config['username'].get(),'https://devse.wiki/')
        self.config = config
        self.parent = parent
        self.guard = ChannelGuard()

    def on_welcome(self, connection, event):
        # FIXME: maybe a cleaner way to do this with confuse (maybe I'll just drop confuse)
        try:
            connection.privmsg(target="nickserv", message=f"IDENTIFY {self.config['nickserv'].get()}")
        except BaseException:
            pass
        connection.join(channel=self.config['channel'].get())

    def on_ctcp(self, connection, event):
        nick = event.source.nick
        if event.arguments[0] == "VERSION":
            connection.ctcp_reply(nick, f"VERSION {version.version()}")
        elif event.arguments[0] == "SOURCE":
            connection.ctcp_reply(nick, 'SOURCE https://github.com/d0p1s4m4/devse-chan')


    def irc_message(self, nick, target, message, **kwargs):
        if nick == config['nick'].get():
            return
        if target == config['nick'].get():
            if message == '\001VERSION\001':
                self.irc.send(
                    'NOTICE',
                    target=nick,
                    message=f"\001VERSION {version.version()}\001")
            elif message == '\001SOURCE\001':
                self.irc.send(
                    'NOTICE',
                    target=nick,
                    message='\001SOURCE https://github.com/d0p1s4m4/devse-chan\001')
            return
        elif target != config['channel'].get():
            return
        if self.guard.is_spammer(nick, message):
            return

        self.parent.to_discord(nick, message)

    def send(self, nick, message):
        colored_nick = user.irc_colorize_nick(nick)
        self.irc.connection.privmsg(target=self.config['channel'].get(), message=f"<{colored_nick}> {message}")

    async def start(self):
        return await self.irc.start()
