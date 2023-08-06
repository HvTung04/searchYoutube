import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # No valid credentials -> login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else: # Create first time
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())
    
    try:
        service = build('youtube', 'v3', credentials=creds)

        # Search for video
        search_query = "SonTungMTP"
        max_result = 10
        response = service.search().list(
            part='snippet',
            q=search_query,
            type='video',
            maxResults= max_result,
        ).execute()
        videos = response['items']
        for video in videos:
            video_id = video['id']['videoId']
            video_name = video['snippet']['title']
            print(f"This video has title: {video_name}.\nID: {video_id}")
    except HttpError as error:
        print("An error occured", error)


if __name__ == "__main__":
    main()