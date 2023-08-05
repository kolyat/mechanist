import os.path
import pickle
import filelock
import pytest

from api.mono.auth import multistep
from core.client import get_http_client


@pytest.fixture(scope='session')
def api_client(tmp_path_factory, worker_id):
    auth = multistep.MultistepAuth(get_http_client())
    if worker_id != "master":
        session_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'session.cookies'
        )
        with filelock.FileLock(session_file + '.lock'):
            if os.path.isfile(session_file):
                with open(session_file, 'rb+') as f:
                    cookies = pickle.load(f)
                auth.client.cookies.jar._cookies.update(cookies)
            else:
                auth.login()
                with open(session_file, 'wb') as f:
                    pickle.dump(auth.client.cookies.jar._cookies, f)
        yield auth.client
    else:
        auth.login()
        yield auth.client
        auth.logout()
