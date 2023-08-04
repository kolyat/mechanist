import pydantic

from core import base


class Status(base.StrEnum):
    PLAYING = 'playing'
    PAUSED = 'paused'
    STOPPED = 'stopped'


@base.optional
class CampaignUpdateModel(pydantic.BaseModel):
    status: Status
