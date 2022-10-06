from .input_converter import InputConverter
from .uart_proto_frame import ExtendedUARTProtocolFrame


class DefaultConverter(InputConverter):

    def __init__(self, csv_path, logger):
        super(DefaultConverter, self).__init__(logger)
        self._csv_path = csv_path

    def convert(self):
        frames = []

        with open(self._csv_path, "r") as csv_file:
            for i, line in enumerate(csv_file.readlines()):
                line = line.rstrip()

                try:
                    timestamp, label, data = line.split(",")

                    frame = ExtendedUARTProtocolFrame(float(timestamp), str(label), bytes.fromhex(data))
                    frames.append(frame)

                except ValueError:
                    self._logger.warning("Invalid line: [%d](%s)", i, line)
                    continue

        return frames
