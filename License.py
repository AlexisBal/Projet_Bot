from licensing.models import *
from licensing.methods import Key, Helpers

# Pip install licensing
# licensing-0.21

# Informations du propriaitaire
RSAPubKey = "<RSAKeyValue><Modulus>zGKjhD1u4eZQg+U2oZgX8inZ1SLvb83jD+oKD20GplwpYcqquQZMAPokGXTs8FMD5X2sc6FtiNKg/wcapvkuyS9KRTauaoQib/B2SW7e9b4zkfpg3hJHW8zm9CZ3F2xbH5E8aXOlm0Knu9lOxjE+e7IogTQGk5RvyO4TO6QRO71bc9dW9h44KWdzku6lcF1VBHM646E6F10ziq7beGhmyLt/dbz88Yt9VP5CKBRH+/QDafbV+KD86WFTQ69p/j+k/h1QF2LYY2tVOhz9TL0iF9zpb8e4mR/vL1RGU3T3ztS21AwGwyCI2j1xc8KvWsUWnPgfDsIr4SRi6EH0d5joxQ==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
auth = "WyIyOTQ2NiIsInBGK1diMVN2TnhPd3ZZTnNxczNXd3MvZS8xT3hKK2RKZk9wbklBT1ciXQ=="


# Fonction de vérification les liscences en ligne. (https://cryptolens.io/)
def VerificationLicense():
    with open("Data/License.txt", "r") as f:
        License = f.read()

    result = Key.activate(token=auth,
                          rsa_pub_key=RSAPubKey,
                          product_id=6868,
                          key=License,
                          machine_code=Helpers.GetMachineCode())

    if result[0] is None or not Helpers.IsOnRightMachine(result[0]):
        print("ERREUR: {0}".format(result[1]))
        print("Inserrez votre license dans le fichier License.txt")
        exit()

    else:
        print("Votre license est valide.")
        pass


VerificationLicense()
