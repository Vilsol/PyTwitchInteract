class Game:

    @staticmethod
    def from_json(data, twitch):
        return Game(
            data['id'],
            data['name'],
            data['box_art_url'],
            twitch
        )

    def __init__(self, game_id, name, box_art_url, twitch):
        """
        :param game_id: Game ID
        :param name: Game name
        :param box_art_url: Template URL for the game’s box art
        :param twitch: Twitch API instance
        """
        self.id = game_id
        self.name = name
        self.box_art_url = box_art_url
        self.twitch = twitch

    def get_streams(self):
        """
        :return: PaginatedResponse of Stream objects
        """
        return self.twitch.get_streams(game_id=self.id)

    def get_streams_metadata(self):
        """
        :return: PaginatedResponse of StreamMetadata objects
        """
        return self.twitch.get_streams_metadata(game_id=self.id)

    def get_videos(self):
        """
        :return: PaginatedResponse of Video objects
        """
        return self.twitch.get_videos(game_id=self.id)
