import confuse
import asyncio
import bottom
import discord

config = confuse.Configuration('devsechan')

discordclient = discord.Client()
ircbot = bottom.Client(
    host=config['irc']['host'].get(str),
    port=6667,
    ssl=False)


@discordclient.event
async def on_message(message):
    if message.author == discordclient.user:
        return
    if message.channel.id != config['discord']['channel'].get():
        return
    formated = f"<{message.author}>: {message.content}"
    if len(message.attachments) >= 1:
        formated += message.attachments[0].url
    ircbot.send("PRIVMSG", target="#devse", message=formated)


@ircbot.on('CLIENT_CONNECT')
async def connect(**kwargs):
    ircbot.send('NICK', nick=config['irc']['nick'].get(str))
    ircbot.send('USER', user=config['irc']['username'].get(str),
                realname='Nyuuu')
    done, pending = await asyncio.wait(
        [ircbot.wait("RPL_ENDOFMOTD"),
         ircbot.wait("ERR_NOMOTD")],
        return_when=asyncio.FIRST_COMPLETED
    )
    for future in pending:
        future.cancel()
    ircbot.send('JOIN', channel="#devse")


@ircbot.on("privmsg")
async def irc_message(nick, target, message, **kwargs):
    if nick == config['irc']['nick'].get(str):
        return
    if target != config['irc']['channel'].get(str):
        return
    channel = discordclient.get_channel(config['discord']['channel'].get())
    await channel.send(f"**<{nick}>** {message}")


@ircbot.on('PING')
def keepalive(message, **kwargs):
    ircbot.send('PONG', message=message)


loop = asyncio.get_event_loop()
loop.create_task(ircbot.connect())
loop.create_task(discordclient.start(config['discord']['token'].get(str)))
loop.run_forever()
