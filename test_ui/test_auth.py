import pytest

from core import client
from core.settings import base_settings


class TestAuth(client.Case):
    @pytest.mark.run(order=1)
    def test_login(self):
        self.open(base_settings.platform_url)
        self.type('[name="ar-user-name"]', base_settings.user.email)
        self.click('[data-test="submit_login"]')
        self.type('[name="ar-user-password"]', base_settings.user.password)
        self.click('[data-test="submit_password"]')
        self.is_element_visible('img[alt="logo"]')
