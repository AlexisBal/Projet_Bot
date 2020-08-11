import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from user_agent import generate_user_agent
import requests.auth
import urllib3
import json


class HTTPProxyDigestAuth(requests.auth.HTTPDigestAuth):
    def handle_407(self, r):
        """Takes the given response and tries digest-auth, if needed."""

        num_407_calls = r.request.hooks['response'].count(self.handle_407)

        s_auth = r.headers.get('Proxy-authenticate', '')

        if 'digest' in s_auth.lower() and num_407_calls < 2:

            self.chal = requests.auth.parse_dict_header(s_auth.replace('Digest ', ''))

            # Consume content and release the original connection
            # to allow our new request to reuse the same one.
            r.content
            r.raw.release_conn()

            r.request.headers['Authorization'] = self.build_digest_header(r.request.method, r.request.url)
            r.request.send(anyway=True)
            _r = r.request.response
            _r.history.append(r)

            return _r

        return r

    def __call__(self, r):
        if self.last_nonce:
            r.headers['Proxy-Authorization'] = self.build_digest_header(r.method, r.url)
        r.register_hook('response', self.handle_407)
        return r


def VerificationProxys():
    try:
        # Ouverture de la session
        s = requests.Session()
        s.trust_env = False
        s.proxies = {
            "http": "http://@",
            "https": "http://lum-customer-hl_eae231f1-zone-zalando_fr-unblocker:0c8voa6qm6rn@zproxy.lum-superproxy.io:22225"
        }
        # Url Test IP
        url_test = 'https://www.zalando.fr'
        url_test2 = 'https://www.zalando.fr/login/?view=login'
        url3 = 'https://httpbin.org/ip'
        # Test du proxy
        s.headers = {"User-Agent": generate_user_agent(),
                     'Connection': 'keep-alive',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                     'Accept-Language': 'fr-fr',
                     'Accept-Encoding': 'gzip, deflate, br'
                     }
        s.get(url_test, verify=False)
        s.get(url_test2, verify=False)
        iptest = s.get(url3, verify=False)
        # Affichage du résultat
        print(s.headers)
        print(s.cookies)
        print(iptest.json())
        s.close()

    # Gestion des exceptions
    except:
        raise


urllib3.disable_warnings()
VerificationProxys()
