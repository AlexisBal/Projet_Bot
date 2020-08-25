import random
import string
from random import randint


def generateur_mail():
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

    word = get_random_string(6)

    nombre = randint(1111, 9999)
    doamine = ["@icanav.net", "@in4mail.net", "@intsv.net", "@kleogb.com", "@mail2paste.com", "@mailvk.net",
               "@ofmailer.net"]
    terminaison = randint(0, 6)

    email = word + str(nombre) + str(doamine[terminaison])

    return email


print(generateur_mail())
print(type(generateur_mail()))

