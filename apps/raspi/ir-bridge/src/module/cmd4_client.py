"""
Cmd4Client module.
This module contains the Cmd4Client class, which is used to operate a device
through a provided device driver.
Classes:
    Cmd4Client: A client to send commands to a device driver.
Usage example:
    device_driver = SomeDeviceDriver()
    client = Cmd4Client(device_driver)
    client.operate_device("start")
"""

import devicedriver

class Cmd4Client:
    def __init__(self, device_driver):
        self.device_driver = device_driver

    def operate_device(self, command):
        if command == "start":
            self.device_driver.start()
        elif command == "stop":
            self.device_driver.stop()
        else:
            print("Unknown command")