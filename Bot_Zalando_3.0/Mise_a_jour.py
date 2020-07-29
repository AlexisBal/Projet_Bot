import tkinter as tk
import requests
from tkinter import messagebox
from bs4 import BeautifulSoup
import webbrowser

version=1.0
Nom_application='ScredAIO'

def mise_a_jour():
    
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Random/Version.txt')
        data = response.text

        if float(data) > float(version):
            messagebox.showinfo('Software Update', 'Update Available!')
            message = messagebox.askyesno('Update !', f'{Nom_application} {version} needs to update to version {data}')
            if message is True:
                       
                webbrowser.open_new_tab('https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Random/Version.txt')
                
                parent.destroy()



            else:
                pass
        else:
            messagebox.showinfo('Software Update', 'No Updates are Available.')
    except Exception as e:
        messagebox.showinfo('Software Update', 'Unable to Check for Update, Error:' + str(e))  




#mise_a_jour()

#with requests.Session() as session:



#response = requests.get('https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Random/Version.txt')
#print(response.text)

#edition = response.find(class ="blob-code blob-code-inner js-file-line")

#print(edition)