

**The script**

This repo contains a script (DbxDeleteFolderScript.py) which is meant for periodically deleting a folder from Dropbox 
(by means of a Cronjob). It writes its state to a file 'last_run' which it will create the first time. The script is also 
capable of catching up after not having run for a while. The folders it deletes need to have a name that can be related 
to a date (e.g. 2020-07-14). For the first use it is necessary to run this script manually in order to set the app key 
and refresh token. For this, this repo also contains a helper class (DbxTokenService) which facilitates this. After that, 
it can run any time without any user interference.

Created by: Laurens van der Kooi

**Setting up Cronjobs**

First, install packages: 

```
pip install dropbox
pip instal isodate
```


Then, make python script executable:
```
chmod +x DbxDeleteFolderScript.pu
```
Change the shebang line as needed:

* On OS X, the shebang line is #! /usr/bin/env python3.
* On Linux, the shebang line is #! /usr/bin/python3.

Check if the script runs (you might need to reformat the script with dos2unix in your Linux-based terminal, as shown below).

```
dos2unix ./DbxDeleteFolderSCript.py
```
Then in terminal: 

```
crontab -e
```
and

On MacOs:
```
PATH = /Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin
52 16 * * * /Users/laurensvanderkooi/PycharmProjects/DropBoxScripting/DbxDeleteFolderScript.py
```
On Linux:
```
52 16 * * * /Users/laurensvanderkooi/PycharmProjects/DropBoxScripting/DbxDeleteFolderScript.py
```

