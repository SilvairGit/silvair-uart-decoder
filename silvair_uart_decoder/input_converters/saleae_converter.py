import re

from collections import defaultdict

from .input_converter import InputConverter
from .silvair_uart_state_machine import ConverterStateMachine

RADIX_FORMAT_REGEX = {
    "DEC": re.compile(r'^(\d+.\d+),(.*),(\d+)$'),
    "HEX": re.compile(r'^(\d+.\d+),(.*),(0x[0-9a-fA-F]{2})$'),
    "ASCII_HEX": re.compile(r'^(\d+.\d+),(.*),.*\s\((0x[0-9a-fA-F]{2})\)$'),
}


def detect_radix_format(line):
    for radix_format, regex in RADIX_FORMAT_REGEX.items():
        if not regex.match(line):
            continue

        return radix_format, regex


def parse_line(line, radix_format, regex):
    match = regex.match(line)
    if match is None:
        return None

    timestamp, label, value = match.groups()

    return float(timestamp), str(label), int(value, 10 if radix_format == "DEC" else 16)


class SaleaeConverter(InputConverter):

    def __init__(self, csv_path, logger):
        super(SaleaeConverter, self).__init__(logger)
        self._csv_path = csv_path

    def convert(self):
        state_machine = ConverterStateMachine()

        sorted_bytes_lists = defaultdict(list)

        with open(self._csv_path) as csv_file:
            radix_format, regex = None, None

            for i, line in enumerate(csv_file.readlines()):

                if i == 0 and detect_radix_format(line) is None:
                    self._logger.info("Skipped header line.")
                    continue

                if radix_format is None:
                    result = detect_radix_format(line)
                    if result is None:
                        self._logger.error("Invalid input file format.")
                        return []

                    radix_format, regex = result

                parsed_line = parse_line(line, radix_format, regex)

                if parse_line is None:
                    self._logger.warning("Invalid line: [%d](%s)`", i, line)
                    continue

                timestamp, label, value = parsed_line

                bytes_list = sorted_bytes_lists[label]
                bytes_list.append(parsed_line)

        frames = []

        for sorted_bytes_list in sorted_bytes_lists.values():
            state_machine.reset()
            frames.extend(state_machine.process(sorted_bytes_list))

        return frames
