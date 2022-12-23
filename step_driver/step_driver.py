from struct import pack

from pymodbus.client import ModbusSerialClient


class StepDriver:
    __commands: dict = {
        'MOVE': 0x01,
        'INIT': 0x03,
        'STOP': 0x04
    }

    def __init__(self, port: str, modbus_address: int, speed_to_search_home_pos: int = 5000):
        self.device = ModbusSerialClient(
            baudrate=115200,
            port=port,
            handle_local_echo=True
        )
        self.__current_pos: int = 0
        self.__status: bool = False
        self.__address = modbus_address
        self.__speed_to_search_home_pos = speed_to_search_home_pos

    def get_status(self) -> bool:
        return self.__status

    def search_home(self) -> None:
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['INIT'], 0, self.__speed_to_search_home_pos])

    def stop(self) -> None:
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['STOP']])

    def move_to_pos(self, position: int, speed: int) -> None:
        with self.device:
            self.device.write_registers(slave=self.__address,
                                        address=0,
                                        values=[self.__commands['MOVE'], speed, self.__speed_to_search_home_pos,
                                                position])

    def __update_info(self) -> None:
        with self.device:
            return self.device.read_holding_registers(unit=self.__address,
                                                      count=3,
                                                      address=8).registers
