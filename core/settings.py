import pydantic


class TestUser(pydantic.BaseModel):
    email: str
    password: str


class Settings(pydantic.BaseSettings):
    scheme: str = pydantic.Field(..., env='SCHEME')
    server_name: str = pydantic.Field(..., env='SERVER_NAME')
    api_version: str = pydantic.Field(..., env='API_VERSION')

    user_email: str = pydantic.Field(..., env='TEST_USER_EMAIL')
    user_password: str = pydantic.Field(..., env='TEST_USER_PASSWORD')

    platform_id: int = pydantic.Field(..., env='PLATFORM_ID')
    devices: list = pydantic.Field(..., env='DEVICES')

    polling_interval: int = pydantic.Field(..., env='POLLING_INTERVAL')

    class Config:
        env_file = f'.env'
        env_file_encoding = 'utf-8'

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
