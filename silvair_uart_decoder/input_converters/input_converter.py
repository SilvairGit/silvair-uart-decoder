
class InputConverter:

    def __init__(self, logger):
        self._logger = logger

    def convert(self):
        """
        Convert input format to extended UART protocol frames.

        :rtype: list<ExtendedUARTProtocolFrame>
        :return: List of extended UART protocol frames.
        """
        raise NotImplementedError
