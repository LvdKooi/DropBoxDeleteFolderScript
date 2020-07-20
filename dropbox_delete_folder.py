#!/usr/bin/env python3
import dropbox, sys, isodate
from datetime import date, timedelta

DAGEN_GRENS = 7
TOKEN = "jYeEYD8vu1oAAAAAAAAW9dP53LLFNiqd5Nd43yNi5rvLDnrtWY3umiraomLSj_-m"

print("Initializing Dropbox API...")
dbx = dropbox.Dropbox(TOKEN)

last_week = date.today() - timedelta(days=DAGEN_GRENS)

try:
    file = open("./last_run", "r")
    date_string = file.readline()

    last_run = isodate.parse_date(date_string)
    file.close()
except Exception:
    print("Openen is mislukt, bestand last_run bestaat nog niet.")
    last_run = last_week - timedelta(days=1)

if last_run == last_week:
    sys.exit("Al helemaal bij met verwijderen. Er wordt niks uitgevoerd.")

from_date = last_run + timedelta(days=1)

while from_date <= last_week:
    date_string = str(from_date)
    print("Verwijderen van de map {}".format(date_string))

    try:
        dbx.files_delete_v2(path="/PiCam/{}".format(date_string))
        print("Verwijderen van map {} succesvol.".format(date_string))

    except Exception:
        print("Er iets mis gegaan, de map is waarschijnlijk reeds verwijderd.")

    from_date = from_date + timedelta(days=1)

try:
    file = open("./last_run", "w")
    file.write(str(last_week))
except Exception:
    sys.exit("openen is mislukt")
finally:
    file.close()