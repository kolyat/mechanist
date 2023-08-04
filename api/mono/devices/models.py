from typing import Tuple, List, Optional, Literal
import datetime
import pydantic
from pydantic import AnyUrl, HttpUrl

from core import base, misc


class Degree(base.IntEnum):
    DEG_0 = 0
    DEG_90 = 90
    DEG_180 = 180
    DEG_270 = 270


class Status(base.StrEnum):
    OFFLINE = 'offline'
    PLAYBACK = 'playback'
    PAUSE = 'pause'
    EMPTY = 'empty'


class ActionCommand(base.StrEnum):
    NONE = ''
    ESCAPE = 'escape'
    CONTINUE = 'continue'
    RESTART = 'restart'
    REBOOT = 'reboot'
    SHUTDOWN = 'shutdown'
    ROTATE_SCREEN = 'rotateMainScreen'


class ActionEvent(base.StrEnum):
    NONE = ''
    COMMAND = 'command'
    UPDATE = 'update'


class RepeatUnit(base.StrEnum):
    SECOND = 'ss'
    MINUTE = 'mm'
    HOUR = 'hh'
    DAY = 'dd'
    WEEK = 'ww'
    MONTH = 'MM'
    YEAR = 'yy'


class Timing(pydantic.BaseModel):
    day_timings: List[Tuple[datetime.time, datetime.time]]


class DownloadInterval(pydantic.BaseModel):
    day_intervals: List[Tuple[datetime.time, datetime.time]]


class Screen(pydantic.BaseModel):
    h: int
    w: int
    rate: int
    x: int
    y: int
    depth: int


class Camera(pydantic.BaseModel):
    name: str
    active: bool


class WakeTimers(pydantic.BaseModel):
    count: int
    status: bool


class Qms(pydantic.BaseModel):
    type: str
    url: AnyUrl
    connected: bool


class Telnet(pydantic.BaseModel):
    enabled: bool
    port: int
    started: bool


class Extras(pydantic.BaseModel):
    qms: Qms
    telnet: Telnet


class AudioOut(pydantic.BaseModel):
    name: str
    selected: bool


class Capabilities(pydantic.BaseModel):
    notch: Optional[bool]
    bluetooth_supported: bool
    bluetooth: dict
    print: bool
    face_recognition: Optional[bool]
    model: Optional[str]
    name: Optional[str]
    manufacturer: Optional[str]
    root: Optional[bool]
    screens: List[Screen]
    cameras: Optional[List[Camera]]
    devices: dict
    serial_number: Optional[str]
    cpu_model: Optional[str]
    cpu_architecture: str
    cpu_cores: Optional[int]
    cpu_logical_cores: Optional[int]
    gpu_model: Optional[str]
    os: str
    os_version: str
    os_bit_capacity: int
    language: Optional[str]
    wake_timers: WakeTimers
    time_zone: datetime.timedelta
    admin: Optional[bool]
    version: str
    os_user: Optional[str]
    build: str
    bit: int
    extras: Extras
    audio_outs: Optional[List[AudioOut]]
    api_link: HttpUrl


class Metrics(pydantic.BaseModel):
    os_start_ts: int
    abr: Optional[bool]
    p_start_ts: int
    br: Optional[float]
    ls_current: Optional[float]
    battery_level: Optional[int]
    power_type: Optional[int]
    ram_used: int
    ram_total: Optional[int]
    ram_player: int
    up_time: int
    os_up_time: int
    space_available: int
    volume: dict


class PlayerMetrics(pydantic.BaseModel):
    status: Status
    project_id: int
    campaign_id: int
    need_to_download: int
    downloaded: int


class Interface(pydantic.BaseModel):
    name: str
    private_ip: str
    hardware_address: str
    net_mask: str
    is_active: bool

    # Validators
    _is_private_ip = pydantic.field_validator('private_ip')(misc.is_ip)
    _is_hardware_address = \
        pydantic.field_validator('hardware_address')(misc.is_mac)
    _is_net_mask = pydantic.field_validator('net_mask')(misc.is_ip)


class Network(pydantic.BaseModel):
    public_ip: str
    interfaces: List[Interface]


class CustomField(pydantic.BaseModel):
    id: int
    name: Optional[str]
    type: Optional[Literal['string', 'bool']]
    value: str


class Tag(pydantic.BaseModel):
    id: int
    name: str
    permission: int


class Campaign(pydantic.BaseModel):
    id: int
    name: str
    permission: int


class AdsZoneResolution(pydantic.BaseModel):
    height: int
    width: int


class Action(pydantic.BaseModel):
    command: ActionCommand = ActionCommand.NONE
    event: ActionEvent = ActionEvent.NONE
    params: list = []
    type: Literal['system'] = 'system'


class Repeat(pydantic.BaseModel):
    every: int
    unit: RepeatUnit


@base.optional
class Command(pydantic.BaseModel):
    id: Optional[int]
    action: Action
    execute_at: Optional[datetime.datetime]
    repeat: Optional[Repeat]


class TimingDate(pydantic.BaseModel):
    year: int
    month: int
    date: int
    timings: List[Timing]


class DeviceRetrieveModel(pydantic.BaseModel):
    id: int
    name: str
    group_id: int
    profile_id: Optional[int]
    timings: List[Timing]
    download_interval: List[DownloadInterval]
    monitoring: bool
    power_control: bool
    connected_at: datetime.datetime
    created_at: datetime.datetime
    skip_bulk_update: bool
    capabilities: Capabilities
    metrics: Metrics
    player_metrics: PlayerMetrics
    networks: Network
    custom_fields: List[CustomField]
    commands: Optional[List[Command]]
    tags: List[Tag]
    campaigns: List[Campaign]
    ads_zone_resolution: AdsZoneResolution
    timings_dates: List[TimingDate]
    permission: int


@base.optional
class DeviceUpdateModel(pydantic.BaseModel):
    ads_zone_resolution: AdsZoneResolution
    commands: List[Command]
    custom_fields: List[CustomField]
    dictionaries: list
    download_interval: List[DownloadInterval]
    is_only_profile_changed: bool
    monitoring: bool
    note: str
    p2p_mode: bool
    power_control: bool
    skip_bulk_update: bool
    storage: dict
    tags: List[int]
    timings: List[Timing]
    timing_dates: List[TimingDate]


class ScreenshotRetrieveModel(pydantic.BaseModel):
    file: HttpUrl
    ts: int
