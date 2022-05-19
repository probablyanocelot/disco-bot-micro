import vlc
import requests
import keyboard
# from models import Song


class Player():
    def __init__(self, json_data):

        # keyboard.add_hotkey(r'ctrl + alt + 8',
        #                     lambda: self.next_song())
        # keyboard.add_hotkey(r'ctrl + alt + 9',
        #                     lambda: self.media_player.pause())
        # keyboard.add_hotkey(r'ctrl + alt + 0', lambda: self.next_song())

        self.Instance = vlc.Instance()  # "prefer-insecure"
        self.media_player = vlc.MediaListPlayer()
        self.playlist = self.Instance.media_list_new()
        self.counter = 0
        self.queue_song()
        self.media_player.play()
        self.print('after play')
        # media_player.play_item_at_index(0)
        self.print('after play_item_at_index')
        self.keyboard.wait(r'ctrl + alt + q')
        self.media_player.stop()

    def queue_song(self):
        # song = Song.query.get(self.counter)
        res = requests.get(
            'http://backend:5000/api/songs/{}/stream'.format(self.counter)).json()
        song = Song(res['id'], res['title'], res['url'])
        Media = self.Instance.media_new(song.url)
        Media.get_mrl()
        self.playlist.add_media(Media)
        self.media_player.set_media_list(self.playlist)

    def next_song():
        self.counter += 1
        queue_song()
        self.media_player.next()

    def prev_song():
        self.counter -= 1
        self.media_player.previous()

    # user_input()
