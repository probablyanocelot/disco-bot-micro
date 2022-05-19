import requests
import pytest
import tidalapi
from tidalapi import Artist, Album, Playlist, Track, Video


class TestSession(tidalapi.Session):
    def __init__(self):
        super().__init__(self.__dict__)

        try:
            test_load_oauth_session(self)
            print(1)
        except:
            self.test_oauth_login_simple()
            print(2)

    def test_load_oauth_session(self, session):
        session_id = session.session_id
        token_type = session.token_type
        access_token = session.access_token
        session = tidalapi.Session()
        assert session.load_oauth_session(session_id, token_type, access_token)
        assert session.check_login()
        assert isinstance(session.user, tidalapi.LoggedInUser)
        assert session.load_oauth_session(
            session_id + "f", token_type, access_token) is False

    def test_failed_login(self):
        session = tidalapi.Session()
        with pytest.raises(requests.HTTPError):
            session.login("", "")
        assert session.check_login() is False

    def test_oauth_login(self):
        config = tidalapi.Config(item_limit=20000)
        session = tidalapi.Session(config)
        login, future = session.login_oauth()
        print("Visit", login.verification_uri_complete,
              "to log in, the link expires in", login.expires_in, "seconds")
        future.result()
        assert session.check_login()
        assert session.config.item_limit == 10000

    def test_failed_oauth_login(self, session):
        client_id = session.config.client_id
        config = tidalapi.Config()
        config.client_id = client_id + 's'
        session = tidalapi.Session(config)
        with pytest.raises(requests.HTTPError):
            session.login_oauth()

    def test_oauth_login_simple(self):
        session = tidalapi.Session()
        session.login_oauth_simple()

    def test_oauth_refresh(self, session):
        access_token = session.access_token
        expiry_time = session.expiry_time
        refresh_token = session.refresh_token
        session.token_refresh(refresh_token)
        assert session.access_token != access_token
        assert session.expiry_time != expiry_time

    def test_search(self, session):
        # Great edge case test
        search = session.search("Walker", limit=300)
        assert len(search['artists']) == 300
        assert len(search['albums']) == 300
        assert len(search['tracks']) == 300
        assert len(search['videos']) == 300
        assert len(search['playlists']) >= 195
        assert isinstance(search['artists'][0], Artist)
        assert isinstance(search['albums'][0], Album)
        assert isinstance(search['tracks'][0], Track)
        assert isinstance(search['videos'][0], Video)
        assert isinstance(search['playlists'][0], Playlist)

        assert (search['top_hit']).name == "Alan Walker"

    def test_type_search(self, session):
        search = session.search("Hello", [Playlist, Video])
        assert isinstance(search['top_hit'], Playlist)

        assert len(search['artists']) == 0
        assert len(search['albums']) == 0
        assert len(search['tracks']) == 0
        assert len(search['videos']) == 50
        assert len(search['playlists']) == 50

    def test_invalid_type_search(self, session):
        with pytest.raises(ValueError):
            session.search("Hello", [tidalapi.Genre])

    def test_invalid_search(self, session):
        search = session.search('ERIWGJRGIJGRWEIOGRJOGREIWJIOWREG')
        assert len(search['artists']) == 0
        assert len(search['albums']) == 0
        assert len(search['tracks']) == 0
        assert len(search['videos']) == 0
        assert len(search['playlists']) == 0
        assert search['top_hit'] is None

    def test_config(self, session):
        assert session.config.item_limit == 1000
        assert session.config.quality == tidalapi.Quality.master.value
        assert session.config.video_quality == tidalapi.VideoQuality.high.value
        assert session.config.alac is True


if __name__ == '__main__':
    session = TestSession()
