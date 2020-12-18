'''
Created on 12.09.2020

@author: Bjoern Graebe
'''
from mpd import MPDClient,ConnectionError

class CannotConnectToMPDError(Exception):
    """This error is thrown when a connection MPD is absolutely impossible."""

class MPDConnection():
    """Connection to a MPD Server. This would make it easy to post it
        to another Play in the future."""
    def __init__(self,pHost,pPort):
        self.host = pHost
        self.port = pPort
        self.mpd_client = MPDClient()
        #self.mpd_client.timeout = 3600

    def connect(self):
        """Connects to the MPD which is specified in the fields host
            and port of MPDConnection."""
        self.mpd_client.connect(host = self.host, port=self.port)

    def ensure_working_connection(self):
        """Ensure a working connection the specified MPD. Is this does
            not succeed an CannotConnectToMPDError is strown."""
        try:
            self.mpd_client.ping()
        except ConnectionError:
            self.connect()
        try:
            self.mpd_client.ping()
        except ConnectionError as connection_error:
            raise CannotConnectToMPDError from connection_error

    def get_possible_tags(self):
        """Returns the tags supported by the MPD to that we are connected to.
            For this a working MPD connection is necessary."""
        self.ensure_working_connection()
        try:
            return self.mpd_client.tagtypes()
        except ConnectionError as connection_error:
            raise CannotConnectToMPDError from connection_error

    def clear(self):
        """Clears the current playlist."""
        self.ensure_working_connection()
        self.mpd_client.clear()

    def get_possible_value_for_tag(self, p_tag):
        """Return a list of the possible values for p_tag."""
        return self.mpd_client.list(p_tag)

    def idle(self):
        """Halts until something happens in the MPD. For example a
            a change of the played song."""
        self.ensure_working_connection()
        self.mpd_client.idle('player')

    def get_play_list_length(self):
        """Returns the count of song in the current playlist."""
        result = self.mpd_client.status()['playlistlength']
        return int(result)

    def get_current_song_number(self):
        """Get the position of the current running song in the current
            playlist. Return -1 if there is no song playing at the moment."""
        status = self.mpd_client.status()
        if status['state'] == 'play':
            result = int(self.mpd_client.status()['song'])
        else:
            result = - 1
        return result

    def is_playing(self):
        """Checks if there is a song playing an the moment."""
        status = self.mpd_client.status()
        result = status['state'] == 'play'
        return result

    def set_mpd_to_run_mpdj(self):
        """Prepares MPD to run a mpdj generated playlist. This sets:
            crossfade to 8 seconds (this should be an option in the future).
            random to toe and replay_gain_mode to track."""
        self.mpd_client.crossfade(8)
        self.mpd_client.random(0)
        self.mpd_client.replay_gain_mode('track')

    def add_song_to_playlist(self, p_path_to_file):
        """Add the song specified by p_path_to_file to the current
            playlist. Ensures a working connection before."""
        self.ensure_working_connection()
        self.mpd_client.add(p_path_to_file)

    def ensure_is_playing(self):
        """Ensure mpd is playing. When it is not playing we start
            playing."""
        status = self.mpd_client.status()
        if status['state'] != 'play':
            self.mpd_client.play()

    def get_files_matching_criteria(self, things_to_find : dict):
        """Return a list of songs which are matching all criterias
            found in the dict things_to_find. """
        self.ensure_working_connection()
        # This splits the dict into tupples (key, values) and sums
        # them up, to get a list for the find method of mpd.
        # Takes is time to understand.
        results = self.mpd_client.find(*sum(things_to_find.items(),()))
        return results
