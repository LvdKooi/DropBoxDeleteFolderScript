#!/usr/bin/env python3
import dropbox, sys, isodate
from datetime import date, timedelta

DAGEN_GRENS = 7
TOKEN = "jYeEYD8vu1oAAAAAAAAW9dP53LLFNiqd5Nd43yNi5rvLDnrtWY3umiraomLSj_-m"

def main():
    last_week = date.today() - timedelta(days=DAGEN_GRENS)
    last_run = bepaal_last_run(last_week)

    print(f"Laatste run is {last_run} geweest.")

    if last_run == last_week:
        print("Al helemaal bij met verwijderen. Er wordt niks uitgevoerd.")
        return

    from_date = last_run + timedelta(days=1)

    verwijder_mappen_van_tot_en_met(from_date, last_week)

    schrijf_last_run_weg(last_week)


def verwijder_mappen_van_tot_en_met(van, tot_en_met):
    print("Initializing Dropbox API...")
    dbx = dropbox.Dropbox(TOKEN)

    while van <= tot_en_met:
        date_string = str(van)

        verwijder_dropbox_map(dbx, date_string)

        van = van + timedelta(days=1)


def bepaal_last_run(last_week):
    try:
        file = open("./last_run", "r")
        date_string = file.readline()
        file.close()
        return isodate.parse_date(date_string)
    except Exception:
        print("Openen van last_run niet gelukt, bestand bestaat nog niet. Bestand wordt zo alsnog aangemaakt.")
        return last_week - timedelta(days=1)


def verwijder_dropbox_map(dbx, date_string):
    print("Verwijderen van de map {}".format(date_string))
    try:
        dbx.files_delete_v2(path=f"/PiCam/{date_string}")
        print(f"Verwijderen van map {date_string} succesvol.")

    except Exception:
        print("Er iets mis gegaan, de map is waarschijnlijk reeds verwijderd.")


def schrijf_last_run_weg(last_run):
    try:
        file = open("./last_run", "w")
        file.write(str(last_run))
        file.close()
    except Exception:
        sys.exit("Openen van last_run voor wegschrijven van datum is mislukt.")


main()
