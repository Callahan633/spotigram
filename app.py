import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
import asyncio_redis
import asyncio

dev_config = configparser.ConfigParser()
dev_config.read('settings_dev.ini')  # Change this to 'settings_example.ini' with your credentials


class SpotifyClient:
    def __init__(self):
        self.scope = 'user-library-read'
        self.user = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=self.scope,
            client_id=dev_config['SPOTIFY_CRED']['SPOTIPY_CLIENT_ID'],
            client_secret=dev_config['SPOTIFY_CRED']['SPOTIPY_CLIENT_SECRET'],
            redirect_uri=dev_config['SPOTIFY_CRED']['SPOTIPY_REDIRECT_URI'],
            cache_path=dev_config['SPOTIFY_CRED']['CACHE_PATH'])
        )

    @staticmethod
    async def _collect_tracks(query_result: dict):
        redis_connection_pool = await asyncio_redis.Pool.create(host='localhost', port=6379, poolsize=30)
        for item in query_result['items']:
            artists_names = [x['name'] for x in item['track']['artists']]
            await redis_connection_pool.set(f'{artists_names}', item['track']['name'])
            saved_tracks = await redis_connection_pool.get(f'{artists_names}')
            print(saved_tracks)
            # print(artists_names, item['track']['name'])
        redis_connection_pool.close()

    async def list_duplicate_tracks(self):
        query_result = self.user.current_user_saved_tracks(limit=50)
        await self._collect_tracks(query_result)
        while query_result['next']:
            query_result = self.user.next(query_result)
            await self._collect_tracks(query_result)


loop = asyncio.get_event_loop()
loop.run_until_complete(SpotifyClient().list_duplicate_tracks())
