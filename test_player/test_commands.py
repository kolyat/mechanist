import pytest
import allure

from api.mono.devices import device as device_api, models
from core.settings import base_settings
from core import improc


@allure.epic('Player remote control')
@allure.feature('Get screenshot from a device')
@pytest.mark.parametrize('device_name,device_id', base_settings.devices)
def test_screenshot(api_client, device_name, device_id):
    device = device_api.Device(api_client)
    with allure.step('Retrieve screenshot from device'):
        screenshot = device.retrieve_screenshot(device_id)
        imp = improc.ImageProcessing()
        imp.load_from_bytes(screenshot)
        assert imp.is_source_image()


@allure.epic('Player remote control')
@allure.feature('Exit and continue playback')
@pytest.mark.parametrize('device_name,device_id', base_settings.devices)
def test_escape_and_continue_playback(api_client, device_name, device_id):
    device = device_api.Device(api_client)
    with allure.step('Escape playback'):
        device.cmd_escape_playback(device_id)
    with allure.step('Waiting for device to be in "Pause" status'):
        device.wait_device(device_id, models.Status.PAUSE)
    with allure.step('Continue playback'):
        device.cmd_continue_playback(device_id)
    with allure.step('Waiting for device to be in "Playback" status'):
        device.wait_device(device_id, models.Status.PLAYBACK)
