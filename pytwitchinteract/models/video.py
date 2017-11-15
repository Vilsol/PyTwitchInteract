class Video:

    @staticmethod
    def from_json(data, twitch):
        return Video(
            data['id'],
            data['user_id'],
            data['title'],
            data['description'],
            data['created_at'],
            data['published_at'],
            data['thumbnail_url'],
            data['view_count'],
            data['language'],
            twitch
        )

    def __init__(self, video_id, user_id, title, description, created_at, published_at, thumbnail_url, view_count, language, twitch):
        """
        :param video_id: ID of the video.
        :param user_id: ID of the user who owns the video.
        :param title: Title of the video.
        :param description: Description of the video.
        :param created_at: Date when the video was created.
        :param published_at: Date when the video was published.
        :param thumbnail_url: Template URL for the thumbnail of the video.
        :param view_count: Number of times the video has been viewed.
        :param language: Language of the video.
        :param twitch: Twitch API instance
        """
        self.id = video_id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.published_at = published_at
        self.thumbnail_url = thumbnail_url
        self.view_count = view_count
        self.language = language
        self.twitch = twitch

    def get_user(self):
        """
        :return: User
        """
        return self.twitch.get_users(id=self.user_id)[0]
