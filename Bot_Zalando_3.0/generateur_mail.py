from guerrillamail import GuerrillaMailSession


session = GuerrillaMailSession()
print (session.get_session_state()['email_address'])
print( session.get_email_list()[0].guid)
print(session.get_email(1))
#print(session.set_email_address(session)
