import requests  # Needed for making HTTP requests
import time  # Needed to generate the OAuth timestamp
import urllib.parse  # Needed to URLencode the parameter string
from base64 import b64encode  # Needed for create_signature function
import hmac  # Needed for create_signature function
import hashlib  # Needed for create_signature functionx
import binascii  # Needed for create_signature function

grant_type = 'client_credentials'
oauth_consumer_key = '49a0eb8a-7d6b-43ad-a592-c17ec12ccdac'  # From credentials.properties file
access_key_secret = 'AAAAALhPeZjCpOfuXeQwReT3TDxRyLZsULPzElThR1e1co26LLv98jm57ykr1F-lJ7SmiuES_jlRL30xQhS2pYpzbx-B8QttHR0rUfmI1PlPWUpYPOclJ9grQm7v77hOyiMMuCz-gxLH_eGjKOVm-rYGIqs2Ovu5_6jLC5aKt0hbz7Ou5ha7u0TUMJmAMqrgjiyAM34LWH08-DRrTKaPWCOLbf9E1UER6E04QOQwIyibRabtprIMSG-_8iWdqtJefkUxhGLkyb-SDgRU8hxyDret0pe2MbJY0PgG7UvOTjyOVO5gYfancsmts1CcA8eStRY5pcQdA-lPm0mxTVxi6fdgmr1ExyI6RjJWWuRh9IAU5WQpFKRqT6bY7UOLhBcJrz2E79P-g4jl6nbQAj1mnlylFKvppNqPsdSyGpOqcUPGuAcdD8aJ7_-oCDXf5N7p4B4Y2Pdw3FO_CI5D6gFdnJtPS8ET-MsKi81L-Y_y--ey89K3MuTNZkM34OJlV8NP6PSB3TxUFplKFfs2CUwRmNCLVJ7jdiowiMtFquGykaWzu3D0CoDEJ31YOfo6ZF2DaNY34K34OUH4DWWhaEqjCLXNaqZXplGJpiIdkKjEaM-e6fWJlvUoW8VbxhweBQpoJDA1i3SSDpKSeW2p7GA_xrnXC-zm6iIukYRz5ZmKAJtvMSVPJ0YIihF_UzGU_GRzC7LCSJ3-GUnqgwJQaGKDzEp066Slef8pEhrNX2WFEQVt3PjWWCEfo3iqQ5t6OuY-v-H-mMKkKWhaZIl3RYSS1lua5ozY9yJvsOJJeiqGTxGvVVNDd_HNa1WFeZAH1WlUSi7VM7Lif2fNrplbh2kdopPCsQnD8qcvEzyC-XlLn0I69WpKDc8nsj_QjAY6a99fRN8ILWcODr71xeTR_6gKmSw7caH_p_XHnNSB730BSCSvra6U9Xts2SiZ_ViZFh_X4PcEJUnsb4jENSuA_3TyRV2wXabic7SftDmftuuQ15Agl3HF_H0ufd314UMwuBQ65hfR9JYKpTqCKm0A9LbzyuLrbkG8f89KS6t5bkWRxIb433L5BikOXeu3o8wPkGsCmSAZpI92p_F3EUehJDUyrHZVpi3hqSRXhjkUMyLU9xQrS3wsNSQr_ZbumPxqPcaavisNaP4phg_L-yjldmvrYuxVTOTy6NhR8GWvbe9hDH79wVu5QGfm9n-aZQLVSUAe6imnHCRJxPpxuOk='
oauth_nonce = str(int(time.time() * 1000))
oauth_timestamp = str(int(time.time()))
oauth_signature_method = 'HMAC-SHA256'
oauth_version = '1.0'
url = 'https://card-entry-service.zalando-payments.com/contexts/checkout/cardsn/oauth2/access_token'


# HMAC-SHA256 hashing algorithm to generate the OAuth signature
def create_signature(secret_key, signature_base_string):
    encoded_string = signature_base_string.encode()
    encoded_key = secret_key.encode()
    temp = hmac.new(encoded_key, encoded_string, hashlib.sha256).hexdigest()
    byte_array = b64encode(binascii.unhexlify(temp))
    return byte_array.decode()


# concatenate the six oauth parameters, plus the request parameters from above, sorted alphabetically by the key and separated by "&"
def create_parameter_string(grant_type, oauth_consumer_key, oauth_nonce, oauth_signature_method, oauth_timestamp,
                            oauth_version):
    parameter_string = ''
    parameter_string = parameter_string + 'grant_type=' + grant_type
    parameter_string = parameter_string + '&oauth_consumer_key=' + oauth_consumer_key
    parameter_string = parameter_string + '&oauth_nonce=' + oauth_nonce
    parameter_string = parameter_string + '&oauth_signature_method=' + oauth_signature_method
    parameter_string = parameter_string + '&oauth_timestamp=' + oauth_timestamp
    parameter_string = parameter_string + '&oauth_version=' + oauth_version
    return parameter_string


parameter_string = create_parameter_string(grant_type, oauth_consumer_key, oauth_nonce, oauth_signature_method,
                                           oauth_timestamp, oauth_version)
encoded_parameter_string = urllib.parse.quote(parameter_string, safe='')
encoded_base_string = 'POST' + '&' + urllib.parse.quote(url, safe='')
encoded_base_string = encoded_base_string + '&' + encoded_parameter_string

# create the signing key
signing_key = access_key_secret + '&'

oauth_signature = create_signature(signing_key, encoded_base_string)
encoded_oauth_signature = urllib.parse.quote(oauth_signature, safe='')

print(signing_key)
print(oauth_signature)
print(encoded_oauth_signature)

# ---------------------Requesting Token---------------------
body = {'grant_type': '{}'.format(grant_type)}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'OAuth oauth_consumer_key="{0}",oauth_nonce="{1}",oauth_signature="{2}",oauth_signature_method="HMAC-SHA256",oauth_timestamp="{3}",oauth_version="1.0"'.format(
        oauth_consumer_key, oauth_nonce, encoded_oauth_signature, oauth_timestamp)
}
print(headers['Authorization'])
response = requests.post(url, data=body, headers=headers)

print(response.text)