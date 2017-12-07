from pytwitchinteract.utils import PaginatedResponse
from pytwitchinteract.models import *

import http.client
import json
import urllib.parse


class Twitch:

    def __init__(self, token=None, api_host='https://api.twitch.tv', api_base='/helix'):
        self.api_host = api_host
        self.api_base = api_base
        self.token = None

        if token is not None:
            self.authenticate(token)

    def authenticate(self, token):
        if token[:6] == 'oauth:':
            token = token[6:]

        if not token.lower()[:6] == 'bearer':
            token = 'Bearer ' + token

        self.token = token

    def do_request(self, endpoint, method='GET', query=None, headers=None, body=None):
        """
        Make a request to the Twitch API

        :param endpoint: Endpoint which to request
        :param method: The method to use
        :param query: Dictionary of query elements
        :param headers: Dictionary of headers
        :param body: Body string

        :return: The response
        """
        if query is None:
            query = {}

        if headers is None:
            headers = {}

        if len(query) > 0:
            query = urllib.parse.urlencode(query, doseq=True)
            endpoint = endpoint + '?' + query

        if self.token is not None:
            headers['Authorization'] = self.token

        if self.api_host[:5] == 'https':
            connection = http.client.HTTPSConnection(self.api_host[8:], port=443)
        else:
            connection = http.client.HTTPConnection(self.api_host[7:], port=80)

        connection.request(method, self.api_base + endpoint, body, headers)

        return connection.getresponse()

    def __get_array(self, data):
        if not isinstance(data, list):
            return [data]

        return data

    def process_array(self, data, mapping):
        result = []

        for i in data:
            result.append(mapping.from_json(i, self))

        return result

    def upload_entitlement(self):
        pass  # TODO

    def get_games(self, id=None, name=None):
        """
        Gets game information by game ID or name

        :param id: Game ID.
            At most 100 id values can be specified
        :param name: Game name. The name must be an exact match.
            For instance, "Pokemon" will not return a list of Pokemon games.
            At most 100 name values can be specified

        :return: Array of Game objects
        """
        if id is None and name is None:
            raise Exception("You must specify one of id or name")

        query = {}

        if id is not None:
            query['id'] = self.__get_array(id)

        if name is not None:
            query['name'] = self.__get_array(name)

        response = self.do_request('/games', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return self.process_array(data['data'], Game)

    def get_streams(self, user_id=None, user_name=None, amount=20, stream_type='all', language=None, game_id=None, community_id=None):
        """
        Gets information about active streams.
        Streams are returned sorted by number of current viewers, in descending order.
        Across multiple pages of results, there may be duplicate or missing streams, as viewers join and leave streams.

        :param user_id: Returns streams broadcast by one or more specified user IDs.
            You can specify up to 100 IDs
        :param user_name: Returns streams broadcast by one or more specified user login names.
            You can specify up to 100 names
        :param amount: Maximum number of objects to return.
            Maximum: 100. Default: 20
        :param stream_type: Stream type: "all", "live", "vodcast".
            Default: "all"
        :param language: Stream language.
            You can specify up to 100 languages
        :param game_id: Returns streams broadcasting a specified game ID.
            You can specify up to 100 IDs
        :param community_id: Returns streams in a specified community ID.
            You can specify up to 100 IDs

        :return: PaginatedResponse of Stream objects
        """
        query = {}

        if user_id is not None:
            query['user_id'] = self.__get_array(user_id)

        if user_name is not None:
            query['user_name'] = self.__get_array(user_name)

        query['amount'] = amount
        query['type'] = stream_type

        if language is not None:
            query['language'] = self.__get_array(language)

        if game_id is not None:
            query['game_id'] = self.__get_array(game_id)

        if community_id is not None:
            query['language'] = self.__get_array(community_id)

        response = self.do_request('/streams', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return PaginatedResponse(data, '/streams', query, Stream, self)

    def get_streams_metadata(self, user_id=None, user_name=None, amount=20, stream_type='all', language=None, game_id=None, community_id=None):
        """
        Gets metadata information about active streams playing Overwatch or Hearthstone.
        Streams are sorted by number of current viewers, in descending order.
        Across multiple pages of results, there may be duplicate or missing streams, as viewers join and leave streams.

        :param user_id: Returns streams broadcast by one or more of the specified user IDs.
            You can specify up to 100 IDs
        :param user_name: Returns streams broadcast by one or more of the specified user login names.
            You can specify up to 100 names
        :param amount: Maximum number of objects to return.
            Maximum 100. Default: 20
        :param stream_type: Stream type: "all", "live", "vodcast".
            Default: "all"
        :param language: Stream language.
            You can specify up to 100 languages
        :param game_id: Returns streams broadcasting the specified game ID.
            You can specify up to 100 IDs
        :param community_id: Returns streams in a specified community ID.
            You can specify up to 100 IDs

        :return: PaginatedResponse of StreamMetadata objects
        """
        query = {}

        if user_id is not None:
            query['user_id'] = self.__get_array(user_id)

        if user_name is not None:
            query['user_name'] = self.__get_array(user_name)

        query['amount'] = amount
        query['type'] = stream_type

        if language is not None:
            query['language'] = self.__get_array(language)

        if game_id is not None:
            query['game_id'] = self.__get_array(game_id)

        if community_id is not None:
            query['language'] = self.__get_array(community_id)

        response = self.do_request('/streams/metadata', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return PaginatedResponse(data, '/streams/metadata', query, StreamMetadata, self)

    def get_users(self, id=None, login=None):
        """
        Gets information about one or more specified Twitch users.
        Users are identified by optional user IDs and/or login name.
        If neither a user ID nor a login name is specified, the user is looked up by Bearer token.

        :param id: User ID.
            Multiple user IDs can be specified.
            Limit: 100
        :param login: User login name.
            Multiple login names can be specified.
            Limit: 100

        :return: Array of User objects
        """
        if id is None and login is None:
            raise Exception("You must specify one of id or login")

        query = {}

        if id is not None:
            query['id'] = self.__get_array(id)

        if login is not None:
            query['login'] = self.__get_array(login)

        response = self.do_request('/users', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return self.process_array(data['data'], User)

    def get_users_follows(self, from_id=None, to_id=None, amount=20):
        """
        Gets information on follow relationships between two Twitch users.
        Information returned is sorted in order, most recent follow first.
        This can return information like "who is lirik following," "who is following lirik,” or “is user X following user Y.”

        :param from_id: User ID.
            The request returns information about users who are being followed by the from_id user
        :param to_id: User ID.
            The request returns information about users who are following the to_id user
        :param amount: Maximum number of objects to return.
            Maximum: 100. Default: 20

        :return: PaginatedResponse of Follow objects
        """
        if from_id is None and to_id is None:
            raise Exception("You must specify one of from_id or to_id")

        query = {}

        if from_id is not None:
            query['from_id'] = self.__get_array(from_id)

        if to_id is not None:
            query['to_id'] = self.__get_array(to_id)

        query['amount'] = amount

        response = self.do_request('/users/follows', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return PaginatedResponse(data, '/users/follows', query, Follow, self)

    def update_user(self, description):
        """
        Updates the description of a user specified by a Bearer token.

        :param description: New description

        :return: User object
        """
        query = {'description': description}

        response = self.do_request('/users', method='PUT', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return User.from_json(data['data'][0], self)

    def get_videos(self, id=None, user_id=None, game_id=None, amount=20, language=None, period='all', sort='time', video_type='all'):
        """
        Gets video information by video ID (one or more), user ID (one only), or game ID (one only).

        :param id: ID of the video being queried.
            If this is specified, you cannot use any other query parameters.
            Limit: 100
        :param user_id: ID of the user who owns the video.
            Limit 1
        :param game_id: ID of the game the video is of.
            Limit 1
        :param amount: Number of values to be returned when getting videos by user or game ID.
            Limit: 100. Default: 20
        :param language: Language of the video being queried.
            Limit: 1
        :param period: Period during which the video was created.
            Valid values: "all", "day", "month", and "week". Default: "all".
        :param sort: Sort order of the videos.
            Valid values: "time", "trending", and "views". Default: "time".
        :param video_type: Type of video.
            Valid values: "all", "upload", "archive", and "highlight". Default: "all".

        :return: PaginatedResponse of Video objects
        """
        if id is None and user_id is None and game_id is None:
            raise Exception("You must specify one of id, user_id or game_id")

        query = {}

        if id is not None:
            query['id'] = self.__get_array(id)

        if user_id is not None:
            query['user_id'] = self.__get_array(user_id)

        if game_id is not None:
            query['game_id'] = self.__get_array(game_id)

        query['amount'] = amount

        if language is not None:
            query['language'] = language

        if period is not None:
            query['period'] = period

        if sort is not None:
            query['sort'] = sort

        if video_type is not None:
            query['type'] = video_type

        response = self.do_request('/videos', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return PaginatedResponse(data, '/videos', query, Video, self)
