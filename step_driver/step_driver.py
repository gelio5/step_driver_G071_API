import serial
from serial import Serial
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE


class StepDriver:
    control_sum = b'\x00'
    start_byte = b'\xFD'
    stop_byte = b'\xFE'
    commands = {
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
        self.port = Serial(baudrate=115200,
                           bytesize=EIGHTBITS,
                           parity=PARITY_NONE,
                           stopbits=STOPBITS_ONE,
                           timeout=0.3)

    def set_port(self, port_name: str) -> None:
        self.port.port = port_name

    def ping(self):
        with self.port:
            message = self.start_byte + \
                      b'\x51' + \
                      self.commands['PING'] + \
                      self.control_sum + \
                      self.stop_byte
            self.port.write(message)
            try:
                answer = self.port.read(5)
                print(answer)
            except serial.SerialException as exception:
                print(exception)

    def find_address(self) -> None:
        with self.port:
            for address in range(256):
                message: bytes = self.start_byte + \
                                 address.to_bytes(length=1, byteorder='big', signed=False) + \
                                 self.commands['PING'] + \
                                 self.control_sum + \
                                 self.stop_byte
                self.port.reset_input_buffer()
                self.port.write(message)
                try:
                    answer = self.port.read(5)
                    if answer:
                        print(address)
                except serial.SerialTimeoutException as e:
                    print(e)
                    continue
