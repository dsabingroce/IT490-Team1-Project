#hello












import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pika 
import os
import json
from pprint import pprint 
import subprocess
from log import *

#spotify authentication
cid ='d874f49748c84696b9015d3c3d1bbcae' # Client ID; copy this from your app 
secret = 'ba49882c11ff438592008d35c3add538' # Client Secret; copy this from your app
username = 'fq1ssqbqvs7td8nir8i8tc5q7' # Your Spotify username

scope = 'user-library-read playlist-modify-public playlist-read-private'

redirect_uri='http://localhost/' # Paste your Redirect URI here

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope, cid, secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)

#get tracks and saves as resutls 
os.system('curl -o seed.json -X "GET" "https://api.spotify.com/v1/recommendations?limit=10&market=US&seed_genres=country" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')

batcmd="cat seed.json | grep 'spotify:track' | sed 's/    \"uri\" : \"spotify:track://g' | sed 's/\"//g'"
new = subprocess.check_output(batcmd, shell=True)

results = new.split("\n")
print(results)
results.pop()
results = list(dict.fromkeys(results))
#print(results)

#create playlist and saves as da_info
name = "That good good 3001"

sp.user_playlist_create(username, name, public=True)

list_info = sp.user_playlists(username, limit=1, offset=0)

da_info = list_info['items'][-1]['id']

#add tracks and saves final link as final
#tracka = ["5TWhLgjy8cgb6CRPnnlnn2"]
for i in range(len(results)):
    results[i] = results[i].strip()

#print(results)
sp.user_playlist_add_tracks(username, da_info, results)

final = "https://open.spotify.com/playlist/" + da_info

#print link
print(final)
db_log("Final link was created.")
