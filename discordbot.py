import discord
import re
import random
from app import app, db
from app.models import User, Quote

token = app.config['DISCORD_TOKEN']
shit_pants_percent = app.config['SHIT_PANTS_PERCENT']
print(token)
client = discord.Client()


def find_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def create_user(user_id):
    user = User(id=user_id)
    db.session.add(user)
    db.session.commit()
    return user


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


@client.event
async def on_message(message: discord.message):
    if message.author == client.user or not message.content.startswith('!q'):
        return
    reporter = find_user_by_id(message.author.id)
    if reporter is None:
        reporter = create_user(message.author.id)
    if message.mentions:
        body = re.sub('<@![0-9]*>', '', message.content[2:]).strip()
        for mention in message.mentions:
            author = find_user_by_id(mention.id)
            if author is None:
                author = create_user(mention.id)
            db.session.add(Quote(user_id=author.id, reporter_id=reporter.id, body=body))
        db.session.commit()
        return
    # if there are no mentions, get a quote
    quote = random.choice(Quote.query.all())
    should_add_shit_pants_quote = random.randint(0, 100) <= shit_pants_percent
    author = await client.fetch_user(quote.user_id)
    message_to_send = quote.body + ' and then I shit my only pair of pants. I swear to god I did.' if should_add_shit_pants_quote else quote.body
    formatted_message = '''
```
''' + message_to_send + '''
- @''' + author.name + '''
```
'''
    await message.channel.send(formatted_message)


if token is not None:
    client.run(token)
