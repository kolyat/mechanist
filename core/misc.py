from typing import Union
import os.path
import httpx
import validators

from . import settings


def dict_to_text(dic: Union[dict, httpx.Cookies]) -> str:
    """Transform dictionary to multiline text.

    {'key1': 'value1', 'key2': 'value2'}
    to
    key1: value1
    key2: value2

    :param dic: dictionary object
    :type dic: Union[dict, httpx.Cookies]

    :return: multiline text
    :rtype: str
    """
    return '\n'.join([f'{k}: {v}' for k, v in dic.items()])


def is_ip(ip: str) -> str:
    """Check whether given string is IPv4 or IPv6.

    :param ip: IP address
    :type ip: str

    :return: IP address
    :rtype: str

    :raises AssertionError when `ip` is not IPv4/6
    """
    ipv4 = False
    if validators.ipv4(ip) is True:
        ipv4 = True
    ipv6 = False
    if validators.ipv6(ip) is True:
        ipv6 = True
    if ipv4 or ipv6:
        return ip
    else:
        assert False


def is_mac(mac: str) -> str:
    """Check whether given string is MAC address.

    :param mac: MAC address
    :type mac: str

    :return: MAC address
    :rtype: str

    :raises AssertionError when `mac` is not MAC address
    """
    if validators.mac_address(mac) is True:
        return mac
    else:
        assert False


def full_url(method):
    def wrapper(*args, **kwargs):
        new_args = list(args)
        # Construct full URL from relative
        url = settings.base_settings.api_url + args[2]
        new_args[2] = url
        return method(*new_args, **kwargs)
    return wrapper


def get_path(sfile: str, *args) -> str:
    """Construct absolute path of a destination file based on
    source file path.

    :param sfile: source file (must be always __file__)
    :type sfile: str

    :param args: parts of destination file (e.g., 'subdir', 'some.file')

    :return: absolute destination path
    :rtype: str
    """
    return os.path.join(os.path.dirname(os.path.abspath(sfile)), *args)


def get_tmp_path(*args) -> str:
    """Construct absolute path of a destination file based on
    project temporary path.

    :param args: parts of destination file (e.g., 'some.file')

    :return: absolute destination path
    :rtype: str
    """
    return os.path.join(settings.base_settings.tmp_path, *args)
