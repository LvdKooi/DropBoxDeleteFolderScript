#!/usr/bin/env python3
import dropbox, sys, isodate
from datetime import date, timedelta

DAGENGRENS = 7
TOKEN = "jYeEYD8vu1oAAAAAAAAW9dP53LLFNiqd5Nd43yNi5rvLDnrtWY3umiraomLSj_-m"

def main():
    lastweek = date.today() - timedelta(days=DAGENGRENS)
    lastrun = bepaallastrun(lastweek)

    print(f"Laatste run is {lastrun} geweest.")

    if lastrun == lastweek:
        sys.exit("Al helemaal bij met verwijderen. Er wordt niks uitgevoerd.")

    fromdate = lastrun + timedelta(days=1)

    verwijdermappenvantotenmet(fromdate, lastweek)

    schrijflastrunweg(lastweek)


def verwijdermappenvantotenmet(van, totenmet):
    print("Initializing Dropbox API...")
    dbx = dropbox.Dropbox(TOKEN)

    while van <= totenmet:
        datestring = str(van)

        verwijderdropboxmap(dbx, datestring)

        van = van + timedelta(days=1)


def bepaallastrun(lastweek):
    try:
        file = open("./last_run", "r")
        date_string = file.readline()
        file.close()
        return isodate.parse_date(date_string)
    except Exception:
        print("Openen van last_run niet gelukt, bestand bestaat nog niet. Bestand wordt zo alsnog aangemaakt.")
        return lastweek - timedelta(days=1)


def verwijderdropboxmap(dbx, datestring):
    print("Verwijderen van de map {}".format(datestring))
    try:
        dbx.files_delete_v2(path=f"/PiCam/{datestring}")
        print(f"Verwijderen van map {datestring} succesvol.")

    except Exception:
        print("Er iets mis gegaan, de map is waarschijnlijk reeds verwijderd.")


def schrijflastrunweg(lastrun):
    try:
        file = open("./last_run", "w")
        file.write(str(lastrun))
        file.close()
    except Exception:
        sys.exit("Openen van last_run voor wegschrijven van datum is mislukt.")


main()
