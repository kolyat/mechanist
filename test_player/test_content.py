import time
import pytest
import allure

from api.mono.devices import device as device_api
from api.mono.campaigns import campaign as campaign_api
from core.settings import base_settings
from core import improc, misc


ATTEMPTS = 3

devices_mark = pytest.mark.parametrize('device_name,device_id',
                                       base_settings.devices)


@allure.epic('Content playback')
class TestContent:

    @staticmethod
    def check_playing_content(api_client, device_name, device_id,
                              campaign_name, data_file):
        passed = False
        campaign_id = base_settings.campaigns[campaign_name]

        device = device_api.Device(api_client)
        campaign = campaign_api.Campaign(api_client)
        imp = improc.ImageProcessing()
        fname = misc.get_path(__file__, 'data', data_file)

        with allure.step(f'Load source image "{fname}"'):
            imp.load_source_from_file(fname)
        with allure.step(f'Play campaign "{campaign_name}" #{campaign_id}'):
            campaign.play_campaign(campaign_id)
        time.sleep(5)
        with allure.step(f'Retrieve screenshot from {device_name} and '
                         f'compare with source image'):
            counter = ATTEMPTS
            while counter > 0 and not passed:
                screenshot = device.retrieve_screenshot(device_id)
                imp.load_target_from_bytes(screenshot)
                passed = imp.compare_images()
                counter -= 1
        with allure.step(f'Pause campaign "{campaign_name}" #{campaign_id}'):
            campaign.pause_campaign(campaign_id)
        return passed

    @allure.feature('JPEG image')
    @pytest.mark.parametrize(
        'campaign_name,data_file',
        (
            ('jpeg', 'jpeg.jpg'),
        )
    )
    @devices_mark
    def test_image(self, api_client, device_name, device_id,
                   campaign_name, data_file):
        assert self.check_playing_content(
            api_client, device_name, device_id, campaign_name, data_file
        )
