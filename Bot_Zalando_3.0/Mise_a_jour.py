import tkinter as tk
import requests
from tkinter import messagebox

version=1.0
Nom_application='ScredAIO'

def mise_a_jour():
    def check_updates():
            try:
                response = requests.get(
                    'https://raw.githubusercontent.com/AlexisBal/Projet_Bot/master/Bot_Zalando_3.0/Data/Version.txt?token=AO2H2FX6SIFTLKLFHGFACQK7DQIAC')
                data = response.text

                if float(data) > float(__version__):
                    messagebox.showinfo('Software Update', 'Update Available!')
                    message = messagebox.askyesno('Update !', f'{Nom_application} {version} needs to update to version {data}')
                    if message is True:

                       
                        webbrowser.open_new_tab('')
                        parent.destroy()



                    else:
                        pass
                else:
                    messagebox.showinfo('Software Update', 'No Updates are Available.')
            except Exception as e:
                messagebox.showinfo('Software Update', 'Unable to Check for Update, Error:' + str(e))  




mise_a_jour()