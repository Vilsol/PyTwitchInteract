class Follow:

    @staticmethod
    def from_json(data, twitch):
        return Follow(
            data['from_id'],
            data['to_id'],
            data['followed_at'],
            twitch
        )

    def __init__(self, from_id, to_id, followed_at, twitch):
        """
        :param from_id: ID of the user following the to_id user.
        :param to_id: ID of the user being followed by the from_id user.
        :param followed_at: Date and time when the from_id user followed the to_id user.
        :param twitch: Twitch API instance
        """
        self.from_id = from_id
        self.to_id = to_id
        self.followed_at = followed_at
        self.twitch = twitch

    def get_from_user(self):
        """
        :return: User
        """
        return self.twitch.get_users(id=self.from_id)

    def get_to_user(self):
        """
        :return: User
        """
        return self.twitch.get_users(id=self.to_id)
