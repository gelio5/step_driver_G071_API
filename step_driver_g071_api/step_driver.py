"""Stepper driver using MODBUS communication protocol"""
import logging
from struct import unpack, pack
from time import sleep

from pymodbus.client import ModbusSerialClient

_logger = logging.getLogger(__name__)


class StepDriver:
    """**StepDriver**.

    :param port: Serial port used for communication;
    :param modbus_address: MODBUS address used for communication;
    :param speed_to_search_home_pos: (optional) Number of steps per second used for search home;

    Basic control of stepper motors based on the STM32G071 microcontroller using
    the Modbus protocol.

    Example::

        from step_driver_g071_api import StepDriver

        x_axis = StepDriver(port='COM3', modbus_address=4)
        x_axis.search_home()
        x_axis.move_to_pos(position=5000, speed=2000)

    P.S.: Max. simultaneously working objects <= 10.
        For simultaneously objects use moving methods in thread with pause between threads <= 50 ms.
    """
    __commands: dict = {
        'MOVE': 0x01,
        'INIT': 0x03,
        'STOP': 0x04
    }

    def __init__(self, port: str, modbus_address: int, speed_to_search_home_pos: int = 5000,
                 max_pos: int = None):
        self.device = ModbusSerialClient(baudrate=115200,
                                         port=port, )
        self.__current_pos: int = 0
        self.__status: bool = False
        self.__address = modbus_address
        self.__speed_to_search_home_pos = speed_to_search_home_pos
        self.__max_position = max_pos

    def __get_status(self) -> bool:
        return self.__status

    def search_home(self) -> None:
        """Search home position"""
        _logger.info('Searching home started')
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['INIT'], 0,
                                                self.__speed_to_search_home_pos])
            self.__update_info()
            while self.__status:
                sleep(0.5)
                self.__update_info()
            if self.__current_pos != 0:
                _logger.critical('Driver not in home position')
            else:
                _logger.info('Driver in home position')

    def stop(self) -> None:
        """Stop moving"""
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['STOP']])

    def move_to_pos(self, position: int, speed: int) -> None:
        """Move to position with set speed"""
        _logger.info('Moving to position %i started', position)
        if self.__max_position:
            if position > self.__max_position:
                raise ValueError(f"Position for {self.__address} driver must be <="
                                 f" {self.__max_position}")
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['MOVE'], speed,
                                                self.__speed_to_search_home_pos,
                                                *divmod(position, 0xFFFF)])
            self.__update_info()
            while self.__status:
                sleep(0.5)
                self.__update_info()
            if self.__current_pos != position:
                _logger.critical('Driver not in set position')
            else:
                _logger.info('Driver in set position')

    def go_to_pos_without_control(self, position: int, speed: int) -> None:
        """Move to position without control"""
        if self.__max_position:
            if position > self.__max_position:
                raise ValueError(f"Position for {self.__address} driver must be <="
                                 f" {self.__max_position}")
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['MOVE'], speed,
                                                self.__speed_to_search_home_pos,
                                                *divmod(position, 0xFFFF)[::-1]])

    def __update_info(self) -> None:
        """Update info about driver"""
        with self.device:
            received_data = self.device.read_holding_registers(slave=self.__address,
                                                               count=3,
                                                               address=8).registers
        self.__status = bool(received_data[0])
        self.__current_pos = unpack('<I', pack('<HH', *received_data[1:]))[0]

    status = property(fget=__get_status)
