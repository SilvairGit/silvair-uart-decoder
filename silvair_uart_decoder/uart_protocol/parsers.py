from construct import Struct, Int8ul, Int16ul, Int32ul, Bytes, this, GreedyRange, GreedyBytes, Array, \
    Switch, Int24ul, BytesInteger, Adapter, Container, StopIf, BitStruct, Padding, Flag, Nibble, Bitwise, Bytewise

from .common import CommandCode, ModelName, OpcodeName, SettingName
from .adapters import ValueObj, AttentionAdapter, DeviceStateAdapter, DFUStatusAdapter, DFUStateAdapter, \
    ErrorAdapter, ModelIdAdapter, ListAdapter, StructAdapter, DataHexStrAdapter, DataAsciiAdapter, UUIDAdapter, \
    Uint8HexAdapter, Uint16HexAdapter, Uint32HexAndIntAdapter, PropertyIdAdapter, CompanyIdAdapter, OpcodeAdapter, \
    MeshDateAdapter, RTCDateAdapter, MeshMesReq1OpcodeAdapter, ELStateAdapter, ELPropertyIDAdapter, \
    ELTTestStatusAdapter, SettingIdAdapter, AccessAdapter


class MeshOpcodeAdapter(Adapter):
    def _decode(self, obj, context, path):
        if obj["first"] <= 0b01111111:
            opcode_value = obj["first"]
        elif obj["first"] > 0b10111111:
            opcode_value = (obj["first"] << 24) + (obj["second"] << 16) + (obj["third"] << 8) + obj['subopcode']
        else:
            opcode_value = (obj["first"] << 8) + obj["second"]

        return opcode_value

    def _encode(self, obj, context, path):
        if obj <= 0xFF:
            return Container(first=obj, second=None, third=None)
        elif obj <= 0xFFFF:
            return Container(first=obj >> 8, second=obj, third=None)

        return Container(first=obj >> 16, second=obj >> 8, third=obj)


ModelId = ModelIdAdapter(Int16ul)

SettingId = SettingIdAdapter(Int16ul)

Access = AccessAdapter(Int8ul)

ModelIds = ListAdapter(GreedyRange(ModelId))

SensorParams = StructAdapter(Struct(
    "property_id" / PropertyIdAdapter(Int16ul),
    "positive_tolerance" / Uint16HexAdapter(Int16ul),
    "negative_tolerance" / Uint16HexAdapter(Int16ul),
    "sampling_function" / Uint8HexAdapter(Int8ul),
    "measurement_period" / Uint8HexAdapter(Int8ul),
    "update_interval" / Uint8HexAdapter(Int8ul),
))

SensorSettingValue = StructAdapter(Struct(
    "model_id" / ModelId,
    "access" / Access,
    "setting_id" / SettingId,
    "setting_value" / Switch(
        this.setting_id,
        {
            ValueObj(SettingName.Sensor_Sensitivity.value): Int8ul,
            ValueObj(SettingName.Sensor_Sensitivity_Steps.value): Int8ul,
        },
        default=None,
    )
))

SensorServerParams = StructAdapter(Bitwise(Struct(
    "setting_count" / Nibble,
    "sensor_count" / Nibble,
    "sensors" / Bytewise(ListAdapter(Array(this.sensor_count, SensorParams))),
    "settings" / Bytewise(ListAdapter(Array(this.setting_count, SensorSettingValue))),
)))

TimeServerParams = StructAdapter(Struct(
    "flags" / Int8ul,
    "rtc_accuracy" / Int16ul
))

LightCTLParams = StructAdapter(Struct(
    "min_temp_range" / Int16ul,
    "max_temp_range" / Int16ul,
))

HealthServerParams = StructAdapter(Struct(
    "company_id_count" / Int8ul,
    "company_ids" / ListAdapter(Array(this.company_id_count, Uint16HexAdapter(Int16ul))),
))

MeshMessageReq = StructAdapter(Struct(
    "instance_idx" / Int8ul,
    "sub_idx" / Int8ul,
    "mesh_opcode" / OpcodeAdapter(Int16ul),
    "mesh_cmd" / DataHexStrAdapter(GreedyBytes),
))

MeshMessageResp = StructAdapter(Struct(
    "instance_idx" / Int8ul,
    "sub_idx" / Int8ul,
))

SensorUpdateReq = StructAdapter(Struct(
    "instance_idx" / Int8ul,
    "property_id" / PropertyIdAdapter(Int16ul),
    "sensor_data" / DataHexStrAdapter(GreedyBytes),
))

DFUInitReq = StructAdapter(Struct(
    "fw_size" / Int32ul,
    "fw_sha256" / DataHexStrAdapter(Bytes(32)),
    "app_data_len" / Int8ul,
    "app_data" / DataHexStrAdapter(Bytes(this.app_data_len))
))

DFUStatusResp = StructAdapter(Struct(
    "status" / DFUStatusAdapter(Int8ul),
    "supp_page_size" / Uint32HexAndIntAdapter(Int32ul),
    "fw_offset" / Uint32HexAndIntAdapter(Int32ul),
    "fw_crc" / Uint32HexAndIntAdapter(Int32ul),
))

HealthFaultParams = StructAdapter(Struct(
    "company_id" / CompanyIdAdapter(Int16ul),
    "fault_id" / Int8ul,
    "instance_idx" / Int8ul,
))

HealthTestParams = StructAdapter(Struct(
    "company_id" / CompanyIdAdapter(Int16ul),
    "test_id" / Int8ul,
    "instance_idx" / Int8ul,
))

ModelParams = ListAdapter(GreedyRange(
    StructAdapter(Struct(
        "model_id" / ModelId,
        "params" / Switch(
            this.model_id,
            {
                ValueObj(ModelName.Health_Server.value): HealthServerParams,
                ValueObj(ModelName.Sensor_Server.value): SensorServerParams,
                ValueObj(ModelName.Light_CTL_Server.value): LightCTLParams,
                ValueObj(ModelName.Time_Server.value): TimeServerParams
            },
            default=None,
        )
    )))
)

Data = StructAdapter(Struct(
    "data" / DataHexStrAdapter(GreedyBytes)
))

DFUPageCreateReq = StructAdapter(Struct(
    "requested_page_size" / Uint32HexAndIntAdapter(Int32ul),
))

Attention = StructAdapter(Struct(
    "attention" / AttentionAdapter(Int8ul),
))

DeviceState = StructAdapter(Struct(
    "device_state" / DeviceStateAdapter(Int8ul),
))

Error = StructAdapter(Struct(
    "error_id" / ErrorAdapter(Int8ul),
))

DFUStatus = StructAdapter(Struct(
    "dfu_status" / DFUStatusAdapter(Int8ul),
))

DFUState = StructAdapter(Struct(
    "dfu_state" / DFUStateAdapter(Int8ul),
))

Version = StructAdapter(Struct(
    "version" / DataAsciiAdapter(GreedyBytes)
))

UUID = StructAdapter(Struct(
    "uuid" / UUIDAdapter(GreedyBytes)
))

Battery = StructAdapter(Struct(
    "instance_index" / Int8ul,
    "battery_level" / Int8ul,
    "time_to_discharge" / Int24ul,
    "time_to_charge" / Int24ul,
    "flags" / Int8ul
))

MeshMesReq1Opcode = MeshMesReq1OpcodeAdapter(MeshOpcodeAdapter(
    Struct(
        "first" / Int8ul,
        StopIf(this.first <= 0b01111111),
        "second" / Int8ul,
        StopIf(this.first <= 0b10111111),
        "third" / Int8ul,
        "subopcode" / Int8ul)
))


RTCDateFormat = RTCDateAdapter(Struct(
    "year" / Int16ul,
    "month" / Int8ul,
    "day" / Int8ul,
    "hour" / Int8ul,
    "minute" / Int8ul,
    "second" / Int8ul,
    "millisecond" / Int16ul
))

TimeSourceSetReq = StructAdapter(Struct(
    "instance_index" / Int8ul,
    "rtc_date" / RTCDateFormat
))

TimeSourceGetResp = TimeSourceSetReq

InstanceIndexContainer = StructAdapter(Struct(
    "instance_index" / Int8ul
))

TimeSourceSetResp = InstanceIndexContainer

TimeSourceGetReq = InstanceIndexContainer

TimeGetReq = InstanceIndexContainer

SenSetUpdateReq = StructAdapter(Struct(
    "instance_index" / Int8ul,
    "property_id" / PropertyIdAdapter(Int16ul),
    "setting_id" / SettingId,
    "setting_value" / Switch(
        this.setting_id,
        {
            ValueObj(SettingName.Sensor_Sensitivity.value): Int8ul,
            ValueObj(SettingName.Sensor_Sensitivity_Steps.value): Int8ul,
        },
        default=None,
    )
))

SenSetUpdateResp = InstanceIndexContainer

MeshTimeFormat = MeshDateAdapter(Struct(
    "tai_seconds" / BytesInteger(5, swapped=True),
    "subsecond" / Int8ul,
    "tai_utc_delta" / Int16ul,
    "time_zone_offset" / Int8ul
))

TimeGetResp = StructAdapter(Struct(
    "instance_index" / Int8ul,
    "date" / MeshTimeFormat
))

ElState = ELStateAdapter(Int8ul)

ELPropertyID = ELPropertyIDAdapter(Int16ul)

ElPropertyStatus = StructAdapter(Struct(
    "property_id" / ELPropertyID,
    "property_value" / Int16ul
))

ElOperationalTimeStatus = StructAdapter(Struct(
    "el_total_operation_time" / Int32ul,
    "el_emergency_time" / Int32ul
))

ELTTestStatus = ELTTestStatusAdapter(Int8ul)
ELTDurationTestResult = BitStruct(
    "RFU" / Padding(4),                # bits 4-7
    "Battery_duration_fault" / Flag,   # bit 3
    "Circuit_fault" / Flag,            # bit 2
    "Battery_fault" / Flag,            # bit 1
    "Lamp_fault" / Flag,               # bit 0
)

ELTFunctionalTestResult = BitStruct(
    "RFU" / Padding(5),                # bits 3-7
    "Circuit_fault" / Flag,            # bit 2
    "Battery_fault" / Flag,            # bit 1
    "Lamp_fault" / Flag,               # bit 0
)

ELTFunctionalTestStatus = StructAdapter(Struct(
    "status" / ELTTestStatus,
    "result" / ELTFunctionalTestResult
))

ElTDurationTestStatus = StructAdapter(Struct(
    "status" / ELTTestStatus,
    "result" / ELTDurationTestResult,
    "test_length" / Int16ul
))

MeshMessageReq1 = StructAdapter(Struct(
    "instance_index" / Int8ul,
    "sub_index" / Int8ul,
    "mesh_opcode" / MeshMesReq1Opcode,
    "mesh_cmd" / Switch(
            this.mesh_opcode,
            {
                ValueObj(OpcodeName.EL_State_Status): ElState,
                ValueObj(OpcodeName.EL_Property_Status): ElPropertyStatus,
                ValueObj(OpcodeName.EL_Operation_Time_Status): ElOperationalTimeStatus,
                ValueObj(OpcodeName.ELT_Functional_Test_Status): ELTFunctionalTestStatus,
                ValueObj(OpcodeName.ELT_Duration_Test_Status): ElTDurationTestStatus,
            },
            default=DataHexStrAdapter(GreedyBytes),
        )
))


class CommandParamParser:
    PARAM_PARSERS = {
        CommandCode.PingRequest: Data.parse,
        CommandCode.PongResponse: Data.parse,
        CommandCode.InitDeviceEvent: ModelIds.parse,
        CommandCode.CreateInstancesRequest: ModelParams.parse,
        CommandCode.CreateInstancesResponse: ModelIds.parse,
        CommandCode.InitNodeEvent: ModelIds.parse,
        CommandCode.MeshMessageRequest: MeshMessageReq.parse,
        CommandCode.MeshMessageResponse: MeshMessageResp.parse,
        CommandCode.CurrentStateResponse: DeviceState.parse,
        CommandCode.Error: Error.parse,
        CommandCode.ModemFirmwareVersionResponse: Version.parse,
        CommandCode.SensorUpdateRequest: SensorUpdateReq.parse,
        CommandCode.AttentionEvent: Attention.parse,
        CommandCode.DeviceUUIDResponse: UUID.parse,
        CommandCode.SetFaultRequest: HealthFaultParams.parse,
        CommandCode.ClearFaultRequest: HealthFaultParams.parse,
        CommandCode.StartTestRequest: HealthTestParams.parse,
        CommandCode.TestFinishedRequest: HealthTestParams.parse,
        CommandCode.FirmwareVersionSetRequest: Version.parse,
        CommandCode.DfuInitRequest: DFUInitReq.parse,
        CommandCode.DfuInitResponse: DFUStatus.parse,
        CommandCode.DfuStatusResponse: DFUStatusResp.parse,
        CommandCode.DfuPageCreateRequest: DFUPageCreateReq.parse,
        CommandCode.DfuPageCreateResponse: DFUStatus.parse,
        CommandCode.DfuWriteDataEvent: Data.parse,
        CommandCode.DfuPageStoreResponse: DFUStatus.parse,
        CommandCode.DfuStateCheckResponse: DFUState.parse,
        CommandCode.BatteryStatusSetRequest: Battery.parse,
        CommandCode.MeshMessageRequest1: MeshMessageReq1.parse,
        CommandCode.TimeSourceSetRequest: TimeSourceSetReq.parse,
        CommandCode.TimeSourceSetResponse: TimeSourceSetResp.parse,
        CommandCode.TimeSourceGetRequest: TimeSourceGetReq.parse,
        CommandCode.TimeSourceGetResponse: TimeSourceGetResp.parse,
        CommandCode.TimeGetRequest: TimeGetReq.parse,
        CommandCode.TimeGetResponse: TimeGetResp.parse,
        CommandCode.SensorSettingUpdateRequest: SenSetUpdateReq.parse,
        CommandCode.SensorSettingUpdateResponse: SenSetUpdateResp.parse,
    }

    def parse(self, cmd_code, data):
        assert data is not None, "Passed `data` argument shouldn't be None"

        try:
            return str(self.PARAM_PARSERS[cmd_code](data))

        except Exception as exc:
            return "{} [WARNING! Exception occurred: `{}`]".format(Data.parse(data), exc)
