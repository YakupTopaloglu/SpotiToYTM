import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
import pandas as pd

# ➤ Spotify Kimlik Bilgilerini Gir
SPOTIFY_CLIENT_ID = '***************'
SPOTIFY_CLIENT_SECRET = '*************************'
SPOTIFY_REDIRECT_URI = 'https://example.org/callback'

# ➤ YouTube API Key
YOUTUBE_API_KEY = '**********************'


# ➤ Spotify Bağlantısı
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
))

# ➤ Çalma Listelerini Listele
playlists = sp.current_user_playlists()
print("\nÇalma Listeleri:")
for idx, playlist in enumerate(playlists['items']):
    print(f"{idx + 1}: {playlist['name']}")

choice = int(input("\nKaç numaralı listeyi aktarmak istiyorsun? ")) - 1
playlist_id = playlists['items'][choice]['id']
playlist_name = playlists['items'][choice]['name']

# ➤ Şarkıları Çek
tracks = sp.playlist_tracks(playlist_id)
track_names = []
for item in tracks['items']:
    track = item['track']
    if track is None:  # ⚠ Silinmiş veya erişilemeyen şarkı
        continue
    name = f"{track['name']} {track['artists'][0]['name']}"
    track_names.append(name)

# ➤ YouTube Bağlantılarını Bul
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
results = []

for song in track_names:
    request = youtube.search().list(
        q=song,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        youtube_link = f"https://www.youtube.com/watch?v={video_id}"
    else:
        youtube_link = "Bulunamadı"
    
    results.append({'Şarkı': song, 'YouTube Linki': youtube_link})
    print(f"{song} → {youtube_link}")

# ➤ Excel (CSV) Olarak Kaydet
df = pd.DataFrame(results)
csv_filename = f"{playlist_name}_youtube_links.csv"
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
