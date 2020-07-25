import requests

def mise_a_jour():
    
    response = requests.get(
    'https://raw.githubusercontent.com/AlexisBal/Projet_Bot/master/Bot_Zalando_3.0/Data/Version.txt?token=AO2H2FXAKZO47FPUA7FM23S7DQDXA')
    data = response.text
    print(data)



mise_a_jour()