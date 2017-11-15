class StreamMetadata:

    @staticmethod
    def from_json(data, twitch):
        return StreamMetadata(
            data['user_id'],
            data['game_id'],
            data['overwatch'],
            data['hearthstone'],
            twitch
        )

    def __init__(self, user_id, game_id, overwatch, hearthstone, twitch):
        """
        :param user_id:
        :param game_id: ID of the game being played on the stream:
            488552 (Overwatch),
            138585 (Hearthstone),
            or null (neither Overwatch nor Hearthstone metadata is available).
        :param overwatch: Object containing the Overwatch metadata, if available; otherwise, None.
        :param hearthstone: Object containing the Hearthstone metadata, if available; otherwise, None.
        :param twitch: Twitch API instance
        """
        self.user_id = user_id
        self.game_id = game_id
        self.overwatch = overwatch
        self.hearthstone = hearthstone
        self.twitch = twitch

    def get_stream(self):
        """
        :return: Stream
        """
        return self.twitch.get_streams(user_id=self.user_id).data[0]

    def get_game(self):
        """
        :return: Game or None
        """
        if self.game_id is None:
            return None

        return self.twitch.get_games(id=self.game_id)
