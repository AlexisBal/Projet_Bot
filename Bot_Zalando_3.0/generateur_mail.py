from guerrillamail import GuerrillaMailSession
import time
import requests


'''session = GuerrillaMailSession()
print (session.get_session_state()['email_address'])
print( session.get_email_list()[0].guid)
print(session.get_email(1))
time.sleep(30)
print( session.get_email_list()[0].guid)

print()
#print(session.set_email_address(session)'''

r= requests.get('https://temp-mail.org/fr/')
print(r.cookies)
print("\n\n")

session = requests.Session()
print(session.cookies.get_dict())

response = session.get('https://temp-mail.org/fr/')
print(session.cookies.get_dict())
