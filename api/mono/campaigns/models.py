import pydantic

from core import base


class Status(base.StrEnum):
    PLAYING = 'playing'
    PAUSED = 'paused'
    STOPPED = 'stopped'


class CampaignUpdateModel(pydantic.BaseModel,
                          metaclass=base.PartialModelMetaclass):
    status: Status
