from datetime import datetime
def horloge():

    now = datetime.now()
    heures = now.hour
    heures = str(heures)
    minutes= now.minute
    minutes = str(minutes)
    secondes = now.second
    secondes = str(secondes)
    milisecondes = now.microsecond
    milisecondes= str(milisecondes)
    milisecondes = milisecondes[0] + milisecondes[1] + milisecondes[2]
    horloge = "[" + heures + ":" + minutes + ":" + secondes + "." + milisecondes + "]"
    return horloge

print(horloge())