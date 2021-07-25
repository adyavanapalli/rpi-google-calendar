"""setup-oauth.py

A script that runs through an OAuth 2.0 flow to obtain a refreshable token.
"""

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar.events.readonly"]
TOKEN_FILE = "token.json"


def main():
    credentials = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    ).run_local_server()

    with open(TOKEN_FILE, "w") as token_file:
        token_file.write(credentials.to_json())


if __name__ == "__main__":
    main()
