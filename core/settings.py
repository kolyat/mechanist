import os
import pydantic
import pydantic_settings


class TestUser(pydantic.BaseModel):
    email: str
    password: str


class Settings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    scheme: str
    server_name: str
    api_version: str

    user_email: str
    user_password: str

    platform_id: int
    devices: list
    campaigns: dict

    polling_interval: int

    tmp_path: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tmp'
    )

    @property
    def api_url(self) -> str:
        """Get base URL of server's API.

        :return: base API URL
        :rtype: str
        """
        return f'{self.scheme}://api.{self.server_name}/v{self.api_version}'

    @property
    def user(self) -> TestUser:
        """Get test user's data.

        :return: test user
        :rtype: pydantic.BaseModel
        """
        return TestUser(email=self.user_email, password=self.user_password)


base_settings = Settings()
if not os.path.exists(base_settings.tmp_path):
    os.mkdir(base_settings.tmp_path)
