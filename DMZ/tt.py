import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pika 
import os
import json
from pprint import pprint 
import subprocess

script = 'curl -o new.json -d @location.json -H "Content-Type: application/json" http://www.mapquestapi.com/directions/v2/routematrix?key=8PtZTD2kqepePZgyZPkbfg7Q6EhkUvcP'

cred=pika.PlainCredentials('DMZ', 'DMZ_1234')

connection=pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))

channel = connection.channel()

channel.queue_declare(queue='DMZ_route', durable=True)
channel.queue_declare(queue='DMZ_genre', durable=True)

#get time from Map API
def on_request_route(ch, method, props, body):
    print(body)
    os.system("echo "+body+" > location.json")  

    os.system(script)

    with open('new.json') as f:
    	data = json.load(f)

    time = data["time"]

    pprint(time[1])

    response = time[1]

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

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

def on_request_genre(ch, method, props, stuff):
    stuff = stuff.split(",")
    genre = stuff[0]
    name = stuff[1]
    #get tracks and saves as resutls 
    print(genre)
    print(name)
    os.system('curl -o seed.json -X "GET" "https://api.spotify.com/v1/recommendations?limit=3&market=US&seed_genres='+genre+'" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')

    batcmd="cat seed.json | grep 'spotify:track' | sed 's/    \"uri\" : \"//g' | sed 's/\"//g'"
    new = subprocess.check_output(batcmd, shell=True)

    results = new.split("\n")
    print(results)
    results.pop()
    results = list(dict.fromkeys(results))
    #print(results)
    
    #create new spotify playlist and save Id as da_info
    sp.user_playlist_create(username, name, public=True)

    list_info = sp.user_playlists(username, limit=1, offset=0)

    da_info = list_info['items'][-1]['id']

    for i in range(len(results)):
        results[i] = results[i].strip()

    #print(results)
    sp.user_playlist_add_tracks(username, da_info, results)

    final = "https://open.spotify.com/playlist/" + da_info

    #print link
    print(final)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DMZ_route', on_message_callback=on_request_route)
channel.basic_consume(queue='DMZ_genre', on_message_callback=on_request_genre)

print(" [x] Awaiting Route Time Calculations RPC requests")
channel.start_consuming()
