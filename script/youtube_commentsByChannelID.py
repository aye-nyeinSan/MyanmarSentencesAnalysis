from googleapiclient.discovery import build
from ftlangdetect import detect
import time

API_KEY = 'AIzaSyD1VE1rJUFBTtP-bIMZZB1oRbLX4GZG-gs'
VIDEO_ID = 'Djhd3bS9ifk'
CHANNEL_ID = 'UCr4rTXIfsJhAOaYOq0iBuTQ'

youtube = build('youtube', 'v3', developerKey=API_KEY)

#Checking only burmese language
def is_burmese(burmese):
    try:
       result = detect(text= burmese , low_memory = True)
       if result['lang'] == 'my' and result['score'] > 0.9:
            return True
       else:
           return False
    except:
        return False

def get_all_video_ids(channel_id):
    video_ids = []
    next_page_token = None

    # Get uploads playlist ID
    res = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    uploads_playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=uploads_playlist_id,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()

        for item in pl_response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids

def get_comments_from_video(video_id):
    comments = []
    next_page_token = None

    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                if is_burmese(comment):
                    comments.append(comment)

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

            time.sleep(0.5)  # avoid quota issues
        except Exception as e:
            print(f"Error fetching comments for video {video_id}: {e}")
            break

    return comments

def get_all_burmese_comments(channel_id):
    all_comments = []
    video_ids = get_all_video_ids(channel_id)

    print(f"Found {len(video_ids)} videos in channel.")

    for idx, vid in enumerate(video_ids, 1):
        print(f"Fetching comments from video {idx}/{len(video_ids)}: {vid}")
        comments = get_comments_from_video(vid)
        all_comments.extend(comments)

    return all_comments

# --- Run the script ---
comments = get_all_burmese_comments(CHANNEL_ID)
print(f"Total Burmese comments found: {len(comments)}")

# Optionally save to a file
with open("burmese_comments.csv", "w", encoding="utf-8") as f:
    for comment in comments:
        f.write(comment + "\n")
