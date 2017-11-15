import json


class PaginatedResponse:

    def __init__(self, data, endpoint, query, mapping, twitch):
        self.data = twitch.process_array(data['data'], mapping)
        self.cursor = data['pagination']['cursor']
        self.endpoint = endpoint
        self.query = query
        self.mapping = mapping
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

        return PaginatedResponse(data, self.endpoint, self.query, self.mapping, self.twitch)
