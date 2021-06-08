import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

'''
Use this to setup a refresh token and the app key in order to the dropbox_delete_folder script
'''
app_key = input("What is the app-key?")

auth_flow = DropboxOAuth2FlowNoRedirect(app_key, use_pkce=True, token_access_type='offline')

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print("2. Click \"Allow\" (you might have to log in first).")
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    with open("./app_key", "w") as file:
       file.write(app_key)

    oauth_result = auth_flow.finish(auth_code)

    with open("./oauth_access_token", "w") as file:
       file.write(oauth_result.refresh_token)

except Exception as e:
    print('Error: %s' % (e,))
    exit(1)

