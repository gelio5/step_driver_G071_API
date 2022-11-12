import serial
from serial import Serial
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE


class StepDriver:
    __control_sum = b'\x00'
    __start_byte = b'\xFD'
    __stop_byte = b'\xFE'
    __commands = {
        'PING': b'\x01',
        'INFO': b'\x02',
        'STATUS': b'\x03',
        # 'RETRANSLATE': b'\x04',
        'TOGGLE_POWER': b'\x05',
        'RUN': b'\x06',
        'SET_POS': b'\07',
        'STOP': b'\x08',
        'RUN_MANUAL': b'\x09'
    }

    def __init__(self):
        self.__port = Serial(baudrate=115200,
                             bytesize=EIGHTBITS,
                             parity=PARITY_NONE,
                             stopbits=STOPBITS_ONE,
                             timeout=0.3)
        self.__address = b'\x51'
        self.status = dict()
        self.__target_position = b'\x00\x00\x00\x00'
        self.__speed = b'\x00\x00',

    def set_port(self, port_name: str) -> None:
        self.__port.port = port_name

    def ping(self) -> None:
        with self.__port:
            message = self.__make_frame('PING')
            self.__port.write(message)
            try:
                answer = self.__port.read(5)
                print(answer)
            except serial.SerialException as exception:
                print(exception)

    def find_address(self) -> None:
        with self.__port:
            for address in range(256):
                message: bytes = self.__start_byte + \
                                 address.to_bytes(length=1, byteorder='big', signed=False) + \
                                 self.__commands['PING'] + \
                                 self.__control_sum + \
                                 self.__stop_byte
                self.__port.reset_input_buffer()
                self.__port.write(message)
                try:
                    answer = self.__port.read(5)
                    if answer:
                        self.set_address(address.to_bytes(length=1, byteorder='big', signed=False))
                        break
                except serial.SerialTimeoutException as e:
                    print(e)
                    continue

    def set_address(self, address: bytes) -> None:
        self.__address = address

    def __make_frame(self, command: str) -> bytes:
        match command:
            case 'PING' | 'STATUS' | 'INFO' | 'STOP':
                message: bytes = self.__start_byte + \
                                 self.__address + \
                                 self.__commands[command] + \
                                 self.__control_sum + \
                                 self.__stop_byte
            case _:
                raise Exception('Making frame for this command not realized!')
        return message

    def __parse_status(self, status: bytes) -> None:
        hex_status = status.hex()[6:-4]
        list_status = []
        for i in range(0, 21, 2):
            list_status.append(hex_status[i:i + 2])
        self.status = {
            'state_flags': list_status[0],
            'encoder': int(''.join(list_status[1:3]), base=16),
            'step_generator': int(''.join(list_status[3:7]), base=16),
            'opt_flags': list_status[7],
            'step_divider': list_status[8],
            'clearance': list_status[9]
        }

    def get_status(self) -> None:
        with self.__port:
            message = self.__make_frame('STATUS')
            self.__port.write(message)
            try:
                answer = self.__port.read(30)
                print(answer)
                self.__parse_status(answer)
            except serial.SerialException as exception:
                print(exception)

    def get_info(self) -> None:
        with self.__port:
            message = self.__make_frame('INFO')
            self.__port.write(message)
            try:
                answer = self.__port.read(30)
                print(answer)
            except serial.SerialException as exception:
                print(exception)

    def run(self, target_position: int, speed: int) -> None:
        self.__target_position = target_position.to_bytes(length=4, byteorder='big', signed=False)
        self.__speed = speed.to_bytes(length=2, byteorder='big', signed=False)
        with self.__port:

            message: bytes = self.__start_byte + \
                             self.__address + \
                             self.__commands['RUN'] + \
                             self.__target_position + \
                             self.__speed + \
                             self.__control_sum + \
                             self.__stop_byte
            self.__port.write(message)
            try:
                answer = self.__port.read(10)
                print(answer)
            except serial.SerialException as exception:
                print(exception)

    def stop(self) -> None:
        with self.__port:
            message = self.__make_frame('STOP')
            self.__port.write(message)
            try:
                answer = self.__port.read(10)
                print(answer.hex())
            except serial.SerialException as exception:
                print(exception)
