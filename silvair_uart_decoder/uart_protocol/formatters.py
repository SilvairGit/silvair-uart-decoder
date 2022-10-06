import calendar
import contextlib
import time
import uuid
from datetime import timedelta, datetime, timezone

from .common import AttentionState, DeviceState, ErrorId, DFUStatus, DFUState, ModelName, OpcodeName, ELState, \
    PropertyID, TestStatus

UINT8_FMT = "0x{:02x}"
UINT16_FMT = "0x{:04x}"
UINT24_FMT = "0x{:06x}"
UINT32_FMT = "0x{:08x}"

TAI_UTC_DELTA_ZERO = 0xFF
TIME_ZONE_OFFSET_ZERO = 0x40
MESH_UNIX_EPOCH_DIFF = calendar.timegm(
    time.strptime("1999-12-31T23:59:28", "%Y-%m-%dT%H:%M:%S")
) - calendar.timegm(time.gmtime(0))
SECONDS_IN_15_MINUTES = 15 * 60


def mesh_tai_utc_delta_to_timedelta(tai_utc_delta: int) -> timedelta:
    return timedelta(seconds=tai_utc_delta - TAI_UTC_DELTA_ZERO)


def subsecond_to_seconds(subsecond: int) -> float:
    return subsecond / 256


def mesh_time_zone_offset_to_timedelta(time_zone_offset: int) -> timedelta:
    return timedelta(seconds=(time_zone_offset - TIME_ZONE_OFFSET_ZERO) * SECONDS_IN_15_MINUTES)


def default_fmter(value, fmt="{}"):
    return fmt.format(value)


def enum_fmter(value, fmt="{}", enum_base=None):
    res = default_fmter(value, fmt)

    with contextlib.suppress(ValueError):
        res += " ({})".format(enum_base(value).name)

    return res


def enum_model_name_fmter(value):
    return enum_fmter(value, UINT16_FMT, ModelName)


def enum_opcode_name_fmter(value):
    return enum_fmter(value, UINT16_FMT, OpcodeName)


def enum_meshmesreq1_opcode_name_fmter(value):
    if value <= 0xFF:
        return enum_fmter(value, UINT8_FMT, OpcodeName)
    elif value <= 0xFFFF:
        return enum_fmter(value, UINT16_FMT, OpcodeName)
    return enum_fmter(value, UINT32_FMT, OpcodeName)


def enum_attention_fmter(value):
    return enum_fmter(value, UINT8_FMT, AttentionState)


def enum_device_state_fmter(value):
    return enum_fmter(value, UINT8_FMT, DeviceState)


def enum_dfu_status_fmter(value):
    return enum_fmter(value, UINT8_FMT, DFUStatus)


def enum_dfu_state_fmter(value):
    return enum_fmter(value, UINT8_FMT, DFUState)


def enum_error_id_fmter(value):
    return enum_fmter(value, UINT8_FMT, ErrorId)


def enum_el_state_fmter(value):
    return enum_fmter(value, UINT8_FMT, ELState)


def enum_property_id_fmter(value):
    return enum_fmter(value, UINT16_FMT, PropertyID)


def enum_test_status_fmter(value):
    return enum_fmter(value, UINT8_FMT, TestStatus)

def list_fmter(value):
    return "[{}]".format(", ".join([str(v) for v in value]))


def struct_fmter(value):
    return "({})".format(", ".join(["{} = {}".format(k, v) for k, v in value.items() if not k.startswith("_")]))


def data_hexstr_fmter(value):
    return "[{}]`{}`".format(len(value), value.hex())


def data_ascii_fmter(value):
    return "{}".format(value.decode("ascii"))


def uuid_fmter(value):
    return "{}".format(uuid.UUID(bytes=bytes(value[::-1])))


def uint8_hex_fmter(value):
    return default_fmter(value, UINT8_FMT)


def uint16_hex_fmter(value):
    return default_fmter(value, UINT16_FMT)


def uint32_hex_fmter(value):
    return default_fmter(value, UINT32_FMT)


def uint8_hex_and_int_fmter(value):
    return "{} ({})".format(uint8_hex_fmter(value), value)


def uint16_hex_and_int_fmter(value):
    return "{} ({})".format(uint16_hex_fmter(value), value)


def uint32_hex_and_int_fmter(value):
    return "{} ({})".format(uint32_hex_fmter(value), value)


def mesh_date_fmter(value):
    milliseconds_date = subsecond_to_seconds(value["subsecond"])
    time_zone = mesh_time_zone_offset_to_timedelta(value["time_zone_offset"])
    sign_char = "-" if time_zone.total_seconds() < 0 else "+"
    full_recv_time = value["tai_seconds"] + MESH_UNIX_EPOCH_DIFF + int(
        time_zone.total_seconds()) + mesh_tai_utc_delta_to_timedelta(value["tai_utc_delta"]).total_seconds() - 42
    recv_date = datetime.fromtimestamp(full_recv_time, timezone(time_zone))
    return f"{recv_date.date().day}-{recv_date.date().month}-{recv_date.date().year} " \
           f"{recv_date.time().hour}:{recv_date.time().minute}:{recv_date.time().second + milliseconds_date} " \
           f"(UTC{sign_char}{time_zone.total_seconds() / (15 * 60)})"


def rtc_date_fmter(value):
    return f"{value.day}-{value.month}-{value.year} {value.hour}:{value.minute}:{value.second}.{value.millisecond}"
