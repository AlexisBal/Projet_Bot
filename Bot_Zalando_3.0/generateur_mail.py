from tempMail2 import TempMail

tm = TempMail()
print(tm)
email = tm.get_email_address()
print tm.get_mailbox(email)