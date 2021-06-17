from dropbox import DropboxOAuth2FlowNoRedirect


class DbxTokenService:

    @staticmethod
    def get_app_key_and_refresh_token(workingdirectory):
        app_key = DbxTokenService.__read_file(workingdirectory + "/app_key")
        oauth2_refresh_token = DbxTokenService.__read_file(workingdirectory + "/oauth_access_token")

        if oauth2_refresh_token is None or app_key is None:
            print("Refresh token or app key appears to be missing, follow instructions below...")
            key_token_pair = DbxTokenService.__set_app_key_and_refresh_token(workingdirectory)
            app_key = key_token_pair[0]
            oauth2_refresh_token = key_token_pair[1]

        return app_key, oauth2_refresh_token

    @staticmethod
    def __read_file(path):
        try:
            with open(path, "r") as file:
                return file.readline()
        except Exception as e:
            print(f"Couldn't open file {path}. Error: {e}")

    @staticmethod
    def __set_app_key_and_refresh_token(workingdirectory):
        app_key = input("What is the app-key?")
        refresh_token = DbxTokenService.__obtain_refresh_token(app_key)

        try:
            with open(workingdirectory + "/app_key", "w") as file:
                file.write(app_key)
            with open(workingdirectory + "/oauth_access_token", "w") as file:
                file.write(refresh_token)
            print("Successfully saved api key and refresh token.")
            return app_key, refresh_token
        except Exception as e:
            print(f'Error: {e}')
            exit(1)

    @staticmethod
    def __obtain_refresh_token(app_key):
        auth_flow = DropboxOAuth2FlowNoRedirect(app_key, use_pkce=True, token_access_type='offline')
        authorize_url = auth_flow.start()

        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")

        auth_code = input("Enter the authorization code here: ").strip()
        oauth_result = auth_flow.finish(auth_code)
        return oauth_result.refresh_token
