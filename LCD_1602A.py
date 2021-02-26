import smbus
import time

MAX_WIDTH = 16

ENABLE = 0x04

BYTE_TYPE = {"data": 1,
             "command": 0, }

LINE_ADDRESS = {"1": 0x80,
                "2": 0xC0, }

BACKLIGHT_SWITCH = {"on": 0x08,
                    "off": 0x00, }

TIMING = {"pulse": 0.0005,
          "delay": 0.0005, }


class LCD:

    def __init__(self, i2c_address=0x27, i2c_detect_number=1):
        self.i2c_address = i2c_address
        self.bus = smbus.SMBus(i2c_detect_number)
        self.init_lcd()

    def __del__(self):
        self.init_lcd()

    def init_lcd(self):
        self._send_byte(0x33, BYTE_TYPE["command"])
        self._send_byte(0x32, BYTE_TYPE["command"])
        self._send_byte(0x06, BYTE_TYPE["command"])
        self._send_byte(0x0C, BYTE_TYPE["command"])
        self._send_byte(0x28, BYTE_TYPE["command"])
        self._send_byte(0x01, BYTE_TYPE["command"])
        time.sleep(TIMING["delay"])

    def show_message(self, message, line):
        if (line == 1) or (line == 2):
            show_line = LINE_ADDRESS[str(line)]
        else:
            show_line = LINE_ADDRESS["1"]
        self._send_byte(show_line, BYTE_TYPE["command"])

        message = message.ljust(MAX_WIDTH, " ")
        for i in range(MAX_WIDTH):
            self._send_byte(ord(message[i]), BYTE_TYPE["data"])

    def _send_byte(self, _bytes, mode):
        bits_high = mode | (_bytes & 0xF0) | BACKLIGHT_SWITCH["on"]
        self.bus.write_byte(self.i2c_address, bits_high)
        self._enable_lcd(bits_high)

        bits_low = mode | ((_bytes << 4) & 0xF0) | BACKLIGHT_SWITCH["on"]
        self.bus.write_byte(self.i2c_address, bits_low)
        self._enable_lcd(bits_low)

    def _enable_lcd(self, bits):
        time.sleep(TIMING["delay"])
        self.bus.write_byte(self.i2c_address, (bits | ENABLE))
        time.sleep(TIMING["pulse"])
        self.bus.write_byte(self.i2c_address, (bits & ~ENABLE))
        time.sleep(TIMING["delay"])
