from discord_webhook import DiscordWebhook, DiscordEmbed


def ManualCheckout():
    # Identifiants Discord Webhook
    webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/734518655043371120/5vLoCDUaInsAFhVr5MkjaVTOinMmh4GlpqCy3IipI6HgiCsbC5KNfUj86Tj5b7R5XwWT', username="Scred AIO")
    # Titre
    embed = DiscordEmbed(title='SUCCESSFUL CHECKOUT', color=242424)
    # Pied de page
    embed.set_footer(text='SCRED AIO')
    embed.set_timestamp()
    # Photo du produit
    embed.set_thumbnail(url='https://img01.ztat.net/article/NI/11/2O/08/WQ/11/NI112O08W-Q11@8.jpg?imwidth=1800&filter=packshot')
    embed.add_embed_field(name='Website', value='Zalando.fr', incline=False)
    embed.add_embed_field(name='Product', value='AIR MAX 200', incline=False)
    embed.add_embed_field(name='Size', value='5')
    embed.add_embed_field(name='Mode', value='Manual')
    embed.add_embed_field(name='Checkout Speed', value='6.33')
    embed.add_embed_field(name='Checkout Link', value='https://www.paypal.com/authflow/twofactor/?returnUri=webapps%2Fhermes&state=flow%3D1-P%26ulReturn%3Dtrue%26token%3DEC-3PY31626XR726971C%26useraction%3Dcommit%26ctngcyReturn%3Dtrue&onFail=return&country.x=FR&locale.x=fr_FR&nonce=2020-07-17T10%3A36%3A33ZBevcRhncpmNuc9fwQYwkbNy6pP50uAO3dlz-zsjmoME&stsReturnUrl=https%3A%2F%2Fwww.paypal.com%2Fcheckoutnow%2F2&mkey=authContext:eb6766fa50234f79a7d898f7ef3bd292', incline=False)

    webhook.add_embed(embed)
    response = webhook.execute()


ManualCheckout()