from typing import Tuple

from silvair_uart_decoder.input_converters import UARTProtocolFrameValidator, ValidationResult
from silvair_uart_decoder.input_converters.silvair_uart_state_machine import ConverterStateMachine
from silvair_uart_decoder.uart_protocol.common import CommandCode
from silvair_uart_decoder.uart_protocol.parsers import CommandParamParser


class ExtensionConverter:
    def __init__(self):
        self.state_machine = ConverterStateMachine()

    def convert(self, timestamp: float, data: int) -> Tuple[float, str]:
        frame = self.state_machine.process_single((timestamp, "None", data))

        if frame is None:
            return 0, ""

        command_param_parser = CommandParamParser()
        validator = UARTProtocolFrameValidator()

        if validator.validate(frame) != ValidationResult.VALID:
            return 0, ""

        command = CommandCode(frame.command)
        output_line = "{:30}".format(command.name)

        if frame.data:
            output_line += command_param_parser.parse(command, frame.data)

        return frame.timestamp, output_line
