from construct import Adapter

from .formatters import enum_model_name_fmter, enum_opcode_name_fmter, enum_attention_fmter, enum_device_state_fmter, \
    enum_dfu_status_fmter, enum_dfu_state_fmter, enum_error_id_fmter, list_fmter, struct_fmter, data_hexstr_fmter, \
    data_ascii_fmter, uuid_fmter, uint8_hex_fmter, uint16_hex_fmter, uint32_hex_fmter, uint8_hex_and_int_fmter, \
    uint16_hex_and_int_fmter, uint32_hex_and_int_fmter, rtc_date_fmter, mesh_date_fmter, \
    enum_meshmesreq1_opcode_name_fmter, enum_el_state_fmter, enum_property_id_fmter, enum_test_status_fmter


class ValueObj:

    def __init__(self, value, fmter=None):
        self.value = value
        self._fmter = fmter

    def __hash__(self):
        if isinstance(self, list) or isinstance(self, dict):
            raise NotImplementedError

        return self.value

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        return self.value == other.value

    def __repr__(self):
        if self._fmter:
            return self._fmter(self.value)

        return self.value


class AttentionAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_attention_fmter)


class DeviceStateAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_device_state_fmter)


class DFUStatusAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_dfu_status_fmter)


class DFUStateAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_dfu_state_fmter)


class ErrorAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_error_id_fmter)


class ModelIdAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_model_name_fmter)

class ELStateAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_el_state_fmter)

class ELPropertyIDAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_property_id_fmter)


class ELTTestStatusAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_test_status_fmter)


class OpcodeAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_opcode_name_fmter)


class MeshMesReq1OpcodeAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, enum_meshmesreq1_opcode_name_fmter)


class ListAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, list_fmter)


class StructAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, struct_fmter)


class DataHexStrAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, data_hexstr_fmter)


class DataAsciiAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, data_ascii_fmter)


class UUIDAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uuid_fmter)


class Uint8HexAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint8_hex_fmter)


class Uint16HexAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint16_hex_fmter)


class Uint32HexAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint32_hex_fmter)


class Uint8HexAndIntAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint8_hex_and_int_fmter)


class Uint16HexAndIntAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint16_hex_and_int_fmter)


class Uint32HexAndIntAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, uint32_hex_and_int_fmter)


class PropertyIdAdapter(Uint16HexAdapter):
    pass


class CompanyIdAdapter(Uint16HexAdapter):
    pass


class MeshDateAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, mesh_date_fmter)


class RTCDateAdapter(Adapter):

    def _decode(self, obj, context, path):
        return ValueObj(obj, rtc_date_fmter)
