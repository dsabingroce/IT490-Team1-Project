import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pika 
import os
import json
from pprint import pprint 
import subprocess
from log import *
time = 0
ftime = 0

db_log("DMZ authenticated with Spotify")
 
script = 'curl -o new.json -d @location.json -H "Content-Type: application/json" http://www.mapquestapi.com/directions/v2/routematrix?key=8PtZTD2kqepePZgyZPkbfg7Q6EhkUvcP'

cred=pika.PlainCredentials('DMZ', 'DMZ_1234')

connection=pika.BlockingConnection(pika.ConnectionParameters('192.168.1.5', 5672, '/', cred))

channel = connection.channel()

channel.queue_declare(queue='DMZ_route', durable=True)
channel.queue_declare(queue='DMZ_saved', durable=True)
channel.queue_declare(queue='DMZ_genre', durable=True)

#get time from Map API
def on_request_route(ch, method, props, body):
    db_log("DMZ received new route information from F.E")
    global time
    global ftime
    print(body)
    os.system("echo "+body+" > location.json")  

    os.system(script)

    with open('new.json') as f:
    	data = json.load(f)

    time = data["time"]

    time = time[1]

    ftime = ((time / 60) / 3)

    if ftime == 0:
        ftime = 1

    print("Time: " + time)
    print("Tracks: " + ftime)

    response = time

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    db_log("DMZ sent new route time to F.E")

def on_request_saved(ch, method, props, saved):
    db_log("DMZ received saved route time from F.E")
    global time
    global ftime
    time = saved

    ftime = ((int(time) / 60) / 3)
    print("Time: " + int(time))
    print("Tracks: " + ftime)

    if ftime == 0:
        ftime = 1


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



def on_request_genre(ch, method, props,stuff):
    db_log("DMZ received genre and playlist name from F.E")
    global time
    global ftime
    stuff = stuff.split(",")
    genre = stuff[0]
    name = stuff[1]
    #get tracks and saves as resutls 
    print("Genre: " + genre)
    print("Playlist name: " + name)
    print(str(ftime))
    os.system('curl -o seed.json -X "GET" "https://api.spotify.com/v1/recommendations?limit='+str(ftime)+'&market=US&seed_genres='+genre+'" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '+token+'"')


    batcmd="cat seed.json | grep 'spotify:track' | sed 's/    \"uri\" : \"//g' | sed 's/\"//g'"
    new = subprocess.check_output(batcmd, shell=True)

    results = new.split("\n")
    #print(results)
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
    print("Link" + final)

    response = final

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Link Sent")
    db_log("DMZ created new link and sent it to F.E")
    
    if genre == 'country':
        da_country = 1
    else:
        da_country = 0

    if genre == 'edm':
        da_edm = 1
    else:
        da_edm = 0

    if genre == 'hip-hop':
        da_hiphop = 1
    else:
        da_hiphop = 0

    if genre == 'pop':
        da_pop = 1
    else:
        da_pop = 0

    if genre == 'rock':
        da_rock = 1
    else:
        da_rock = 0

    scoreboard = "{},{},{},{},{},{},{}".format(time, ftime, da_country, da_edm, da_hiphop, da_pop, da_rock)

    print ("Scoreboard: " + scoreboard)

    channel.exchange_declare(exchange='DB_addScores', exchange_type='direct', durable=True)
    channel.basic_publish(exchange='DB_addScores', routing_key='', body=scoreboard)
    db_log("DMZ sent scoreboard update to Database.")

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='DMZ_route', on_message_callback=on_request_route)
channel.basic_consume(queue='DMZ_genre', on_message_callback=on_request_genre)
channel.basic_consume(queue='DMZ_saved', on_message_callback=on_request_saved)

print(" [x] Awaiting Route Time Calculations RPC requests")
channel.start_consuming()
