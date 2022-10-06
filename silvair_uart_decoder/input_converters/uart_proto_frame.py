import enum

import crcmod


class UARTProtocolFrame:

    PREAMBLE_LEN = 2
    LENGTH_LEN = 1
    COMMAND_LEN = 1
    CRC_LEN = 2

    LENGTH_IDX = 2
    COMMAND_IDX = 3
    DATA_IDX = 4

    def __init__(self, data_bytes):
        self.data_bytes = data_bytes or bytearray()

    @property
    def preamble(self):
        return self.data_bytes[:self.PREAMBLE_LEN]

    @property
    def length(self):
        return int(self.data_bytes[self.LENGTH_IDX])

    @property
    def command(self):
        return int(self.data_bytes[self.COMMAND_IDX])

    @property
    def data(self):
        return self.data_bytes[self.DATA_IDX:self.__crc_index]

    @property
    def crc(self):
        return int.from_bytes(self.data_bytes[self.__crc_index:], byteorder="little")

    @property
    def crc_data(self):
        return self.data_bytes[self.LENGTH_IDX:self.__crc_index]

    @property
    def __crc_index(self):
        return self.DATA_IDX + self.length

    def __repr__(self):
        params = {
            "length": self.length,
            "command": self.command,
            "data": self.data_bytes.hex()
        }
        return "len: {p[length]}, cmd: 0x{p[command]:02x}, data: `{p[data]}`".format(p=params)


class ExtendedUARTProtocolFrame(UARTProtocolFrame):

    def __init__(self, timestamp=0, label=None, data_bytes=None):
        super(ExtendedUARTProtocolFrame, self).__init__(data_bytes)
        self.timestamp = timestamp
        self.label = label or "-"

    def __repr__(self):
        super_repr = super(ExtendedUARTProtocolFrame, self).__repr__()

        params = {
            "timestamp": self.timestamp,
            "label": self.label
        }

        return "timestamp: {p[timestamp]}, label: {p[label]}, {s}".format(p=params, s=super_repr)


class ValidationResult(enum.IntEnum):
    VALID = 0
    INVALID_PREAMBLE = 1
    INVALID_DATA_LENGTH = 2
    INVALID_CRC = 3
    TOO_SHORT = 4


class UARTProtocolFrameValidator:

    crc_func = crcmod.mkCrcFun(poly=0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)

    PREAMBLE_FIRST_BYTE = 0xAA
    PREAMBLE_SECOND_BYTE = 0x55

    MIN_UART_PROTO_FRAME_LEN = 6
    MAX_DATA_LEN = 127

    @classmethod
    def validate(cls, frame):
        if len(frame.data_bytes) < cls.MIN_UART_PROTO_FRAME_LEN:
            return ValidationResult.TOO_SHORT

        if frame.preamble[0] != cls.PREAMBLE_FIRST_BYTE or frame.preamble[1] != cls.PREAMBLE_SECOND_BYTE:
            return ValidationResult.INVALID_PREAMBLE

        if frame.length > cls.MAX_DATA_LEN:
            return ValidationResult.INVALID_DATA_LENGTH

        if len(frame.data_bytes) != (cls.MIN_UART_PROTO_FRAME_LEN + frame.length):
            return ValidationResult.INVALID_DATA_LENGTH

        if frame.crc != cls.crc_func(frame.crc_data):
            return ValidationResult.INVALID_CRC

        return ValidationResult.VALID
