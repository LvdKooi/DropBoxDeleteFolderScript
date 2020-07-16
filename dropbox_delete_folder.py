#! /usr/bin/python3
import dropbox
from datetime import date, timedelta

DAGEN_GRENS = 7
TOKEN = "jYeEYD8vu1oAAAAAAAAW9dP53LLFNiqd5Nd43yNi5rvLDnrtWY3umiraomLSj_-m"

print("Initializing Dropbox API...")
dbx = dropbox.Dropbox(TOKEN)

vorige_week_string = str(date.today() - timedelta(days=DAGEN_GRENS))

print("Verwijderen van de map {}".format(vorige_week_string))

try:
    dbx.files_delete_v2(path="/PiCam/{}".format(vorige_week_string))
    print("Verwijderen van map {} succesvol.".format(vorige_week_string))
except Exception:
    print("Er iets mis gegaan, de map is waarschijnlijk reeds verwijderd.")