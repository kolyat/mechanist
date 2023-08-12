import pytest
import allure

from api.mono.devices import device as device_api, models
from core.settings import base_settings
from core import improc


pytestmark = pytest.mark.parametrize('device_name,device_id',
                                     base_settings.devices)


@allure.epic('Player remote control')
class TestCommands:

    @allure.feature('Get screenshot from a device')
    def test_screenshot(self, api_client, device_name, device_id):
        device = device_api.Device(api_client)

        with allure.step(f'Retrieve screenshot from {device_name}'):
            screenshot = device.retrieve_screenshot(device_id)
            imp = improc.ImageProcessing()
            imp.load_target_from_bytes(screenshot)
            assert imp.is_target_image()

    @allure.feature('Exit and continue playback')
    def test_escape_and_continue_playback(self, api_client,
                                          device_name, device_id):
        device = device_api.Device(api_client)

        with allure.step(f'Escape {device_name} playback'):
            device.cmd_escape_playback(device_id)

        with allure.step(f'Waiting for {device_name} to be in "Pause" status'):
            device.wait_device(device_id, models.Status.PAUSE)

        with allure.step(f'Continue {device_name} playback'):
            device.cmd_continue_playback(device_id)

        with allure.step(f'Waiting for {device_name} to be in "Playback" '
                         f'status'):
            device.wait_device(device_id, models.Status.PLAYBACK)
