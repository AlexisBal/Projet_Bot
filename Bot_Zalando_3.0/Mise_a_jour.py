import tkinter as tk
import requests
from tkinter import messagebox, ttk
import webbrowser
from os import getcwd
import urllib.request as ur
from os import remove
from sys import argv
import os
import time


'''nombre = int(input("entrer un nombre et je le multiplie par 2 :"))
nombre=nombre*2
print(nombre)
time.sleep(5)'''

def mise_a_jour():

    if os.path.basename(__file__) == 'ScredAIO-1.exe':
        
        directory = os.path.dirname(os.path.realpath(__file__))
        old_file_name = directory + '\ScredAIO-1.exe'
        new_file_name = directory +'\ScredAIO.exe'
        os.rename( old_file_name , new_file_name)

    version=1.0
    Nom_application='ScredAIO'

    try:
        headers = {
                    'Authorization': 'token 57a9f2d3432b41fa87ff48ecdce02af2cb228cc8',
                    'Accept': 'application/vnd.github.v3.raw',
                        }

        response = requests.get(
            'https://raw.githubusercontent.com/AlexisBal/Projet_Bot/master/Version_%2B_Executable/Version.txt', 
            headers=headers, allow_redirects=True)
        
        data = float(response.text)
        
        if float(data) > float(version):
            messagebox.showinfo('Software Update', 'Update Available!')
            message = messagebox.askyesno('Update !', f'{Nom_application} {version} needs to update to version {data}')
            if message is True:
                       
                directory = os.path.dirname(os.path.realpath(__file__))
                
                filename = directory + '\ScredAIO-1.exe'
                #print(filename)
                
                headers = {
                    'Authorization': 'token 57a9f2d3432b41fa87ff48ecdce02af2cb228cc8',
                    'Accept': 'application/vnd.github.v3.raw',
                        }

                r = requests.get(
                    'https://raw.githubusercontent.com/AlexisBal/Projet_Bot/master/Version_%2B_Executable/ScredAIO-1.exe', 
                    headers=headers, allow_redirects=True)
                
                f = open(filename,'wb')
                f.write(r.content)
                version=data

                filename = directory + '\ScredAIO-1.exe'
                os.startfile(filename)
                
                #remove(argv[0])
                pass

            else:
                pass
        else:
            messagebox.showinfo('Software Update', 'No Updates are Available.')
            
    except Exception as e:
        messagebox.showinfo('Software Update', 'Unable to Check for Update, Error:' + str(e))


mise_a_jour()