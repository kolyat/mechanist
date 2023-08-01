from typing import Callable, Any
import json
import httpx
import pydantic

from . import settings, logger


class Base:
    """Bridge class between HTTP client and framework's API.

    :ivar client: HTTP client
    """
    def __init__(self, client):
        self.client = client

    @staticmethod
    def url(url_pattern: str, **kwargs) -> str:
        """Completes URL pattern with given arguments. Any additional arguments
        are ignored.

        self.url(
            '/platforms/{platform_id}/equipments/{equipment_id}',
            platform_id=17, equipment_id=41, something=113
        )
        Output: '/platforms/17/equipments/41'

        :param url_pattern: URL pattern
        :type url_pattern: str

        :param kwargs: arguments for URL pattern

        :return: completed URL
        :rtype: str
        """
        return url_pattern.format(**kwargs)

    @staticmethod
    def prepare_json(model: dict) -> dict:
        """Prepare request payload from pydantic model.
        Model should be converted to dict first with optional `exclude_none`
        and `exclude_unset` parameters.
        SomeModel().dict(exclude_none=True)

        :param model: model to be prepared
        :type model: dict

        :return: prepared payload
        :rtype: dict
        """
        return json.loads(json.dumps(model))

    @staticmethod
    def check_status_ok(request: Callable[..., Any], *args, **kwargs):
        """Checks status code of a response whether it is equal to 200 (OK).

        :param request: callable which makes HTTP request and returns response
        object
        :type request: Callable[..., Any]

        :return: response object if status code = 200 otherwise False
        """
        response = request(*args, **kwargs)
        if response.status_code == 200:
            return response
        else:
            return False


def get_http_client():
    """Get initialized HTTP client.

    :return: HTTP client object
    """
    return httpx.Client(
        base_url=settings.base_settings.api_url,
        event_hooks={
            'request': [logger.log_request],
            'response': [logger.log_response]}
    )
