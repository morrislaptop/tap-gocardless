import json
from datetime import datetime, timedelta
import backoff
import requests
from singer import metrics
from singer import utils

class Server5xxError(Exception):
    pass

class Server429Error(Exception):
    pass

class GocardlessClient:

    def __init__(self, access_token, user_agent):
        self.__access_token = access_token
        self.__user_agent = user_agent
        self.__session = requests.Session()
        self.__base_url = "https://api.gocardless.com" if "live_" in access_token else "https://api-sandbox.gocardless.com"

    def __exit__(self, exception_type, exception_value, traceback):
        self.__session.close()

    @backoff.on_exception(backoff.expo, (Server5xxError, ConnectionError, Server429Error), max_tries=7, factor=3)
    @utils.ratelimit(400, 60)
    def request(self, method, path=None, url=None, **kwargs):
        if not url and path:
            url = self.__base_url + path

        if 'endpoint' in kwargs:
            endpoint = kwargs['endpoint']
            del kwargs['endpoint']
        else:
            endpoint = None

        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Authorization'] = 'Bearer {}'.format(self.__access_token)
        kwargs['headers']['GoCardless-Version'] = '2015-07-06'

        if self.__user_agent:
            kwargs['headers']['User-Agent'] = self.__user_agent

        if method == 'POST':
            kwargs['headers']['Content-Type'] = 'application/json'

        with metrics.http_request_timer(endpoint) as timer:
            response = self.__session.request(method, url, **kwargs)
            timer.tags[metrics.Tag.http_status_code] = response.status_code

        if response.status_code >= 500:
            raise Server5xxError()

        #Use retry functionality in backoff to wait and retry if
        #response code equals 429 because rate limit has been exceeded
        if response.status_code == 429:
            raise Server429Error()

        response.raise_for_status()

        return response.json()

    def get(self, path, **kwargs):
        return self.request('GET', path=path, **kwargs)

    def post(self, path, **kwargs):
        return self.request('POST', path=path, **kwargs)
