import waiting

from core.client import Base
from core.settings import base_settings
from . import models


class Device(Base):
    """Device management.
    """
    URL_DEVICE = '/platforms/{platform_id}/devices/{device_id}'
    URL_SCREENSHOT = '/platforms/{platform_id}/devices/screenshot'

    def get_device(self, device_id: int):
        """Get device info.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        response = self.client.get(
            self.url(self.URL_DEVICE,
                     platform_id=base_settings.platform_id,
                     device_id=device_id)
        )
        assert response.status_code == 200, \
            f'Could not get device {device_id} info'
        return response

    def put_device(self, device_id: int, payload: dict):
        """Put device info.

        :param device_id: device ID
        :type device_id: int

        :param payload: request payload
        :type payload: dict

        :return: response object
        """
        return self.client.put(
            self.url(self.URL_DEVICE,
                     platform_id=base_settings.platform_id,
                     device_id=device_id),
            json=payload
        )

    def get_screenshot_info(self, device_id: int):
        """Get info with URL of a screenshot.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        return self.client.get(
            self.url(self.URL_SCREENSHOT,
                     platform_id=base_settings.platform_id),
            params={'device_id': device_id}
        )

    def check_new_screenshot(self, device_id: int, ts: int):
        """Checks status code of a response whether it is equal to 200 (OK).

        :param device_id: device ID
        :type device_id: int

        :param ts: timestamp of previous screenshot
        :type ts: int

        :return: response object if new timestamp > given (old) timestamp
        """
        response = self.get_screenshot_info(device_id)
        new_ts = response.json().get('ts', 0)
        if new_ts > ts:
            return response
        else:
            return False

    def retrieve_screenshot(self, device_id: int) -> bytes:
        """Retrieve screenshot from a device.

        :param device_id: device ID
        :type device_id: int

        :return: screenshot in JPEG format
        :rtype: bytes
        """
        ts = self.get_screenshot_info(device_id).json().get('ts', 0)

        response = self.client.post(
            self.url(self.URL_SCREENSHOT,
                     platform_id=base_settings.platform_id),
            json={'device_id': device_id}
        )
        assert response.status_code == 200, \
            f'Problem occurred with screenshot request form device {device_id}'

        response = waiting.wait(
            lambda: self.check_new_screenshot(device_id, ts),
            timeout_seconds=30,
            sleep_seconds=base_settings.polling_interval,
            waiting_for=f'updated screenshot info for device {device_id}'
        )

        file_url = response.json()['file']
        screenshot = self.client.get(file_url).read()
        return screenshot

    def wait_device(self, device_id: int, status: str) -> bool:
        """Wait for device's status to be playback / pause / etc.

        :param device_id: device ID
        :type device_id: int

        :param status: status of a device (models.Status)
        :type status: str

        :return: True if status achieved
        :rtype: bool
        """
        return waiting.wait(
            lambda: self.get_device(
                device_id).json()['player_metrics']['status'] == status,
            timeout_seconds=120,
            sleep_seconds=base_settings.polling_interval,
            waiting_for=f'device {device_id} is {status}'
        )

    def cmd_escape_playback(self, device_id: int):
        """Send 'escape playback' command to device.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.ESCAPE,
                    event=models.ActionEvent.COMMAND
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not execute "escape" command for device {device_id}'
        return response

    def cmd_continue_playback(self, device_id: int):
        """Send 'continue playback' command to device.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.CONTINUE,
                    event=models.ActionEvent.COMMAND
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not execute "continue" command for device {device_id}'
        return response

    def cmd_restart_player(self, device_id: int):
        """Send 'restart player' command to device.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.RESTART,
                    event=models.ActionEvent.COMMAND
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not execute "restart" command for device {device_id}'
        return response

    def cmd_reboot_device(self, device_id: int):
        """Send 'reboot' command to device.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.REBOOT,
                    event=models.ActionEvent.COMMAND
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not execute "reboot" command for device {device_id}'
        return response

    def cmd_update_player(self, device_id: int):
        """Send 'update player' command to device.

        :param device_id: device ID
        :type device_id: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.NONE,
                    event=models.ActionEvent.UPDATE
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not execute "update" command for device {device_id}'
        return response

    def cmd_rotate_screen(self, device_id: int, degrees: int):
        """Send 'rotate screen' command to device.

        :param device_id: device ID
        :type device_id: int

        :param degrees: degree value (from models.Degree)
        :type degrees: int

        :return: response object
        """
        payload = self.prepare_json(models.DeviceUpdateModel(
            commands=[models.Command(
                action=models.Action(
                    command=models.ActionCommand.ROTATE_SCREEN,
                    event=models.ActionEvent.NONE,
                    params=[degrees]
                )
            )]
        ).model_dump(exclude_none=True))
        response = self.put_device(device_id, payload)
        assert response.status_code == 200, \
            f'Could not "rotate screen" to {degrees} for device {device_id}'
        return response
