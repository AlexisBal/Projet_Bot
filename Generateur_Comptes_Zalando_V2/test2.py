import requests
import certifi

with requests.Session() as s:
    url_get = "https://www.zalando.fr/login/?view=register"
    headers_1 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": ""
    }
    a = s.get(url_get, headers=headers_1, cert=(certifi.where()))
    print(a.status_code)
    x_flow_id = a.headers["X-Zalando-Child-Request-Id"]
    Set_Cookie = a.headers["Set-Cookie"].rsplit("; ")
    x_xsrf_token = Set_Cookie[0].lstrip("frsx=")
    print(x_xsrf_token)
    cookies = s.cookies
    print(cookies['frsx'])
    x_zalando_client_id = Set_Cookie[4].lstrip("Secure, Zalando-Client-Id=")

    headers_2 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    url_get_2 = "https://www.zalando.fr/resources/a6c5863f92201d42d0a3ba96882c7b"
    e = s.get(url_get_2, headers=headers_2)
    print(e.status_code)

    headers_3 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    url_get_3 = "https://www.zalando.fr/api/rr/pr/sajax?flowId=ju36xvKEqGdtc9vr&try=1"
    f = s.get(url_get_3, headers=headers_3)
    print(f.status_code)

    headers_a = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Content-Length": "532",
        "x-xsrf-token": x_xsrf_token,
        "x-page-type": "/looneytunes/login/shop",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.zalando.fr",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    data_a = {
        "languageswitcher_ttmp": 1410.554999994929,
        "zds-login-page-page-interactive": 1599.419999998645,
        "primary-done": 1601.105000008829,
        "fragment-langSwitcher": 10.199999989708886,
        "fragment-tracking": 3.2749999954830855,
        "fragment-shoplogin": 65.58500000392087,
        "fragment-mask-smartbanner-fragment": 2.2299999982351437,
        "first-paint": 1409.3100000027334,
        "first-contentful-paint": 1409.3100000027334,
        "bundle-js-loaded": 1348.0249999993248,
        "bundle-js-loading-duration": 19.85499999136664,
        "zds-login-page-ttmp": 1409.3100000027334,
        "ttfb": 1258,
        "ttlb": 1262,
    }
    #url_post_a = "https://www.zalando.fr/api/cmag"
    #k = s.post(url_post_a, data=data_a, headers=headers_a)
    #print(k.status_code)
    #print(k.raise_for_status())

    headers_b = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Content-Length": "585",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.zalando.fr",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    data_b = {
        "service_name": "ingestjs",
        "events": [
            {
                "component_name": "page",
                "component_id": "_h2qHG2IZQ4XZkehaz_67",
                "event_name": "init",
                "context": {
                    "screen_resolution": "1440x900",
                    "viewport_size": "1440x821",
                    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
                    "language": "fr-FR",
                    "document_title": "Se connecter",
                    "referrer": "",
                    "location": "https://www.zalando.fr/login/?view=register",
                    "template": "/looneytunes/login/shop",
                },
                "event_number": 0,
                "flow_id": "7Vv5O8eK+MM-p35j",
                "source": "mosaic",
                "tab_id": "F9uDGHEBQb~fpNAqiAd1A",
            }
        ],
    }
    #url_post_b = "https://www.zalando.fr/api/t/i"
    #m = s.post(url_post_b, data=data_b, headers=headers_b)
    #print(m.status_code)
    #print(m.raise_for_status())

    headers_c = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Content-Length": "935",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.zalando.fr",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    data_c = {
        "service_name": "ingestjs",
        "events": [
            {
                "component_name": "mosaic",
                "component_id": "jeiE7msQhtiON9vfpucIk",
                "event_name": "client-performance-metric",
                "context": {
                    "languageswitcher_ttmp": 1410.554999994929,
                    "zds-login-page-page-interactive": 1599.419999998645,
                    "primary-done": 1601.105000008829,
                    "fragment-langSwitcher": 10.199999989708886,
                    "fragment-tracking": 3.2749999954830855,
                    "fragment-shoplogin": 65.58500000392087,
                    "fragment-mask-smartbanner-fragment": 2.2299999982351437,
                    "first-paint": 1409.3100000027334,
                    "first-contentful-paint": 1409.3100000027334,
                    "bundle-js-loaded": 1348.0249999993248,
                    "bundle-js-loading-duration": 19.85499999136664,
                    "zds-login-page-ttmp": 1409.3100000027334,
                    "ttfb": 1258,
                    "ttlb": 1262,
                    "x-page-type": "/looneytunes/login/shop",
                    "fragment_tracking_receive_timestamp": "2020-06-12T19:00:00.819Z",
                    "host": "www.zalando.fr",
                    "clientMetric": True,
                },
                "event_number": 1,
                "flow_id": "7Vv5O8eK+MM-p35j",
                "source": "mosaic",
                "tab_id": "F9uDGHEBQb~fpNAqiAd1A",
            }
        ],
    }
    #url_post_c = "https://www.zalando.fr/api/t/i"
    #w = s.post(url_post_c, data=data_c, headers=headers_c)
    #print(w.status_code)
    #print(w.raise_for_status())

    headers_d = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Content-Length": "8757",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://www.zalando.fr",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    data_d = [
        {
            "consentId": "7e011ad5657f080be90f04f927f1b8752cf85db8e4ecf3875ec4c646f0868c5a",
            "consentStatus": True,
            "dataProcessingService": "Akamai for Zalando ",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "eb30b4fc2c11f5373cd3e42857291af9a1c2795ba55b7aa5114898d49ae8c819",
            "consentStatus": True,
            "dataProcessingService": "Akamai for Zalon",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "3dd3f7ea8199f37bf4321d75a67ed3024337d3acdd486dd67c2f74686ee7b53a",
            "consentStatus": True,
            "dataProcessingService": "AWIN for Zalando Lounge",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "ecbfbd80cc186d4b4f6c7a12507e92a4a0136a887bbc26b413efd17764effd43",
            "consentStatus": True,
            "dataProcessingService": "BootstrapCDN for Zalando Outlet",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "bd9845ae6d447c21d7cecf13dd0f72f702bce218c321e8ad813c6d49ea6bcc94",
            "consentStatus": True,
            "dataProcessingService": "branch.io Pixel for Zalando Lounge",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "2f1a3f22ac6e1f24431547084b19513a656a53732949845443fe27e36dfbe99f",
            "consentStatus": True,
            "dataProcessingService": "Creative Factory for Zalando",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "b8d490830cb86ea15cc2ff8e21acd8043798a3d92ef79f0f6cd453faa2ee0a28",
            "consentStatus": True,
            "dataProcessingService": "Device Ident for Zalando",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "e33c25eadeb6e3a319c814084877917dbfb0a6d4dbc46d8d9b7a8dd3e32acf00",
            "consentStatus": True,
            "dataProcessingService": "Facebook Pixel for Lounge",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "faddfcc445f5743fd8693318196f3aa6502e7093e3ac409a233f2e69be13656d",
            "consentStatus": True,
            "dataProcessingService": "Facebook Pixel for Zalando",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "64f84cc6a0b6aeb9ff17afa0fe88e2ad343ae6283e68dedc08535556499dbac9",
            "consentStatus": True,
            "dataProcessingService": "Facebook Pixel for Zalando Outlet",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "2811b34269632efa7d53855657863a10bb38ff8f1b94703617d4d157b0a6f3be",
            "consentStatus": True,
            "dataProcessingService": "Facebook Pixel for Zalon",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "56165a1a48de3eab04a362c27d34e4645dbca4a88c7526f76f68244743e767ab",
            "consentStatus": True,
            "dataProcessingService": "Facebook Pixel for ZMS",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "c9b000a06a9b432c46cac87f9f8f47e51f04a0dcda48bda8362562c8fc3e84c3",
            "consentStatus": True,
            "dataProcessingService": "FontAwesome for Zalando Outlet",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
        {
            "consentId": "8757d10c199086e0f207f251dc3382590225ff5f14ca6eca67aaff63e7b64a56",
            "consentStatus": True,
            "dataProcessingService": "fonts.net for Zalando Outlet",
            "action": "onAcceptAllBtnClick",
            "language": "en",
        },
        {
            "consentId": "e399071f3d1fb4f268d1b15984fe6ae2463d1ade05a443842a69ba42f5705982",
            "consentStatus": True,
            "dataProcessingService": "Google Ads for Zalando",
            "action": "onAcceptAllBtnClick",
            "language": "fr",
        },
    ]
    #url_post_d = "https://www.zalando.fr/api/consents"
    #x = s.post(url_post_d, data=data_d, headers=headers_d)
    #print(x.status_code)

    sensor_data = {
        "sensor_data": "7a74G7m23Vrp0o5c9173031.54-1,2,-94,-100,Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362,"
        "uaend,12083,20030107,fr-FR,Gecko,1,0,0,0,391686,3056866,1280,680,1280,720,463,607,1295,,"
        "cpen:0,i1:0,dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:0,bat:0,x11:0,x12:1,9181,"
        "0.0117028775,795956630770,loc:-1,2,-94,-101,do_en,dm_en,t_dis-1,2,-94,-105,0,-1,0,0,1063,"
        "1884,0;0,-1,0,0,908,1768,0;0,1,0,0,981,1435,0;1,-1,0,0,2177,1798,0;-1,2,-94,-102,0,-1,0,0,"
        "972,1884,1;0,-1,0,0,925,1768,1;0,1,0,0,986,1435,1;1,-1,0,0,1995,1798,1;-1,2,-94,-108,-1,2,"
        "-94,-110,0,4,117,369,1226,-1;1,2,117,369,1226,-1;2,1,4892,374,1220;3,1,4900,393,1207;4,1,"
        "4906,409,1197;5,1,4913,428,1187;6,1,4921,480,1167;7,1,4929,521,1154;8,1,4936,539,1146;9,1,"
        "4942,623,1117;10,1,123816,545,1441;11,1,123822,572,1412;12,1,123829,605,1384;13,1,123838,620,"
        "1374;14,1,123844,632,1363;15,1,257501,521,1413;16,1,257508,520,1383;17,1,257515,516,1320;18,"
        "1,257522,513,1294;19,1,257530,509,1213;20,1,257537,505,1174;21,1,257545,501,1097;22,1,257552,"
        "496,1066;23,1,257560,496,1033;24,1,257567,496,993;25,1,257575,497,979;26,1,257582,497,967;27,"
        "1,257590,500,951;28,1,257597,503,939;29,1,257604,505,933;30,1,257612,507,927;31,1,257619,509,"
        "923;32,1,257626,511,920;33,1,257634,515,916;34,1,257643,527,909;35,1,257648,537,905;36,1,"
        "257659,548,904;37,1,257664,559,905;38,1,257671,578,907;39,1,257679,613,917;40,1,257686,627,"
        "922;41,1,298100,516,988;42,3,298110,516,988,-1;43,4,298230,516,986,-1;44,1,299551,557,874;45,"
        "3,299559,557,874,-1;46,4,299751,557,873,-1;47,1,300828,584,693;48,3,300837,584,693,-1;49,4,"
        "300989,584,693,-1;50,1,327987,643,409;51,1,327994,633,407;52,1,328001,626,405;53,1,328009,"
        "620,401;54,1,328016,615,399;55,1,328373,605,381;56,1,328381,599,372;57,1,328389,595,366;58,1,"
        "328395,589,357;59,1,328403,585,349;60,1,328410,579,339;61,1,328418,575,330;62,1,328425,571,"
        "321;63,1,328434,568,313;64,1,328440,565,305;65,1,328447,563,301;66,1,328455,559,292;67,1,"
        "328462,555,283;68,1,328470,552,271;69,1,328477,549,265;70,1,328484,547,260;71,1,328493,547,"
        "255;72,1,328501,547,254;73,1,328507,546,253;74,1,328514,546,252;75,1,328521,546,251;76,1,"
        "328529,546,251;77,1,328596,546,250;78,1,328604,546,249;79,1,328611,547,249;80,1,328619,550,"
        "249;81,1,328625,553,249;82,1,328635,557,252;83,1,328640,561,255;84,1,328650,563,257;85,1,"
        "328656,569,262;86,1,328663,571,265;87,1,328671,573,267;88,1,328678,577,271;89,1,328686,578,"
        "272;90,1,328692,579,273;91,1,328701,581,275;92,1,328708,581,275;93,1,328716,583,277;94,1,"
        "328722,583,277;95,1,328827,583,276;96,1,328835,583,273;97,1,328842,581,267;98,1,328851,579,"
        "263;99,1,328856,578,257;100,1,328864,576,254;101,1,328872,574,249;102,1,328879,572,247;103,1,"
        "328886,569,243;104,1,328894,565,239;105,1,340013,486,243;106,1,340013,486,243;107,1,340019,"
        "493,251;202,3,588503,895,479,-1,3;203,4,588555,895,479,-1,3;373,3,626799,242,1219,-1;374,4,"
        "627004,242,1219,-1;375,2,627005,242,1219,-1;557,3,921516,98,790,2366;558,4,921569,98,790,"
        "-1;560,3,929901,301,989,-1;561,4,929945,301,991,-1;563,3,938238,303,1186,-1;564,4,938317,303,"
        "1186,-1;565,2,938317,302,1186,-1;713,3,953189,346,1187,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,"
        "-94,-109,-1,2,-94,-114,1,3,298104,516,988;2,3,299552,556,874;3,3,300828,584,692;8,3,921512,"
        "98,790;9,3,929896,300,989;10,3,938233,302,1186;11,4,938317,302,1186;-1,2,-94,-103,3,2;2,"
        "9184;3,289774;2,292219;3,298101;2,302593;0,329903;1,339495;3,339547;2,339568;3,587988;2,"
        "630264;3,921510;2,923091;3,929894;2,934467;3,938233;2,948238;-1,2,-94,-112,"
        "https://www.zalando.fr/login/?view=register-1,2,-94,-115,1,39830069,32,0,0,4635871,44465908,"
        "953189,0,1591913261540,13,17029,0,714,2838,13,0,953191,48007072,1,"
        "70769C98B687B487EDB11AA876284490~-1~YAAQH3IRAkV4lpNyAQAADVx6pQQUjelrjmwRAe5bNDiLKh8PH+EI7lpuI"
        "+71UJ/j7niXkW90ZCQ9Oek6zv5CaX6+R2ANBcj4qQobgIP8fnA/a/JoOHQ"
        "/F7LEiUv0rTRig78FZtB1tfAH02lSej2Dtj6wGp/pXCJ4RWgR9YTZft0lE1gKhqxP6qaZgUPyN38JnSyWrqSsAfqve"
        "/ce1nm96vo/+d51AQ0R5c/XRDx+68E8rQbdF7yHaS0XEE5Sv5EjHtX3akEFs/I0Kg9fBwquT9QKl6QqG9AtZ"
        "/oDT2w8X7SVhKe+SpgYGjv2gMvM9/F+SKxFSh5MR0X8pls466RX4WE8gVM=~-1~-1~-1,31303,864,-119753953,"
        "27074993-1,2,-94,-106,1,15-1,2,-94,-119,20,60,40,60,80,40,20,40,20,20,20,260,280,80,-1,2,-94,"
        "-122,0,0,0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,-1,2,-94,-70,"
        "-359992563;-1439556030;dis;,23;true;true;true;-120;true;24;24;true;true;-1-1,2,-94,-80,"
        "5499-1,2,-94,-116,27511667-1,2,-94,-118,233033-1,2,-94,-121,;4;7;0 "
    }
    url_post1 = "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
    headers_4 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    c = s.post(url_post1, data=sensor_data, headers=headers_4)
    print(c.status_code)

    sensor_data_bis = {
        "sensor_data": "7a74G7m23Vrp0o5c9174241.54-1,2,-94,-100,Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36,uaend,12147,"
        "20030107,fr-FR,Gecko,3,0,0,0,391704,8399265,1440,900,1440,900,1440,821,1440,,cpen:0,i1:0,"
        "dm:0,cwen:0,non:1,opc:0,fc:0,sc:0,wrc:1,isc:0,vib:1,bat:1,x11:0,x12:1,8921,0.571005954285,"
        "795994199646,loc:-1,2,-94,-101,do_en,dm_en,t_en-1,2,-94,-105,0,-1,0,0,954,1884,0;0,-1,0,0,"
        "1041,1768,0;0,1,0,0,927,1435,0;1,-1,0,0,2091,1798,0;-1,2,-94,-102,0,-1,0,0,990,1884,1;0,-1,0,"
        "0,1031,1768,1;0,1,0,0,995,1435,1;1,-1,0,0,2037,1798,1;-1,2,-94,-108,0,1,3951,undefined,0,0,"
        "-1;1,2,3969,undefined,0,0,-1;2,1,3970,undefined,0,0,-1;3,2,3978,undefined,0,0,-1;4,1,5827,-2,"
        "0,0,1884;5,3,5828,-2,0,0,1884;6,2,5881,-2,0,0,1884;7,1,6246,-2,0,0,1884;8,3,6246,-2,0,0,"
        "1884;9,2,6321,-2,0,0,1884;10,1,6420,-2,0,0,1884;11,3,6420,-2,0,0,1884;12,2,6503,-2,0,0,"
        "1884;13,1,7712,-2,0,0,1768;14,3,7712,-2,0,0,1768;15,2,7796,-2,0,0,1768;16,1,7815,-2,0,0,"
        "1768;17,3,7815,-2,0,0,1768;18,2,7896,-2,0,0,1768;19,1,7910,-2,0,0,1768;20,3,7911,-2,0,0,"
        "1768;21,1,8031,-2,0,0,1768;22,3,8031,-2,0,0,1768;23,2,8082,-2,0,0,1768;24,2,8094,-2,0,0,"
        "1768;25,1,11003,8,0,0,1435;26,2,11112,8,0,0,1435;27,1,11329,-3,0,0,1435;28,2,11468,-3,0,0,"
        "1435;29,1,11618,8,0,0,1435;30,2,11713,8,0,0,1435;31,1,12274,-2,0,0,1435;32,3,12274,-2,0,0,"
        "1435;33,2,12333,-2,0,0,1435;34,1,12667,-2,0,0,1435;35,3,12667,-2,0,0,1435;36,2,12742,-2,0,0,"
        "1435;37,1,12833,-2,0,0,1435;38,3,12834,-2,0,0,1435;39,2,12922,-2,0,0,1435;40,1,13161,-2,0,0,"
        "1435;41,3,13162,-2,0,0,1435;42,2,13253,-2,0,0,1435;43,1,13277,-2,0,0,1435;44,3,13277,-2,0,0,"
        "1435;45,2,13355,-2,0,0,1435;46,1,13373,-2,0,0,1435;47,3,13373,-2,0,0,1435;48,1,13500,-2,0,0,"
        "1435;49,3,13501,-2,0,0,1435;50,2,13526,-2,0,0,1435;51,2,13568,-2,0,0,1435;52,1,16691,-3,0,0,"
        "1435;53,2,16838,-3,0,0,1435;54,1,17016,8,0,0,1435;55,2,17119,8,0,0,1435;56,1,17221,8,0,0,"
        "1435;57,2,17292,8,0,0,1435;58,1,17368,8,0,0,1435;59,2,17447,8,0,0,1435;60,1,17495,8,0,0,"
        "1435;61,2,17571,8,0,0,1435;62,1,17623,8,0,0,1435;63,2,17708,8,0,0,1435;64,1,18327,-2,0,0,"
        "1435;65,3,18328,-2,0,0,1435;66,1,18398,-2,0,0,1435;67,3,18399,-2,0,0,1435;68,2,18409,-2,0,0,"
        "1435;69,2,18478,-2,0,0,1435;70,1,18584,-2,0,0,1435;71,3,18584,-2,0,0,1435;72,1,18619,-2,0,0,"
        "1435;73,3,18620,-2,0,0,1435;74,2,18663,-2,0,0,1435;75,2,18683,-2,0,0,1435;76,1,20599,-2,0,0,"
        "1435;77,3,20600,-2,0,0,1435;78,1,20701,-2,0,0,1435;79,3,20701,-2,0,0,1435;80,2,20709,-2,0,0,"
        "1435;81,2,20790,-2,0,0,1435;82,1,20845,-2,0,0,1435;83,3,20846,-2,0,0,1435;84,2,20937,-2,0,0,"
        "1435;85,1,21070,-2,0,0,1435;86,3,21070,-2,0,0,1435;87,2,21171,-2,0,0,1435;88,1,21175,-2,0,0,"
        "1435;89,3,21175,-2,0,0,1435;90,2,21235,-2,0,0,1435;91,1,21321,-2,0,0,1435;92,3,21322,-2,0,0,"
        "1435;93,2,21393,-2,0,0,1435;94,1,21726,16,0,8,1435;95,1,22555,-2,0,8,1435;96,3,22555,-2,0,8,"
        "1435;97,2,22630,-2,0,8,1435;98,2,22727,16,0,0,1435;99,1,22861,-2,0,0,1435;100,3,22861,-2,0,0,"
        "1435;101,2,22928,-2,0,0,1435;102,1,22955,-2,0,0,1435;103,3,22956,-2,0,0,1435;104,2,23055,-2,"
        "0,0,1435;105,1,23148,-2,0,0,1435;106,3,23148,-2,0,0,1435;107,1,23203,-2,0,0,1435;108,3,23204,"
        "-2,0,0,1435;109,2,23217,-2,0,0,1435;110,2,23271,-2,0,0,1435;111,1,23433,-2,0,0,1435;112,3,"
        "23434,-2,0,0,1435;113,2,23509,-2,0,0,1435;114,1,23661,-2,0,0,1435;115,3,23661,-2,0,0,"
        "1435;116,2,23748,-2,0,0,1435;117,1,23793,-2,0,0,1435;118,3,23794,-2,0,0,1435;119,2,23881,-2,"
        "0,0,1435;120,1,25872,8,0,0,1435;121,2,25943,8,0,0,1435;122,1,27353,8,0,0,1435;123,2,27444,8,"
        "0,0,1435;124,1,27515,8,0,0,1435;125,2,27601,8,0,0,1435;126,1,27669,8,0,0,1435;127,2,27756,8,"
        "0,0,1435;128,1,28221,-2,0,0,1435;129,3,28222,-2,0,0,1435;130,2,28321,-2,0,0,1435;131,1,28400,"
        "-2,0,0,1435;132,3,28401,-2,0,0,1435;133,2,28484,-2,0,0,1435;134,1,29185,16,0,8,1798;135,1,"
        "29539,-2,0,8,1798;136,3,29539,-2,0,8,1798;137,2,29602,-2,0,8,1798;138,2,29735,16,0,0,"
        "1798;139,1,29884,-2,0,0,1798;140,3,29884,-2,0,0,1798;141,2,29959,-2,0,0,1798;142,1,30132,-2,"
        "0,0,1798;143,3,30132,-2,0,0,1798;144,2,30215,-2,0,0,1798;145,1,30244,-2,0,0,1798;146,3,30245,"
        "-2,0,0,1798;147,1,30623,16,0,8,1798;148,2,31438,16,0,0,1798;-1,2,-94,-110,0,1,2723,681,535;1,"
        "1,2726,698,552;2,1,2745,727,584;3,1,2765,746,606;4,1,2776,758,618;5,1,2832,788,657;6,1,2845,"
        "788,666;7,1,2886,783,713;8,1,3329,777,171;9,1,3347,769,170;10,1,3364,766,173;11,1,3499,704,"
        "304;12,1,3502,699,340;13,1,3510,698,346;14,1,3527,695,361;15,1,3544,694,371;16,1,3562,693,"
        "376;17,1,3577,692,378;18,1,3596,691,378;19,1,3610,690,379;20,1,3627,688,378;21,1,3646,686,"
        "376;22,1,3661,682,375;23,1,3677,682,375;24,1,3693,679,376;25,1,3710,677,376;26,1,3734,671,"
        "385;27,1,3743,670,386;28,1,3760,668,389;29,1,3776,665,391;30,1,3793,664,394;31,1,3810,661,"
        "396;32,1,3826,660,398;33,1,3857,658,400;34,1,3863,657,400;35,1,3894,656,402;36,1,3914,655,"
        "402;37,1,3928,655,403;38,1,3943,654,403;39,3,3979,654,403,1884;40,1,3988,654,403;41,4,4062,"
        "654,403,1884;42,2,4068,654,403,1884;43,1,6789,654,404;44,1,6801,651,416;45,1,6817,649,429;46,"
        "1,6833,649,439;47,1,6851,649,447;48,1,6867,649,456;49,1,6884,650,465;50,1,6900,651,470;51,1,"
        "6917,652,472;52,1,6933,652,473;53,1,6949,652,473;54,1,6967,652,474;55,1,6989,652,474;56,1,"
        "7034,652,474;57,1,7052,650,475;58,1,7067,647,478;59,1,7085,646,478;60,1,7100,644,482;61,1,"
        "7116,643,483;62,1,7134,642,484;63,3,7146,642,484,1768;64,1,7157,641,484;65,4,7282,641,484,"
        "1768;66,2,7287,641,484,1768;67,1,7305,641,484;68,1,8516,642,484;69,1,8536,658,484;70,1,8551,"
        "675,487;71,1,8567,688,496;72,1,8588,713,526;73,1,8601,717,535;74,1,8619,720,556;75,1,8636,"
        "720,585;76,1,8651,718,605;77,1,8667,717,624;78,1,8684,717,647;79,1,8700,717,658;80,1,8716,"
        "716,670;81,1,8733,713,677;82,1,8752,710,680;83,1,8767,708,682;84,1,8786,705,684;85,1,8802,"
        "704,684;86,1,8819,703,685;87,1,8833,703,685;88,1,8852,703,684;89,1,8868,702,681;90,1,8885,"
        "702,674;91,1,8900,702,670;92,1,8916,702,667;93,1,8934,704,665;94,1,8949,705,663;95,1,8967,"
        "705,663;96,1,8983,706,663;97,1,9000,706,663;98,1,9023,706,662;99,1,9037,706,662;100,1,9053,"
        "706,662;101,1,9069,704,661;102,1,9085,699,659;103,1,9101,694,658;104,1,9117,686,657;105,1,"
        "9134,671,657;155,3,10069,613,653,1435;169,4,10512,286,643,-1;170,2,10515,286,643,-1;289,3,"
        "16039,621,658,1435;290,4,16142,621,658,1435;291,2,16147,621,658,1435;332,3,19735,567,656,"
        "1435;341,4,19969,331,656,-1;342,2,19973,331,656,-1;410,3,25445,618,657,1435;411,4,25581,618,"
        "657,1435;412,2,25585,618,657,1435;446,3,26979,706,659,1435;447,4,27084,706,659,1435;448,2,"
        "27088,706,659,1435;470,3,28827,698,736,1798;481,4,29069,-1,-1,-1;482,2,29072,-1,-1,-1;518,3,"
        "35067,689,1129,-1;-1,2,-94,-117,-1,2,-94,-111,-1,2,-94,-109,-1,2,-94,-114,-1,2,-94,-103,-1,2,"
        "-94,-112,https://www.zalando.fr/login/?view=register-1,2,-94,-115,NaN,1241948,32,0,0,0,NaN,"
        "35067,0,1591988399292,26,17030,149,519,2838,17,0,35071,3836867,0,"
        "B94B13408752796D9FA179CAE9B326F7~-1"
        "~YAAQtnIRAmAASppyAQAAA57nqQTTWkwggemyrCGrLGH6zIX9UVCPmrn8h2QUAUEj0lF29rBPzgtrr3jj5UR+sGK"
        "+yWtwHgK5PKrEczsUuy0vU4y4VqSql0liKBYIFZt3nczVvU/bk7MZGowQRAMx86YP4IE0jN8oqp+/2hnEhuzz1v"
        "/F1LmsrorvI+dkHwlJxvr1PtQztbz6t7Lu2VUZTzWjPiXOd6Cqf9FjpxbIYw"
        "+X4vRWL7hx1pGMG3TVz6Af5FBrUD52TihdEmqVEDfspLjDmsTcsrm+ukW8T7IxqPymb"
        "+6ciaUHfV7AoPBUPHdRkdThHLdjoBII1qsbNTApP0/BUIY=~-1~-1~-1,33155,954,-2009515897,30261693-1,2,"
        "-94,-106,1,11-1,2,-94,-119,58,64,63,93,103,132,92,47,12,9,9,1667,1915,510,-1,2,-94,-122,0,0,"
        "0,0,1,0,0-1,2,-94,-123,-1,2,-94,-124,-1,2,-94,-126,-1,2,-94,-127,11321144241322243122-1,2,"
        "-94,-70,-36060876;-1849314799;dis;,7,8;true;true;true;-120;true;30;30;true;false;-1-1,2,-94,"
        "-80,5578-1,2,-94,-116,8399281-1,2,-94,-118,386880-1,2,-94,-121,;10;31;0 "
    }
    url_post1_bis = "https://www.zalando.fr/resources/a6c5863f921840dbe8f36578d86f32"
    headers_4_bis = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
    }
    c_bis = s.post(url_post1_bis, data=sensor_data_bis, headers=headers_4_bis)
    print(c_bis.status_code)

    url_get2 = "https://www.zalando.fr/api/reef/register/schema"
    headers_5 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "x-xsrf-token": x_xsrf_token,
        "x-zalando-render-page-uri": "/login/?view=register",
        "x-zalando-client-id": x_zalando_client_id,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-zalando-request-uri": "/login/?view=register",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "x-flow-id": x_flow_id,
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
        "If-None-Match": 'W / "72a-kWB4XOWPPX4CDJaawJqhJ8/Dvdc"',
    }
    b = s.get(url_get2, headers=headers_5)
    print(b.status_code)

    register = {
        "newCustomerData": {
            "accepts_terms_and_conditions": "true",
            "date_of_birth": "",
            "email": "benjamain.balayre@isep.fr",
            "fashion_preference": [],
            "firstname": "alexis",
            "lastname": "balayre",
            "password": "Dubai007",
            "subscribe_to_news_letter": False
        },
        "wnaMode": "shop"
    }
    url_post2 = "https://www.zalando.fr/api/reef/register"
    headers_6 = {
        "Host": "www.zalando.fr",
        "Connection": "keep-alive",
        "Content-Length": "241",
        "x-xsrf-token": x_xsrf_token,
        "x-zalando-render-page-uri": "/login/?view=register",
        "x-zalando-client-id": x_zalando_client_id,
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-zalando-request-uri": "/login/?view=register",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "x-flow-id": x_flow_id,
        "Origin": "https://www.zalando.fr",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.zalando.fr/login/?view=register",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "Zalando-Client-Id=b1df7ae2-413a-47c3-8fef-f8eddd7810b4; _ga=GA1.2.664290401.1591967248; _ga=GA1.2.664290401.1591967248; _gid=GA1.2.1312755635.1591967250; frsx=AAAAAD-SjMUG4tP5bhKC-XQ0JqV83Sb5oFGDBp0QqF2FQ56WA4m_AJjN_fzumzi8UjG2H--LY6OSVtGYYKoaUvKKYbMd-uf6CwR0NQXA96D-E3OYK3KZLap8wTnCJhpkJ8cEGerNdkYXGqhSyCclys8=; bm_sz=F7C0BB69337BED4B888F4132708471B2~YAAQL+57XJuJLKdyAQAAGWm7qQghX01ytvpSiNUPFBXXlMx9zoj3qJZUtsRMb7ii7BYOeZMAHqxhvcrQCAG7w5cD8TD1D5QAaY7hpPGJhxcTB8hXi1pBvQoJq6zqxmBmgOzeYjw1peZBYhabqTTZmEDW554KbtiWHUcg2asphrU6vfyh1x+qiuu0UEc1z85G; ak_bmsc=4422E901871FDA669DA2446E478055515C7BEE2F9B3D00007BC5E35E8D031673~plf/SeYXVoJanwUYXSBvgy6wmvVBJt8TqIC4MhvfwStiwziusQNTIFtzHpLX+Qyzi0hBkVZc/fLvlfLSN/QDqumh0uOguPfliZnYiUpoCPcaEdLT3uLOXDzQGYnGCmz3mDu8+X0wAQb7y+0UG4LOkn62w+n23v55UsGPYkbDOsbhfbO6OKyanLK8/PG/vxiBXzgrKLsjpftHJmrkPhcVE/DQWHqjLspiB9W1AjFqsXxUVxLJKnuI8U9zrmA+oEnjKp; _abck=B94B13408752796D9FA179CAE9B326F7~-1~YAAQXO57XPdpSINyAQAAW07EqQTDYE//4sIeq6V7Sgh6PUCBojb/x0/UuKUbLfgzLxogK2Vio3+s4LXUz8GS5PIL1vFWSZf1gXFj5cLqt4Nn3hHsM2hkbaNe7d44Mfb3oFrPjIEFsuN1I2TY4qjjq/CV3qvmBRuzjW3DSq1rLV2qfb1RQjbiIGhfTVKG1sBZtRtnJk360X/GBzlc6RcUZLYMy59h/WJdVdjspZv/ZPnJim41NAfxk8qheBki3Xx6KJgqAxYlPAynCyh+uZZOXW6aKHBZV4zzHG9Zcb1ZMkoCXP32dWJR+/bfIhGJVVhEykcUcEwhRh7njn1ybmXywiLsEao=~-1~-1~-1",
        "If-None-Match": 'W / "72a-kWB4XOWPPX4CDJaawJqhJ8/Dvdc"',
    }
    s.close()

    #n = s.post(url_post2, data=json.dumps(register), headers=headers_6, allow_redirects=True)
    #print(n.status_code)


