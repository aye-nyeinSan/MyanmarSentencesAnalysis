from googleapiclient.discovery import build
from ftlangdetect import detect




# Set up YouTube API credentials
API_KEY = 'AIzaSyD1VE1rJUFBTtP-bIMZZB1oRbLX4GZG-gs'
VIDEO_ID = 'Djhd3bS9ifk'


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
    
# Function to get comments from a video
def get_video_comments(video_id):
    comments = []
    next_page_token = None
    
    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            pageToken=next_page_token
        )
        
        response = request.execute()
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            is_burmese_comment = is_burmese(comment)
            if is_burmese_comment:
                comments.append(comment)
    
            
        next_page_token = response.get('nextPageToken')
        
        if not next_page_token:
            break
        
        return comments
    
burmese_comments = get_video_comments(VIDEO_ID)


 