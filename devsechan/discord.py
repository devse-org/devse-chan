
import discord


def Discord(parent, config):

    bot = discord.Client()

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        if message.channel.id != config['channel'].get():
            return

        msg_list = message.content.split('\n')

        attachments_count = len(message.attachments)
        for i in range(attachments_count):
            msg_list.append(message.attachments[i].url)
        parent.to_irc(message.author, msg_list)

    return bot
