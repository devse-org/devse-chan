from re import M
import bottom
import asyncio
import platform

from devsechan.utils import version


class IRC:

    def __init__(self, parent, config):
        self.config = config
        self.irc = bottom.Client(host=config['host'].get(), port=config['port'].get(), ssl=config['ssl'].get())

        @self.irc.on('CLIENT_CONNECT')
        async def connect(**kwargs):
            self.irc.send('NICK', nick=config['nick'].get())
            self.irc.send('USER', user=config['username'].get(), realname='https://devse.wiki/')

            done, pending = await asyncio.wait(
                [self.irc.wait('RPL_ENDOFMOTD'), self.irc.wait('ERR_NOMOTD')],
                return_when=asyncio.FIRST_COMPLETED)
            for future in pending:
                future.cancel()

            # FIXME: maybe a cleaner way to do this with confuse (maybe I'll just drop confuse)
            try:
                self.irc.send('PRIVMSG', target="nickserv", message=f"IDENTIFY {config['nickserv'].get()}")
            except BaseException:
                pass
            self.irc.send('JOIN', channel=config['channel'].get())

        @self.irc.on('privmsg')
        async def irc_message(nick, target, message, **kwargs):
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
            elif target != config['channel'].get():
                return
            await parent.to_discord(nick, message)

        @self.irc.on('PING')
        async def irc_ping(message, **kwargs):
            self.irc.send('PONG', message=message)

    def send(self, nick, message):
        self.irc.send('PRIVMSG', target=self.config['channel'].get(), message=f"<\x036{nick}\x0F> {message}")

    async def start(self):
        return await self.irc.connect()
