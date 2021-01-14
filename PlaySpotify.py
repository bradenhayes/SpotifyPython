import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from datetime import datetime
import schedule
import time


cid ="61ce98e1500d48438714352d227ede3e" 
secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
username = "bradenhayes55"
redirect_url='http://localhost:8000'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
scope = "playlist-modify-public playlist-modify-private playlist-read-private user-modify-playback-state"
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
                
    except:
            print("Failed to parse JSON")
    
    sp.user_playlist_add_tracks(username,playlist_id[0],ids)
    try:
        sp.start_playback(device_id='15f2001582a255b113c082f8327e1dcbc21e4ea8',context_uri="spotify:playlist:" +playlist_id[0])
    except:
            print("Device is offline")

    
def getTrackIDs(user, playlist_id):
    ids =[]
    playlist = sp.user_playlist(user, playlist_id)
    for x in playlist['tracks']['items']:
        track = x['track']
        ids.append(track['id'])
    return ids


def new_playlist():
    ids = getTrackIDs(username, '37i9dQZEVXbwTsxvuo6IFR')
    create_and_add(ids)
    
schedule.every().sunday.at('13:24').do(new_playlist)
while 1:
    schedule.run_pending()
    time.sleep(1)
