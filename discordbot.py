import discord
import re
import random
from app import app, db
from app.models import Quote

token = app.config['DISCORD_TOKEN']
shit_pants_percent = app.config['SHIT_PANTS_PERCENT']
client = discord.Client()
mentions_regex = re.compile('<@!([0-9]*)>')


@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))


def get_user_nick_with_name_from_id(server, user_id):
    print('getting user by id {}'.format(user_id))
    user = server.get_member(user_id)
    if user is None:
        return 'Someone who isn\'t here anymore'
    return '{}'.format(user.nick, user.name)


def replace_mentions_with_nickname_for_server(server, message):
    for match in re.finditer(mentions_regex, message):
        name = get_user_nick_with_name_from_id(server, int(match.group(1)))
        message = message.replace(match.group(0), name)
    return message


def get_easter_egg_quote():
    return "So there I was, shitting my pants, and then I said"


@client.event
async def on_message(message: discord.message):
    if message.author == client.user or not message.content.startswith('!q'):
        return
    body = message.content[2:].strip()
    server = message.channel.guild
    if message.mentions:
        for mention in message.mentions:
            db.session.add(Quote(user_id=mention.id, reporter_id=message.author.id, server_id=server.id, body=body))
        db.session.commit()
        return
    # if there are no mentions, get a quote, but only from the server
    quote = random.choice(Quote.query.filter_by(server_id=server.id).all())
    quote_with_nicknames = replace_mentions_with_nickname_for_server(server, quote.body)
    should_add_shit_pants_quote = random.randint(0, 100) <= shit_pants_percent
    message_to_send = "{} {}".format(get_easter_egg_quote() if should_add_shit_pants_quote else "",
                                     quote_with_nicknames).strip()
    formatted_message = '''
```
''' + message_to_send + '''
```
'''
    await message.channel.send(formatted_message)


if token is not None:
    client.run(token)
