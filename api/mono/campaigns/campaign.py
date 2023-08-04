from core.client import Base
from core.settings import base_settings
from . import models


class Campaign(Base):
    """Campaign management.
    """
    URL_CAMPAIGN = '/platforms/{platform_id}/campaign/{campaign_id}'

    def put_campaign(self, campaign_id: int, payload: dict):
        """Put campaign info.

        :param campaign_id: campaign ID
        :type campaign_id: int

        :param payload: request payload
        :type payload: dict

        :return: response object
        """
        return self.client.put(
            self.url(self.URL_CAMPAIGN,
                     platform_id=base_settings.platform_id,
                     campaign_id=campaign_id),
            json=payload
        )

    def play_campaign(self, campaign_id: int):
        """Play campaign.

        :param campaign_id: campaign ID
        :type campaign_id: int

        :return: response object
        """
        payload = self.prepare_json(models.CampaignUpdateModel(
                status=models.Status.PLAYING
        ).model_dump(exclude_none=True))
        response = self.put_campaign(campaign_id, payload)
        assert response.status_code == 200, \
            f'Could not play campaign {campaign_id}'
        return response

    def pause_campaign(self, campaign_id: int):
        """Pause campaign.

        :param campaign_id: campaign ID
        :type campaign_id: int

        :return: response object
        """
        payload = self.prepare_json(models.CampaignUpdateModel(
                status=models.Status.PAUSED
        ).model_dump(exclude_none=True))
        response = self.put_campaign(campaign_id, payload)
        assert response.status_code == 200, \
            f'Could not pause campaign {campaign_id}'
        return response
