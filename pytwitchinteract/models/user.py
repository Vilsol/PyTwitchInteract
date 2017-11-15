class User:

    @staticmethod
    def from_json(data, twitch):
        return User(
            data['id'],
            data['login'],
            data['display_name'],
            data['type'],
            data['broadcaster_type'],
            data['description'],
            data['profile_image_url'],
            data['offline_image_url'],
            data['view_count'],
            twitch
        )

    def __init__(self, user_id, login, display_name, user_type, broadcaster_type, description, profile_image_url, offline_image_url, view_count, twitch):
        """
        :param user_id:
        :param login:
        :param display_name:
        :param user_type:
        :param broadcaster_type:
        :param description:
        :param profile_image_url:
        :param offline_image_url:
        :param view_count:
        :param twitch: Twitch API instance
        """
        self.id = user_id
        self.login = login
        self.display_name = display_name
        self.type = user_type
        self.broadcaster_type = broadcaster_type
        self.description = description
        self.profile_image_url = profile_image_url
        self.offline_image_url = offline_image_url
        self.view_count = view_count
        self.twitch = twitch

    def get_stream(self):
        """
        :return: Stream
        """
        return self.twitch.get_streams(user_id=self.id).data[0]

    def get_stream_metadata(self):
        """
        :return: StreamMetadata
        """
        return self.twitch.get_streams_metadata(user_id=self.id).data[0]

    def get_followers(self):
        """
        :return: PaginatedResponse of Follow objects
        """
        return self.twitch.get_users_follows(to_id=self.id)

    def get_follows(self):
        """
        :return: PaginatedResponse of Follow objects
        """
        return self.twitch.get_users_follows(from_id=self.id)

    def get_videos(self):
        """
        :return: PaginatedResponse of Video objects
        """
        return self.twitch.get_videos(user_id=self.id)
