import json
import logging
import requests

from django.conf import settings


class AbstractClientManager:

    client = None

    def check_client(self):
        assert self.client != None, 'Client not implemented'

    def get_client(self):
        self.check_client()
        return self.client


class AbstractClient:
    # after first call, we retry call as many as max_retry_attempt
    max_retry_attempt = 1
    headers = {}

    class Meta:
        always_use_production = False
        client_url = {
            'production': '',
            'development': ''
        }

    def __init__(self, name: str = None, max_retry_attempt: int = None):
        cls_name = self.__class__.__name__
        self.logger = logging.getLogger(cls_name)
        self.client_name = cls_name
        if max_retry_attempt is not None and max_retry_attempt >= 0:
            self.max_retry_attempt = max_retry_attempt

        assert hasattr(self, 'Meta'), (
            f'Class {cls_name} missing "Meta" attribute')
        assert hasattr(self.Meta, 'always_use_production'), (
            f'Class {cls_name} missing "Meta.always_use_production" attribute')
        assert hasattr(self.Meta, 'client_url'), (
            f'Class {cls_name} missing "Meta.client_url" attribute')

    def get_target_url(self):
        """
        Return target url based on settings
        """
        if getattr(self.Meta, 'always_use_production') or settings.PRODUCTION:
            return self.Meta.client_url['production']
        return self.Meta.client_url['development']

    def get_full_endpoint(self, uri: str):
        """
        Generate full url from uri
        """
        return f'{self.get_target_url()}{uri}'

    def get_max_retry_attempt(self):
        return self.max_retry_attempt

    def get_client_name(self):
        return self.client_name

    def set_header(self, key, value):
        self.headers[key] = value

    def post_headers(self):
        # immutable
        headers = dict(self.headers)
        headers['content-type'] = 'application/json'
        return headers

    def get_headers(self):
        # immutable
        headers = dict(self.headers)
        headers['content-type'] = 'application/json'
        headers['accept'] = 'application/json'
        return headers

    def is_success(self, request):
        """
        Check if request is success
        """
        code = request.status_code
        return code >= 200 and code < 300

    def is_attempt_exceeded(self, retry_attempt: int):
        """"
        Check if retry_attempt exceeded
        """
        return retry_attempt >= self.get_max_retry_attempt()

    def load_result(self, request):
        """
        Load result from request.
        Deserialize JSON to Dict.
        """
        return json.loads(request.content)

    def get(self, uri: str, **params):
        """
        Get request.
        Example of uri
        `/users`
        """
        return self.__request_get__(self.get_full_endpoint(uri), params)

    def post(self, uri: str, **data):
        """
        Post request.
        Example of uri
        `/users`
        """
        return self.__request_post__(self.get_full_endpoint(uri), data)

    def __request_get__(self, endpoint: str, params: dict = None, retry_attempt: int = 0):
        """
        Helper method to get request.
        If request failed/error, it will retry until
        max_retry_attempt.
        Return tuple of result and is_success
        """
        try:
            req = requests.get(endpoint, params=params,
                               headers=self.get_headers())
            res = self.load_result(req)

            if self.is_success(req):
                return (res, True)
            else:
                # log the message first
                log_message = f'{self.get_client_name()} failed to GET ({endpoint}): / attempt: {retry_attempt} / HTTP code:{req.status_code} \
                    / err msg: {res}'
                self.logger.error(log_message)

                if self.is_attempt_exceeded(retry_attempt):
                    return (res, False)
                else:
                    return self.__request_get__(endpoint, params, retry_attempt + 1)
        except requests.exceptions.RequestException as e:
            # something wrong with requests
            self.logger.exception(str(e))
            return (None, False)

    def __request_post__(self, endpoint: str, data: dict, retry_attempt: int = 0):
        """
        Helper method to post request.
        If request failed/error, it will retry until
        max_retry_attempt.self.user_manager.get_user(stateless_user.id)
        Return tuple of result and is_success
        """
        try:
            req = requests.post(endpoint, json.dumps(data),
                                headers=self.post_headers())
            res = self.load_result(req)

            if self.is_success(req):
                return (res, True)
            else:
                # log the message first
                log_message = f'{self.get_client_name()} failed to POST ({endpoint}): / retry attempt: {retry_attempt} / HTTP code:{req.status_code} \
                    / err msg: {res}'
                self.logger.error(log_message)

                if self.is_attempt_exceeded(retry_attempt):
                    return (res, False)
                else:
                    return self.__request_post__(endpoint, data, retry_attempt + 1)

        except requests.exceptions.RequestException as e:
            # something wrong with requests
            self.logger.exception(str(e))
            return (None, False)
