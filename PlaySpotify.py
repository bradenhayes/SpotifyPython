import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from datetime import datetime
import schedule
import time


cid ="61ce98e1500d48438714352d227ede3e" 
secret = "5472a4601ac94130bd9f1a097eb7095a"
username = "bradenhayes55"
redirect_url='http://localhost:8000'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = "playlist-modify-public playlist-modify-private playlist-read-private"
token = util.prompt_for_user_token(username, scope,cid,secret,redirect_url)


if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)    
   
def create_and_add(ids):    
    sp.user_playlist_create(username,datetime.today().strftime('%Y-%m-%d'),public=False)
    playlist_id=[]
    playlist_json= sp.user_playlists(username,limit=1)
    try:
        for x in playlist_json['items']:
            playlist_id.insert(0,str(x['id']))
            #print(playlist_id[0])
                
    except:
            print("Failed to parse JSON")
    
    sp.user_playlist_add_tracks(username,playlist_id[0],ids)
    
    


    
def getTrackIDs(user, playlist_id):
    ids =[]
    playlist = sp.user_playlist(user, playlist_id)
    for x in playlist['tracks']['items']:
        track = x['track']
        ids.append(track['id'])
    return ids


def new_playlist():
    ids = getTrackIDs(username, '37i9dQZEVXbwTsxvuo6IFR')
    #print(ids)
    create_and_add(ids)
    
schedule.every().friday.at('16:30').do(new_playlist)
while 1:
    schedule.run_pending()
    time.sleep(1)
