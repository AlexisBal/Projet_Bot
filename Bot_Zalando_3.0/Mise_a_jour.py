import tkinter as tk
import requests
from tkinter import messagebox, ttk
import webbrowser

version=1.0
Nom_application='Bot'

def mise_a_jour():
    
    try:
        response = requests.get(
            'https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Random/Version.txt')
        data = response.text
        

        if float(data) > float(version):
            messagebox.showinfo('Software Update', 'Update Available!')
            message = messagebox.askyesno('Update !', f'{Nom_application} {version} needs to update to version {data}')
            if message is True:
                       
                response = requests.get('https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Principale.py')
                code = response.text
                print(code)

                with open("Bot_Zalando_3.0/ScredAIO1.py", "w") as f:
                    f.write(code)
                
                pass


            else:
                pass
        else:
            messagebox.showinfo('Software Update', 'No Updates are Available.')
            
    except Exception as e:
        messagebox.showinfo('Software Update', 'Unable to Check for Update, Error:' + str(e))




mise_a_jour()




#mise_a_jour()

#response = requests.get('https://raw.githubusercontent.com/JamesBond65/Hujub/master/Rnadom%201/Random/Version.txt')
#print(response.text)

#edition = response.find(class ="blob-code blob-code-inner js-file-line")

#print(edition)