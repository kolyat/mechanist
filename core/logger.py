from typing import Union
import logging
import httpx
import allure

from . import misc


def attach(obj: Union[httpx.Request, httpx.Response]) -> None:
    """Attach data to request/response.

    :param obj: request or response object
    :type obj: Union[httpx.Request, httpx.Response]
    """
    headers = misc.dict_to_text(obj.headers)
    logging.debug(str(obj.headers))
    allure.attach(headers, attachment_type=allure.attachment_type.TEXT)
    try:
        cookies = misc.dict_to_text(obj.cookies)
        logging.debug(str(cookies))
        allure.attach(cookies, attachment_type=allure.attachment_type.TEXT)
    except Exception as e:
        logging.debug(str(e))
    try:
        content = obj.read()
        logging.debug(str(content))
        if obj.headers.get('content-type', None):
            content_type = obj.headers['content-type']
            attachment_type = None
            if 'text/plain' in content_type:
                attachment_type = allure.attachment_type.TEXT
            elif 'text/html' in content_type:
                attachment_type = allure.attachment_type.HTML
            elif 'application/json' in content_type:
                attachment_type = allure.attachment_type.JSON
            elif 'image/jpeg' in content_type:
                attachment_type = allure.attachment_type.JPG
            else:
                pass
            if attachment_type:
                allure.attach(content, attachment_type=attachment_type)
    except Exception as e:
        logging.debug(str(e))


def log_request(request: httpx.Request) -> None:
    """Log request to Allure.

    :param request: client's HTTP request
    :type request: httpx.Request
    """
    with allure.step(f'{request.method} {request.url}'):
        attach(request)


def log_response(response: httpx.Response) -> None:
    """Log response to Allure.

    :param response: server's response
    :type response: httpx.Response
    """
    with allure.step(
            f'{response.status_code} {response.reason_phrase} {response.url}'
    ):
        attach(response)
