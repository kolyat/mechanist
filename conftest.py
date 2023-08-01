import pytest

from api.mono.auth import multistep
from core.client import get_http_client


@pytest.fixture(scope='session')
def api_client():
    auth = multistep.MultistepAuth(get_http_client())
    auth.login()
    yield auth.client
    auth.logout()
