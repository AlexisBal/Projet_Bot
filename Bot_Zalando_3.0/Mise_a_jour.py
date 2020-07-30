import tkinter as tk
import requests
from tkinter import messagebox, ttk
import webbrowser
from os import getcwd
import urllib.request as ur




def mise_a_jour(version):
    version=1.0
    Nom_application='ScredAIO'
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/JamesBond65/Hujub/master/Random.1/version.txt')
        data = response.text
        print(data)
        

        if float(data) > float(version):
            messagebox.showinfo('Software Update', 'Update Available!')
            message = messagebox.askyesno('Update !', f'{Nom_application} {version} needs to update to version {data}')
            if message is True:
                       

                url = 'https://raw.github.com/JamesBond65/Hujub/master/Random.1/dist/update.exe'
                directory = getcwd()
                print(directory)
                filename = directory + '\Bot_Zalando_3.0\ScredAIO.exe'
                print(filename)
                r = requests.get(url, allow_redirects=True)

                f = open(filename,'wb')
                f.write(r.content)
                version=data
                
                
                
                pass


            else:
                pass
        else:
            messagebox.showinfo('Software Update', 'No Updates are Available.')
            
    except Exception as e:
        messagebox.showinfo('Software Update', 'Unable to Check for Update, Error:' + str(e))
        




mise_a_jour()