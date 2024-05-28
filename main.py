# We import the required modules:
from bs4 import BeautifulSoup
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from my_vars import *

# Call our auth variables:

your_client_id = CLIENT_ID
your_client_secret = CLIENT_SECRET
your_spotify_display_name = SPOTIFY_DISPLAY_NAME


# Prompt Command to ask when we were born?
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

# Then we get the data for the Top100 Hits of that period:
response = requests.get("https://www.billboard.com/charts/hot-100/"+date)

soup = BeautifulSoup(response.text, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# We authenticate on Spotify (after we initialized a App and got our credentials):
sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		scope="playlist-modify-private",
		redirect_uri="http://example.com",
		client_id=your_client_id,
		client_secret=your_client_secret,
		show_dialog=True,
		cache_path="token.txt",
		username=your_spotify_display_name
	)
)

user_id = sp.current_user()["id"]
print(user_id)

# Search the songs in the playlist on Spotify:
song_uris = []
year = date.split("-")[0]

for song in song_names:
	result = sp.search(q=f"track: {song} year: {year}", type="track")
	print(result)
	try:
		uri = result["tracks"]["items"][0]["uri"]
		song_uris.append(uri)
	except IndexError:
		print(f"{song} couldn't be found in Spotify. Skipped.")

# Now we create a new private Spotify Playlist:
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Top100 Hits (data from Billboard.com)", public=False)
print(playlist)

# Now we add the songs to the newly created playlist:
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)