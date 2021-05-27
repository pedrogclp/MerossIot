import asyncio
import os
from random import randint

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.enums import OnlineStatus

EMAIL = os.environ.get('MEROSS_EMAIL') or "YOUR_MEROSS_CLOUD_EMAIL"
PASSWORD = os.environ.get('MEROSS_PASSWORD') or "YOUR_MEROSS_CLOUD_PASSWORD"


async def main():
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve the MSL120 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="msl120d", online_status=OnlineStatus.ONLINE)

    if len(plugs) < 1:
        print("No online msl120 smart bulbs found...")
    else:
        # Let's play with RGB colors. Note that not all light devices will support
        # rgb capabilities. For this reason, we first need to check for rgb before issuing
        # color commands.
        dev = plugs[0]

        # Update device status: this is needed only the very first time we play with this device (or if the
        #  connection goes down)
        await dev.async_update()
        # Check the current RGB color
        # current_color = dev.get_rgb_color()
        # current_temp = dev.get_color_temperature()
        # print(f"Currently, device {dev.name} is set to color (RGB) = {current_color} and {current_temp} temperature.")
        # Randomly chose a new color
        # Cargar el color que quiero.
        # rgb = randint(0, 255), randint(0, 255), randint(0, 255)
        # print(f"Chosen random color (R,G,B): {current_color}")
        # Blanco noche.
        await dev.async_turn_on(channel=0)
        await dev.async_set_light_color(luminance = 10)
        await dev.async_set_light_color(temperature = 20)
        # Blanco dia.
        # await dev.async_set_light_color(temperature = 100)
        # await dev.async_set_light_color(luminance = 100)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    # On Windows + Python 3.8, you should uncomment the following
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
