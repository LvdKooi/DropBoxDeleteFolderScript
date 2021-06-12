#!/usr/bin/env python3
import sys
from datetime import date, timedelta

import isodate
from dropbox import dropbox
from dropbox.exceptions import ApiError

from DbxTokenService import DbxTokenService

"""
Script created by Laurens van der Kooi. 

This script is meant for periodically deleting a folder from Dropbox (by means of a Cronjob). It writes its state to a 
file 'last_run' which it will create the first time. It is also capable of catching up after not having run for a while. 
The folders it deletes need to have a name that can be related to a date (e.g. 2020-07-14). For the first use it is 
necessary to run this script manually in order to set the app key and refresh token. After that, it can run any time 
without user interference.

"""

MAX_AGE_IN_DAYS = 7


def main():
    last_week = date.today() - timedelta(days=MAX_AGE_IN_DAYS)
    last_run = get_last_run(last_week)

    print(f"Last run deleted folder: {last_run}")

    if last_run == last_week:
        print("Already up to date, program will exit.")
        sys.exit()

    from_date = last_run + timedelta(days=1)

    delete_folders_from_to(from_date, last_week)


def read_file(path):
    try:
        with open(path, "r") as file:
            return file.readline()
    except Exception as e:
        print(f"Couldn't open file {path}. Error: {e}")


def get_dropbox():
    oauth2_refresh_token = read_file("./oauth_access_token")
    app_key = read_file("./app_key")

    if oauth2_refresh_token is None or app_key is None:
        print('Refresh token or app key appears to be missing, follow instructions below...')
        DbxTokenService.set_app_key_and_refresh_token()

    dbx = dropbox.Dropbox(oauth2_refresh_token=read_file("./oauth_access_token"), app_key=read_file("app_key_copy"))
    dbx.users_get_current_account()
    print("Successfully set up client!")
    return dbx


def delete_folders_from_to(from_date, to_date):
    print("Initializing Dropbox API...")
    dbx = get_dropbox()

    while from_date <= to_date:
        date_string = str(from_date)

        delete_dropbox_folder(dbx, date_string)

        from_date = from_date + timedelta(days=1)

    write_last_run_to_file(to_date)


def get_last_run(last_week):
    try:
        with open("./last_run", "r") as file:
            date_string = file.readline()
            return isodate.parse_date(date_string)
    except Exception:
        print("Couldn't open file 'last_run', because it doesn't exist yet. File will be created later on.")
        return last_week - timedelta(days=1)


def delete_dropbox_folder(dbx, date_string):
    print("Deleting folder: {}".format(date_string))
    try:
        dbx.users_get_current_account()
        dbx.files_delete_v2(path=f"/PiCam/{date_string}")
        print(f"Successfully deleted folder: {date_string}.")

    except ApiError as e:
        print("Something went wrong. Folder doesn't exist (anymore).")


def write_last_run_to_file(last_run):
    try:
        with open("./last_run", "w") as file:

            file.write(str(last_run))

    except Exception:
        sys.exit("Failure while opening/creating file 'last_run'. This step is necessary to save this scripts' state.")


main()
