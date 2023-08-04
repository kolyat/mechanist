from typing import Optional
import pydantic

from core.settings import base_settings
from core.client import Base


class MultistepModel(pydantic.BaseModel):
    session_id: str = None
    login: Optional[str]
    password: Optional[str]


class MultistepAuth(Base):
    """Multistep authentication.
    """
    URL_START = '/auth/login/multi_step/start'
    URL_CHECK_LOGIN = '/auth/login/multi_step/check_login'
    URL_COMMIT_PASSWORD = '/auth/login/multi_step/commit_pwd'
    URL_FINISH = '/auth/login/multi_step/finish'
    URL_LOGOUT = '/users/logout'

    def __init__(self, client):
        super().__init__(client)
        self.session_id = None

    def start(self) -> None:
        """Step 1: get session ID.
        """
        response = self.client.post(self.URL_START)
        self.session_id = response.json()['session_id']

    def check_login(self, login: str) -> None:
        """Step 2: check login.

        :param login: user's login (`base_settings.user.email` by default)
        :type login: str
        """
        self.client.post(
            self.URL_CHECK_LOGIN,
            json={'session_id': self.session_id, 'login': login}
        )

    def commit_password(self, password: str) -> None:
        """Step 3: commit and check password.

        :param password: user's password (`base_settings.user.password` by
        default)
        :type password: str
        """
        self.client.post(
            self.URL_COMMIT_PASSWORD,
            json={'session_id': self.session_id, 'password': password}
        )

    def finish(self) -> None:
        """Step 4: send session ID and finish authentication procedure.
        """
        self.client.post(self.URL_FINISH, json={'session_id': self.session_id})

    def login(self,
              login: str = base_settings.user.email,
              password: str = base_settings.user.password) -> None:
        """Perform multistep authentication and log in to system.

        :param login: user's login (`base_settings.user.email` by default)
        :type login: str

        :param password: user's password (`base_settings.user.password` by
        default)
        :type password: str
        """
        self.start()
        self.check_login(login)
        self.commit_password(password)
        self.finish()

    def logout(self):
        """Log out from system.
        """
        self.client.post(self.URL_LOGOUT)
