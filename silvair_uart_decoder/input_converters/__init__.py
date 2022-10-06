import contextlib

from .default_converter import DefaultConverter
from .saleae_converter import SaleaeConverter
from .uart_proto_frame import UARTProtocolFrameValidator, ValidationResult


FORMAT_CONVERTERS = {
    "default": DefaultConverter,
    "saleae": SaleaeConverter,
}


def get_converter(name, *args, **kwargs):
    with contextlib.suppress(KeyError):
        return FORMAT_CONVERTERS[name](*args, **kwargs)
