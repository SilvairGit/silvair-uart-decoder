import enum
from typing import List, Union

from .uart_proto_frame import UARTProtocolFrameValidator, ValidationResult, ExtendedUARTProtocolFrame


class ConverterStateMachine:
    PREAMBLE_BYTE_1 = 0xAA
    PREAMBLE_BYTE_2 = 0x55

    CRC_LEN = 2

    class _Result(enum.IntEnum):
        INVALID_PREAMBLE = 1
        PREAMBLE_BYTE_READ = 2
        PREAMBLE_READ = 3
        LENGTH_READ = 5
        COMMAND_CODE_READ = 6
        DATA_BYTE_READ = 7
        DATA_READ = 8
        CRC_BYTE_READ = 9
        CRC_READ = 10

    class _Iterator:
        def __init__(self, data):
            self._data = data
            self._current_idx = 0
            self._saved_idx = 0

        def __iter__(self):
            return self

        def save_idx(self):
            self._saved_idx = self._current_idx

        def restore_idx(self):
            self._current_idx = self._saved_idx

        def __next__(self):
            if self._current_idx >= len(self._data):
                raise StopIteration

            result = self._data[self._current_idx]
            self._current_idx += 1

            return result

    def __init__(self):
        self._process_handler = self._process_first_preamble_byte
        self._length = 0
        self._length_ctr = 0
        self._crc_ctr = 0
        self._frame = ExtendedUARTProtocolFrame()

    def reset(self):
        self._length = 0
        self._length_ctr = 0
        self._crc_ctr = 0
        self._frame = ExtendedUARTProtocolFrame()

    def _process_first_preamble_byte(self, byte):
        if byte != self.PREAMBLE_BYTE_1:
            return self._Result.INVALID_PREAMBLE

        self._frame.data_bytes.append(byte)
        self._process_handler = self._process_second_preamble_byte
        return self._Result.PREAMBLE_BYTE_READ

    def _process_second_preamble_byte(self, byte):
        self._frame.data_bytes.append(byte)

        if byte != self.PREAMBLE_BYTE_2:
            self._process_handler = self._process_first_preamble_byte
            return self._Result.INVALID_PREAMBLE

        self._process_handler = self._process_length
        return self._Result.PREAMBLE_READ

    def _process_length(self, byte):
        self._frame.data_bytes.append(byte)
        self._length = byte

        self._process_handler = self._process_cmd_code
        return self._Result.LENGTH_READ

    def _process_cmd_code(self, byte):
        self._frame.data_bytes.append(byte)
        self._process_handler = self._process_data if self._length else self._process_crc
        return self._Result.COMMAND_CODE_READ

    def _process_data(self, byte):
        self._frame.data_bytes.append(byte)

        if self._length_ctr < (self._length - 1):
            self._length_ctr += 1
            return self._Result.DATA_BYTE_READ

        self._process_handler = self._process_crc
        return self._Result.DATA_BYTE_READ

    def _process_crc(self, byte):
        self._frame.data_bytes.append(byte)

        if self._crc_ctr < (self.CRC_LEN - 1):
            self._crc_ctr += 1
            return self._Result.CRC_BYTE_READ

        self._process_handler = self._process_first_preamble_byte
        return self._Result.CRC_READ

    def process(self, bytes_list) -> List[ExtendedUARTProtocolFrame]:
        frames = []

        validator = UARTProtocolFrameValidator()
        _iter = self._Iterator(bytes_list)

        for timestamp, label, value in _iter:
            result = self._process_handler(value)

            if result == self._Result.PREAMBLE_BYTE_READ:
                self._frame.timestamp = timestamp
                self._frame.label = label

            elif result == self._Result.PREAMBLE_READ:
                _iter.save_idx()
                frames.append(self._frame)

            elif result == self._Result.CRC_READ:
                if validator.validate(self._frame) != ValidationResult.VALID:
                    _iter.restore_idx()

                self.reset()

        return frames

    def process_single(self, values) -> Union[ExtendedUARTProtocolFrame, None]:
        validator = UARTProtocolFrameValidator()

        timestamp, label, value = values

        result = self._process_handler(value)

        if result == self._Result.PREAMBLE_BYTE_READ:
            self._frame.timestamp = timestamp
            self._frame.label = label

        elif result == self._Result.CRC_READ:
            frame = self._frame

            self.reset()
            if validator.validate(frame) != ValidationResult.VALID:
                return

            return frame
