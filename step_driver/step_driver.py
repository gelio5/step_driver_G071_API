import logging
from struct import unpack, pack

from pymodbus.client import ModbusSerialClient

_logger = logging.getLogger(__name__)


class StepDriver:
    """**StepDriver**.

    :param port: Serial port used for communication;
    :param modbus_address: MODBUS address used for communication;
    :param speed_to_search_home_pos: (optional) Number of steps per second used for search home;

    Basic control of stepper motors based on the STM32G071 microcontroller using the Modbus protocol.

    Example::

        from step_driver import StepDriver

        x_axis = StepDriver(port='COM3', modbus_address=4)
        x_axis.search_home()
        x_axis.move_to_pos(position=5000, speed=2000)
    """
    __commands: dict = {
        'MOVE': 0x01,
        'INIT': 0x03,
        'STOP': 0x04
    }

    def __init__(self, port: str, modbus_address: int, speed_to_search_home_pos: int = 5000):
        self.device = ModbusSerialClient(
            baudrate=115200,
            port=port, )
        self.__current_pos: int = 0
        self.__status: bool = False
        self.__address = modbus_address
        self.__speed_to_search_home_pos = speed_to_search_home_pos

    def get_status(self) -> bool:
        return self.__status

    def search_home(self) -> None:

        _logger.info('Searching home started')
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['INIT'], 0, self.__speed_to_search_home_pos])
            self.__update_info()
            while self.__status:
                self.__update_info()
            print(self.__current_pos)
            if self.__current_pos != 0:
                _logger.critical('Driver not in home position')
            else:
                _logger.info('Driver in home position')

    def stop(self) -> None:
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['STOP']])

    def move_to_pos(self, position: int, speed: int) -> None:
        _logger.info(f'Moving to position {position} started')
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=2,
                                        values=[self.__commands['MOVE'], speed, self.__speed_to_search_home_pos,
                                                position])
            self.__update_info()
            while self.__status:
                self.__update_info()
            if self.__current_pos != position:
                _logger.critical('Driver not in set position')
            else:
                _logger.info('Driver in set position')

    def go_to_pos_without_control(self, position: int, speed: int) -> None:
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['MOVE'], speed, self.__speed_to_search_home_pos,
                                                position])

    def __update_info(self) -> None:
        with self.device:
            received_data = self.device.read_holding_registers(slave=self.__address,
                                                               count=3,
                                                               address=8).registers
            print(received_data)
        self.__status = bool(received_data[0])
        self.__current_pos = unpack('<I', pack('<HH', *received_data[1:]))[0]

    status = property(fget=get_status)
