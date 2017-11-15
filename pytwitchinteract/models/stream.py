class Stream:

    @staticmethod
    def from_json(data, twitch):
        return Stream(
            data['id'],
            data['user_id'],
            data['game_id'],
            data['community_ids'],
            data['type'],
            data['title'],
            data['viewer_count'],
            data['started_at'],
            data['language'],
            data['thumbnail_url'],
            twitch
        )

    def __init__(self, stream_id, user_id, game_id, community_ids, stream_type, title, viewer_count, started_at, language, thumbnail_url, twitch):
        """
        :param stream_id: Stream ID
        :param user_id: ID of the user who is streaming
        :param game_id: ID of the game being played on the stream
        :param community_ids: Array of community IDs
        :param stream_type: Stream type: "live", "vodcast", "playlist", or ""
        :param title: Stream title
        :param viewer_count: Number of viewers watching the stream at the time of the query
        :param started_at: UTC timestamp
        :param language: Stream language
        :param thumbnail_url: Thumbnail URL of the stream.
            All image URLs have variable width and height.
            You can replace {width} and {height} with any values to get that size image
        :param twitch: Twitch API instance
        """
        self.id = stream_id
        self.user_id = user_id
        self.game_id = game_id
        self.community_ids = community_ids
        self.type = stream_type
        self.title = title
        self.viewer_count = viewer_count
        self.started_at = started_at
        self.language = language
        self.thumbnail_url = thumbnail_url
        self.twitch = twitch

    def get_user(self):
        """
        :return: User
        """
        return self.twitch.get_users(id=self.user_id)[0]

    def get_game(self):
        """
        :return: Game or None
        """
        if self.game_id is None or self.game_id == "":
            return None

        return self.twitch.get_games(id=self.game_id)[0]

    def get_metadata(self):
        """
        :return: StreamMetadata
        """
        return self.twitch.get_streams_metadata(user_id=self.user_id).data[0]
