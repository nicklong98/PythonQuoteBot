import discord
import re
import random
from app import app, db
from app.models import Quote

token = app.config['DISCORD_TOKEN']
shit_pants_percent = app.config['SHIT_PANTS_PERCENT']
print(token)
client = discord.Client()


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.message):
    if message.author == client.user or not message.content.startswith('!q'):
        return
    body = re.sub('<@![0-9]*>', '', message.content[2:]).strip()
    server = message.channel.guild
    if message.mentions:
        for mention in message.mentions:
            db.session.add(Quote(user_id=mention.id, reporter_id=message.author.id, server_id=server.id, body=body))
        db.session.commit()
        return
    # if there are no mentions, get a quote, but only from the server
    quote = random.choice(Quote.query.filter_by(server_id=server.id).all())
    should_add_shit_pants_quote = random.randint(0, 100) <= shit_pants_percent
    author = server.get_member(quote.user_id)
    author_name = author.nick if author is not None else 'Someone who isn\'t here anymore'
    message_to_send = quote.body + ' and then I shit my only pair of pants. I swear to god I did.' if should_add_shit_pants_quote else quote.body
    formatted_message = '''
```
''' + message_to_send + '''
- ''' + author_name + '''
```
'''
    await message.channel.send(formatted_message)


if token is not None:
    client.run(token)
