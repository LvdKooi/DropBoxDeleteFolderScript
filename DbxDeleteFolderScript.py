#! /usr/bin/python3
import os
import sys
from datetime import date, timedelta

import dropbox
import isodate
from dropbox.exceptions import ApiError

from DbxTokenService import DbxTokenService

MAX_AGE_IN_DAYS = 7
LOCAL_WORKING_DIR = os.getcwd()  # replace if needed


def main():
    last_week = date.today() - timedelta(days=MAX_AGE_IN_DAYS)
    last_run = get_last_run(last_week)

    print(f"Last run deleted folder: {last_run}")

    if last_run == last_week:
        print("Already up to date, program will exit.")
        sys.exit()

    from_date = last_run + timedelta(days=1)

    delete_folders_from_to(from_date, last_week)


def get_dropbox():
    key_token_pair = DbxTokenService.get_app_key_and_refresh_token(LOCAL_WORKING_DIR)
    app_key = key_token_pair[0]
    oauth2_refresh_token = key_token_pair[1]

    dbx = dropbox.Dropbox(oauth2_refresh_token=oauth2_refresh_token,
                          app_key=app_key)
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
        with open(LOCAL_WORKING_DIR + "/last_run", "r") as file:
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
        with open(LOCAL_WORKING_DIR + "/last_run", "w") as file:

            file.write(str(last_run))
    except Exception:
        sys.exit("Failure while opening/creating file 'last_run'. This step is necessary to save this scripts' state.")


main()
