import requests
from tkinter import messagebox

version=1.0
Nom_application='ScredAIO'

def mise_a_jour():
    
    response = requests.get(
    'https://raw.githubusercontent.com/AlexisBal/Projet_Bot/master/Bot_Zalando_3.0/Data/Version.txt?token=AO2H2FQPIOVTLAPT3SBGF6K7DQESE')
    data = response.text
    print(data)

    if float(data) > float(version):
                    messagebox.showinfo('Software Update', 'Update Available!')
                    mb1 = messagebox.askyesno('Update!', f'{Nom_application} {version} needs to update to version {data}')




mise_a_jour()