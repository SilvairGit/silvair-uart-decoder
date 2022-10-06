import unittest

from .uart_proto_frame import UARTProtocolFrame, ValidationResult, UARTProtocolFrameValidator


class UARTProtocolFrameTest(unittest.TestCase):

    def test_should_extract_uart_protocol_frame_fields_properly(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,                # Preamble
                                         0x04,                      # Length
                                         0x05,                      # Command
                                         0x11, 0x22, 0x33, 0x44,    # Data
                                         0xAA, 0xBB]))              # CRC

        self.assertSequenceEqual(frame.preamble, bytes([0xAA, 0x55]))
        self.assertEqual(frame.length, 4)
        self.assertEqual(frame.command, 5)
        self.assertSequenceEqual(frame.data, bytes([0x11, 0x22, 0x33, 0x44]))
        self.assertEqual(frame.crc, int.from_bytes(bytes([0xAA, 0xBB]), "little"))


class UARTProtocolFrameValidatorTest(unittest.TestCase):

    def setUp(self):
        self.validator = UARTProtocolFrameValidator()

    def test_should_return_INVALID_CRC_when_validate_frame_with_invalid_crc(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,                # Preamble
                                         0x04,                      # Length
                                         0x05,                      # Command
                                         0x11, 0x22, 0x33, 0x44,    # Data
                                         0xAA, 0xBB]))              # CRC

        self.assertEqual(ValidationResult.INVALID_CRC, self.validator.validate(frame))

    def test_should_return_TOO_SHORT_when_validate_frame_length_is_shorter_than_min_size(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x00,          # Length
                                         0x01,          # Command
                                                        # Data
                                         0x05]))        # CRC (invalid)
        self.assertEqual(ValidationResult.TOO_SHORT, self.validator.validate(frame))

    def test_should_return_INVALID_PREAMBLE_when_validate_frame_have_invalid_preamble1(self):
        frame = UARTProtocolFrame(bytes([0xA1, 0x55,    # Preamble (invalid)
                                         0x00,          # Length
                                         0x01,          # Command
                                                        # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_PREAMBLE, self.validator.validate(frame))

    def test_should_return_INVALID_PREAMBLE_when_validate_frame_have_invalid_preamble2(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x54,    # Preamble (invalid)
                                         0x00,          # Length
                                         0x01,          # Command
                                                        # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_PREAMBLE, self.validator.validate(frame))

    def test_should_return_INVALID_PREAMBLE_when_validate_frame_have_invalid_preamble3(self):
        frame = UARTProtocolFrame(bytes([0xA0, 0x54,    # Preamble (invalid)
                                         0x00,          # Length
                                         0x01,          # Command
                                                        # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_PREAMBLE, self.validator.validate(frame))

    def test_should_return_INVALID_DATA_LENGTH_when_validate_frame_length_is_bigger_than_max(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x80,          # Length (invalid)
                                         0x01,          # Command
                                                        # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_DATA_LENGTH, self.validator.validate(frame))

    def test_should_return_INVALID_DATA_LENGTH_when_validate_frame_data_length_is_different_than_value_length_field1(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x00,          # Length
                                         0x01,          # Command
                                         0x02,          # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_DATA_LENGTH, self.validator.validate(frame))

    def test_should_return_INVALID_DATA_LENGTH_when_validate_frame_data_length_is_different_than_value_length_field2(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x01,          # Length
                                         0x01,          # Command
                                         0x02, 0x04,    # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_DATA_LENGTH, self.validator.validate(frame))

    def test_should_return_INVALID_DATA_LENGTH_when_validate_frame_data_length_is_different_than_value_length_field3(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x02,          # Length
                                         0x01,          # Command
                                                        # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_DATA_LENGTH, self.validator.validate(frame))

    def test_should_return_INVALID_CRC_when_validate_frame_has_invalid_crc(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x02,          # Length
                                         0x01,          # Command
                                         0x02, 0x03,    # Data
                                         0x02, 0x04]))  # CRC

        self.assertEqual(ValidationResult.INVALID_CRC, self.validator.validate(frame))

    def test_should_return_VALID_when_validate_frame_is_valid(self):
        frame = UARTProtocolFrame(bytes([0xAA, 0x55,    # Preamble
                                         0x00,          # Length
                                         0x10,          # Command
                                                        # Data
                                         0x6E, 0x00]))  # CRC

        self.assertEqual(ValidationResult.VALID, self.validator.validate(frame))
