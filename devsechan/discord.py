
import discord


def Discord(parent, config):
    intents = discord.Intents.default()
    intents.members = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if message.webhook_id:
            return
        if message.channel.id != config['channel'].get():
            return
        content = message.content
        for user in message.mentions:
            substitute = f"@{user.name}#{user.discriminator}"
            content = content.replace(f"<@!{user.id}>", substitute).replace(f"<@{user.id}>", substitute)
        for channel in message.channel_mentions:
            content = content.replace(f"<#{channel.id}>", f"#{channel.name}")
        msg_list = content.split('\n')
        attachments_count = len(message.attachments)
        for i in range(attachments_count):
            msg_list.append(message.attachments[i].url)
        parent.to_irc(message.author, msg_list)

    return bot
