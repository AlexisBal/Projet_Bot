from discord_webhook import DiscordWebhook, DiscordEmbed
import urllib3


def ManualCheckout():
    # Désactivation des messages d'avertissement
    urllib3.disable_warnings()

    # Identifiants Discord Webhook
    webhook = DiscordWebhook(
        url='https://discordapp.com/api/webhooks/734518655043371120/5vLoCDUaInsAFhVr5MkjaVTOinMmh4GlpqCy3IipI6HgiCsbC5KNfUj86Tj5b7R5XwWT',
        username="Scred AIO",
        avatar_url='https://pbs.twimg.com/profile_images/1283768710138863617/D2yC8Qpg_400x400.jpg',
        verify=False,
        proxies={
            'http': 'http://ym7Y:ahpdkK@45.81.248.235:3128/'
        }
    )
    # Titre
    embed = DiscordEmbed(title='Successfully checked out !', color=1160473)
    # Pied de page
    embed.set_footer(text='SCRED AIO')
    embed.set_timestamp()
    # Photo du produit
    embed.set_thumbnail(url='https://img01.ztat.net/article/NI/11/2O/08/WQ/11/NI112O08W-Q11@8.jpg?imwidth=1800&filter=packshot')
    embed.add_embed_field(name='Website', value='Zalando.fr', inline=False)
    embed.add_embed_field(name='Product', value='AIR MAX 200', inline=False)
    embed.add_embed_field(name='Size', value='5')
    embed.add_embed_field(name='Mode', value='Manual')
    embed.add_embed_field(name='Checkout Speed', value='6.33')
    embed.add_embed_field(name='Checkout Link', value='https://www.paypal.com/cgi-bin/webscr?cmd=_express-checkout&useraction=commit&token=EC-1RL7475223748615G', incline=False)

    webhook.add_embed(embed)
    response = webhook.execute()


ManualCheckout()