import RPi.GPIO as GPIO
import MFRC522
import signal
import firebase_admin
import json
import os
from firebase_admin import credentials
from firebase_admin import db

credentialsPath = "/home/pi/Desktop/final/papipe-f7cd8-firebase-adminsdk-9cagp-58384dec5d.json"
saveCardPath = "/home/pi/Desktop/final/data"

continue_reading = True


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


cred = credentials.Certificate(credentialsPath)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://papipe-f7cd8-default-rtdb.europe-west1.firebasedatabase.app/'
})

ref = db.reference('server/saving-data/pap')


def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = format(i, '02X') + mystring
    return mystring


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:  # !-- Start
        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_SelectTagSN()

        open(saveCardPath + "/lastcard.txt", "w").write(uidToString(uid))
        print("Card detected")

        users_ref = ref.child("users").child(uidToString(uid)).update({
            'name': "Saraiva",
            'type': "Militar",
            'senhas': 4
        })

        if status == MIFAREReader.MI_OK:
            print("Card read UID: %s" % uidToString(uid))
        else:
            print("Authentication error")
