import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Réglage des "Timeouts"
class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = 5
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


# Réglage des "Retries"
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])

# Désactivation des mes messages d'avertissement
urllib3.disable_warnings()

# Démarrage de la session
with requests.Session() as session:
    session.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    })
    url_get = 'https://www.asos.com/fr/'
    url_get_1 = 'https://www.asos.com/fr/homme/'
    url_get_2 = 'https://my.asos.com/my-account?country=FR&keyStoreDataversion=j42uv2x-26&lang=fr-FR&nlid=nav%20header&store=FR'
    a = session.get(url_get, verify=False)
    b = session.get(url_get_1, verify=False)
    c = session.get(url_get_2, verify=False, allow_redirects=False)
    url_get_3 = c.headers['location']
    d = session.get(url_get_3, verify=False, allow_redirects=False)
    url_get_4 = d.headers['location']
    signin = url_get_4.lstrip("https://my.asos.com/identity/login?signin=")
    url_get_5 = 'https://my.asos.com/identity/register?signin=%s&checkout=False&forceAuthentication=True' % signin
    e = session.get(url_get_5, verify=False)
    RequestVerificationToken = e.cookies['__RequestVerificationToken']
    RecaptchatSiteKey = '6LdP-5AUAAAAAPO8yIXcyhOoDwJjDlUvwrwfAp_V'
    valeurs = {
        '__RequestVerificationToken': RequestVerificationToken,
        'Email': 'alexis.balayre@orange.fr',
        'FirstName': 'Alexis',
        'LastName': 'Balayre',
        'Password': 'fozwic-kApqob-2mekge',
        'BirthDay': 15,
        'BirthMonth': 5,
        'BirthYear': 2001,
        'Gender': 'F',
        'All': False,
        'Clear': False,
        'ServicePreferences[0].PreSelected': False,
        'ServicePreferences[0].PreferenceId': 'promos',
        'ServicePreferences[0].ActionText': 'Promos et soldes',
        'ServicePreferences[1].PreSelected': False,
        'ServicePreferences[1].PreferenceId': 'newness',
        'ServicePreferences[1].ActionText': 'Nouveautés',
        'ServicePreferences[2].PreSelected': False,
        'ServicePreferences[2].PreferenceId': 'lifestyle',
        'ServicePreferences[2].ActionText': 'Exclusivement pour vous',
        'ServicePreferences[3].PreSelected': False,
        'ServicePreferences[3].PreferenceId': 'partner',
        'ServicePreferences[3].ActionText': 'Partenaires ASOS',
        'RecaptchatSiteKey': RecaptchatSiteKey,
        'TermsAndConditions': True,
        'TermsAndConditions': False,
        'g-recaptcha-reponse': '',
        'submitting': 'Soumission...'
    }
    url_post = 'https://my.asos.com/identity/register?signin=%s&isCheckout=False' % signin
    f = session.post(url_post, data=valeurs)
    print(f.status_code)
    session.close()



