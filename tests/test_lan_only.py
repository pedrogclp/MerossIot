from timeit import default_timer as timer

from meross_iot.controller.device import BaseDevice
from meross_iot.controller.mixins.toggle import ToggleXMixin
from meross_iot.model.credentials import MerossCloudCreds
from meross_iot.manager import LocalMerossManager, MerossManager
from datetime import datetime
import asyncio

import logging

from meross_iot.model.enums import Namespace

l = logging.getLogger(__name__)


async def main():
    creds = MerossCloudCreds(token='', key='test', user_id='1111', user_email='', issued_on=datetime.utcnow())
    manager: MerossManager = LocalMerossManager(creds=creds, auto_reconnect=True, domain="192.168.1.2", port=8883, insecure_ssl=True)
    try:
        await manager.async_init()
        l.info("Manager init completed.")
        l.info("Waiting a bit...")
        await asyncio.sleep(10)

        l.info("Searching for devices...")
        devs = manager.find_devices()

        dev = devs[0]  # type: ToggleXMixin
        l.info("Found: %s", devs)

        async def test(namespace: Namespace, data: dict, device_internal_id: str):
            l.info(f"Recevied event: {namespace}.")
            l.info(f"State: {dev.is_on()}")

        dev.register_push_notification_handler_coroutine(test)
        await asyncio.sleep(30)

        """
        dev = devs[0]
        data = dev.get_sys_data()
        dev.async_turn_on()
        """
    finally:
        manager.close()
        print("Closed")

if __name__ == '__main__':
    asyncio.run(main())
