**Setting up Cronjobs**

First, install packages and make python script executable (chmod +x)

Then in terminal: crontab -e

and

On MacOs:

PATH = /Library/Frameworks/Python.framework/Versions/3.8/bin:/usr/local/bin:/usr/bin:/bin
52 16 * * * /Users/laurensvanderkooitkp/PycharmProjects/DropBoxScripting/dropbox_delete_folder.py

On Linux:

52 16 * * * /Users/laurensvanderkooitkp/PycharmProjects/DropBoxScripting/dropbox_delete_folder.py

After typing:
save by pressing Esc and type :wq
ignore changes by typing :qa