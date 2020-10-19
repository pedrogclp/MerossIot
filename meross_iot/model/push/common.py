from typing import Union

from meross_iot.model.enums import OnlineStatus
from meross_iot.model.shared import BaseDictPayload


class HardwareInfo(BaseDictPayload):
    def __init__(self, version=None, uuid=None, type=None, sub_type=None, mac_address=None, chip_time=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.version = version
        self.uuid = uuid
        self.type = type
        self.sub_type = sub_type
        self.mac_address = mac_address
        self.chip_type = chip_time


class FirmwareInfo(BaseDictPayload):
    def __init__(self, wifi_mac=None, version=None, user_id=None, server=None, port=None, inner_ip=None,
                 compile_time=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wifi_mac = wifi_mac
        self.version = version
        self.user_id = user_id
        self.server = server
        self.port = port
        self.inner_ip = inner_ip
        self.compile_time = compile_time


class TimeInfo(BaseDictPayload):
    def __init__(self, timezone=None, timestamp=None, time_rule=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timezone = timezone
        self.timestamp = timestamp
        self.time_rule = time_rule


class OnlineInfo(BaseDictPayload):
    def __init__(self, status: Union[str, int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(status, str):
            int_status = int(status)
        elif isinstance(status, int):
            int_status = status
        else:
            raise ValueError("Invalid online status")

        self.status = OnlineStatus(int_status)


class SystemInfo(BaseDictPayload):
    def __init__(self, hardware: dict, firmware: dict, time: dict, online: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hardware = HardwareInfo.from_dict(hardware)
        self.firmware = FirmwareInfo.from_dict(firmware)
        self.time = TimeInfo.from_dict(time)
        self.online = OnlineInfo.from_dict(online)

