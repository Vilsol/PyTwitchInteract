import http.client, urllib.parse, json


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

    def upload_entitlement(self):
        pass  # TODO

    def get_games(self, id=None, name=None):
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

        return data['data']

    def get_streams(self, user_id=None, user_name=None, amount=20, stream_type='all', language=None, game_id=None, community_id=None):
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

        return PaginatedResponse(data, '/streams', query, self)

    def get_streams_metadata(self, user_id=None, user_name=None, amount=20, stream_type='all', language=None, game_id=None, community_id=None):
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

        return PaginatedResponse(data, '/streams/metadata', query, self)

    def get_users(self, id=None, login=None):
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

        return data['data']

    def get_users_follows(self, from_id=None, to_id=None, amount=20):
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

        return PaginatedResponse(data, '/users/follows', query, self)

    def update_user(self, description):
        query = {'description': description}

        response = self.do_request('/users', method='PUT', query=query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return data['data']

    def get_videos(self, id=None, user_id=None, game_id=None, amount=20, language=None, period='all', sort='time', video_type='all'):
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

        return PaginatedResponse(data, '/videos', query, self)


class PaginatedResponse:

    def __init__(self, data, endpoint, query, twitch):
        self.data = data['data']
        self.cursor = data['pagination']['cursor']
        self.endpoint = endpoint
        self.query = query
        self.twitch = twitch

    def next(self):
        new_query = self.query.copy()
        new_query['after'] = self.cursor
        return self.__re_request(new_query)

    def previous(self):
        new_query = self.query.copy()
        new_query['before'] = self.cursor
        return self.__re_request(new_query)

    def __re_request(self, new_query):
        response = self.twitch.do_request(self.endpoint, query=new_query)

        data = response.read()
        data = json.loads(data)

        if response.status < 200 or response.status > 299:
            raise Exception(data['message'])

        return PaginatedResponse(data, self.endpoint, self.query, self.twitch)
