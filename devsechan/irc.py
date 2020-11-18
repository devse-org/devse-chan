import bottom
import asyncio


def IRC(parent, config):

    irc = bottom.Client(
        host=config['host'].get(),
        port=config['port'].get(),
        ssl=config['ssl'].get()
    )

    @irc.on('CLIENT_CONNECT')
    async def connect(**kwargs):
        irc.send('NICK', nick=config['nick'].get())
        irc.send('USER', user=config['username'].get(), realname='https://devse.wiki/')

        done, pending = await asyncio.wait(
            [irc.wait('RPL_ENDOfMOTD'), irc.wait('ERR_NOMOTD')],
            return_when=asyncio.FIRST_COMPLETED)
        for future in pending:
            future.cancel()

        # FIXME: maybe a cleaner way to do this with confuse (maybe I'll just drop confuse)
        try:
            irc.send('PRIVMSG', target="nickserv", message=f"IDENTIFY {config['nickserv'].get()}")
        except BaseException:
            pass
        irc.send('JOIN', channel=config['channel'].get())

    @irc.on('privmsg')
    async def irc_message(nick, target, message, **kwargs):
        if nick == config['nick'].get():
            return
        if target != config['channel'].get():
            return
        await parent.to_discord(nick, message)

    @irc.on('PING')
    async def irc_ping(message, **kwargs):
        irc.send('PONG', message=message)

    return irc
