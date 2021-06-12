

**The script**

The script in DbxDeleteFolderScript.py is meant for periodically deleting a folder from Dropbox (by means of a Cronjob). It 
writes its state to a file 'last_run' which it will create the first time. It is also capable of catching up after not 
having run for a while. The folders it deletes need to have a name that can be related to a date (e.g. 2020-07-14). For 
the first use it is necessary to run this script manually in order to set the app key and refresh token. After that, it 
can run any time without any user interference.

Created by: Laurens van der Kooi

**Setting up Cronjobs**

First, install packages and make python script executable (chmod +x)

Then in terminal: crontab -e

and

On MacOs:

PATH = /Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin
52 16 * * * /Users/laurensvanderkooi/PycharmProjects/DropBoxScripting/DbxDeleteFolderScript.py

On Linux:

52 16 * * * /Users/laurensvanderkooi/PycharmProjects/DropBoxScripting/DbxDeleteFolderScript.py

After typing:
save by pressing Esc and type :wq
ignore changes by typing :qa
