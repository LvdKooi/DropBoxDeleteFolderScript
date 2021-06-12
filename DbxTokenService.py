from dropbox import DropboxOAuth2FlowNoRedirect


class DbxTokenService:

    @staticmethod
    def set_app_key_and_refresh_token():
        app_key = input("What is the app-key?")
        refresh_token = DbxTokenService.__obtain_refresh_token(app_key)

        try:
            with open("app_key", "w") as file:
                file.write(app_key)
            with open("./oauth_access_token", "w") as file:
                file.write(refresh_token)
            print("Successfully saved api key and refresh token.")
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
