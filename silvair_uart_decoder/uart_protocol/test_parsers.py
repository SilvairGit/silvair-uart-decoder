import unittest

from .parsers import ModelId, ModelIds, Attention, Data, DFUPageCreateReq, DeviceState, Error, DFUStatus, \
    DFUState, UUID, Version, HealthFaultParams, HealthTestParams, MeshMessageReq, MeshMessageResp, SensorUpdateReq, \
    DFUInitReq, DFUStatusResp, HealthServerParams, SensorParams, SensorServerParams, ModelParams, TimeGetResp, \
    TimeSourceGetResp, MeshMessageReq1


class ParsersTest(unittest.TestCase):

    def test_should_parse_ModelId(self):
        data = bytes([0x36, 0x01])
        self.assertEqual(0x0136, ModelId.parse(data).value)

    def test_should_parse_ModelIds(self):
        data = bytes([0x00, 0x00, 0x36, 0x01, 0x22, 0x33])
        self.assertSequenceEqual([0x0000, 0x0136, 0x3322], ModelIds.parse(data).value)

    def test_should_parse_UUID(self):
        data = bytes([0x12, 0x34, 0x56, 0x78, 0x12, 0x34, 0x56, 0x78, 0xAA, 0xBB, 0xCC, 0xDD, 0xAA, 0xBB, 0xCC, 0xDD])
        self.assertSequenceEqual(data, UUID.parse(data).value.uuid.value)

    def test_should_parse_Attention(self):
        data = bytes([0x01])
        self.assertEqual(1, Attention.parse(data).value.attention.value)

    def test_should_parse_Data(self):
        data = bytes([0x12, 0x34, 0x56, 0x78])
        self.assertSequenceEqual(data, Data.parse(data).value.data.value)

    def test_should_parse_DFUPageCreateReq(self):
        data = bytes([0x20, 0x00, 0x00, 0x00])
        self.assertEqual(32, DFUPageCreateReq.parse(data).value.requested_page_size.value)

    def test_should_parse_DeviceState(self):
        data = bytes([0x03])
        self.assertEqual(3, DeviceState.parse(data).value.device_state.value)

    def test_should_parse_Error(self):
        data = bytes([0x04])
        self.assertEqual(4, Error.parse(data).value.error_id.value)

    def test_should_parse_DFUStatus(self):
        data = bytes([0x05])
        self.assertEqual(5, DFUStatus.parse(data).value.dfu_status.value)

    def test_should_parse_DFUState(self):
        data = bytes([0x06])
        self.assertEqual(6, DFUState.parse(data).value.dfu_state.value)

    def test_should_parse_Version(self):
        data = b'1.0.5'
        self.assertSequenceEqual(data, Version.parse(data).value.version.value)

    def test_should_parse_HealthFaultParams(self):
        data = bytes([0x36, 0x01, 0x01, 0x02])

        result = HealthFaultParams.parse(data)
        self.assertEqual(0x0136, result.value.company_id.value)
        self.assertEqual(1, result.value.fault_id)
        self.assertEqual(2, result.value.instance_idx)

    def test_should_parse_HealthTestParams(self):
        data = bytes([0x36, 0x01, 0x02, 0x01])

        result = HealthTestParams.parse(data)
        self.assertEqual(0x0136, result.value.company_id.value)
        self.assertEqual(2, result.value.test_id)
        self.assertEqual(1, result.value.instance_idx)

    def test_should_parse_MeshMessageReq(self):
        data = bytes([0x01, 0x02, 0x8e, 0x80, 0x12, 0x34, 0x56, 0x78])

        result = MeshMessageReq.parse(data)
        self.assertEqual(1, result.value.instance_idx)
        self.assertEqual(2, result.value.sub_idx)
        self.assertEqual(0x808e, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([0x12, 0x34, 0x56, 0x78]), result.value.mesh_cmd.value)

    def test_should_parse_MeshMessageResp(self):
        data = bytes([0x01, 0x02])

        result = MeshMessageResp.parse(data)
        self.assertEqual(1, result.value.instance_idx)
        self.assertEqual(2, result.value.sub_idx)

    def test_should_parse_SensorUpdateReq(self):
        data = bytes([0x01, 0x8e, 0x80, 0x12, 0x34, 0x56, 0x78])

        result = SensorUpdateReq.parse(data)
        self.assertEqual(1, result.value.instance_idx)
        self.assertEqual(0x808e, result.value.property_id.value)
        self.assertEqual(bytes([0x12, 0x34, 0x56, 0x78]), result.value.sensor_data.value)

    def test_should_parse_DFUInitReq(self):
        fw_sha256 = bytes([0x07, 0x70, 0x15, 0x97, 0x88, 0xdd, 0xbe, 0x07,
                           0x5c, 0xd1, 0xcc, 0xd0, 0x8d, 0x11, 0xda, 0x29,
                           0x2b, 0x1a, 0xbe, 0x4c, 0x47, 0xd2, 0x8b, 0xb5,
                           0xae, 0xb7, 0xa4, 0xbc, 0x7c, 0x84, 0x61, 0x39])

        app_data = bytes([0x12, 0x34, 0x56, 0x78])

        data = bytes([0x00, 0x08, 0x00, 0x00]) + fw_sha256 + bytes([len(app_data)]) + app_data

        result = DFUInitReq.parse(data)
        self.assertEqual(2048, result.value.fw_size)
        self.assertSequenceEqual(fw_sha256, result.value.fw_sha256.value)
        self.assertEqual(len(app_data), result.value.app_data_len)
        self.assertSequenceEqual(app_data, result.value.app_data.value)

    def test_should_parse_DFUStatusResp(self):
        data = bytes([0x01, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x3b, 0xf6, 0x8d, 0x11])

        result = DFUStatusResp.parse(data)
        self.assertEqual(1, result.value.status.value)
        self.assertEqual(1024, result.value.supp_page_size.value)
        self.assertEqual(1024, result.value.fw_offset.value)
        self.assertEqual(0x118df63b, result.value.fw_crc.value)

    def test_should_parse_HealthServerParams(self):
        data = bytes([0x01, 0x36, 0x01])

        result = HealthServerParams.parse(data)
        self.assertEqual(1, result.value.company_id_count)
        self.assertSequenceEqual([0x0136], result.value.company_ids.value)

    def test_should_parse_SensorParams(self):
        data = bytes([0x4d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x40])

        result = SensorParams.parse(data)
        self.assertEqual(0x004d, result.value.property_id.value)
        self.assertEqual(0x0000, result.value.positive_tolerance.value)
        self.assertEqual(0x0000, result.value.negative_tolerance.value)
        self.assertEqual(0x01, result.value.sampling_function.value)
        self.assertEqual(0x00, result.value.measurement_period.value)
        self.assertEqual(0x40, result.value.update_interval.value)

    def test_should_parse_SensorServerParams(self):
        data = bytes([0x01, 0x4d, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x40])

        result = SensorServerParams.parse(data)
        self.assertEqual(1, result.value.sensor_count)
        self.assertEqual(0x004d, result.value.sensors.value[0].value.property_id.value)
        self.assertEqual(0x0000, result.value.sensors.value[0].value.positive_tolerance.value)
        self.assertEqual(0x0000, result.value.sensors.value[0].value.negative_tolerance.value)
        self.assertEqual(0x01, result.value.sensors.value[0].value.sampling_function.value)
        self.assertEqual(0x00, result.value.sensors.value[0].value.measurement_period.value)
        self.assertEqual(0x40, result.value.sensors.value[0].value.update_interval.value)

    def test_should_parse_ModelParams(self):
        data = bytes([0x0f, 0x13, 0x00, 0x11, 0x01, 0x4d, 0x00, 0x00,
                      0x00, 0x00, 0x00, 0x01, 0x00, 0x40, 0x02, 0x00,
                      0x01, 0x36, 0x01])

        result = ModelParams.parse(data)
        self.assertEqual(0x130f, result.value[0].value.model_id.value)
        self.assertEqual(None, result.value[0].value.params)
        self.assertEqual(0x1100, result.value[1].value.model_id.value)
        self.assertEqual(0x004d, result.value[1].value.params.value.sensors.value[0].value.property_id.value)
        self.assertEqual(0x0000, result.value[1].value.params.value.sensors.value[0].value.positive_tolerance.value)
        self.assertEqual(0x0000, result.value[1].value.params.value.sensors.value[0].value.negative_tolerance.value)
        self.assertEqual(0x01, result.value[1].value.params.value.sensors.value[0].value.sampling_function.value)
        self.assertEqual(0x00, result.value[1].value.params.value.sensors.value[0].value.measurement_period.value)
        self.assertEqual(0x40, result.value[1].value.params.value.sensors.value[0].value.update_interval.value)
        self.assertEqual(0x0002, result.value[2].value.model_id.value)
        self.assertEqual(1, result.value[2].value.params.value.company_id_count)
        self.assertSequenceEqual([0x0136], result.value[2].value.params.value.company_ids.value)

    def test_should_parse_TimeServer_ModelParams(self):
        data = bytes([0x00, 0x12, 0x01, 0x10, 0x27])

        result = ModelParams.parse(data)
        self.assertEqual(0x1200, result.value[0].value.model_id.value)
        self.assertEqual(0x01, result.value[0].value.params.value.flags)
        self.assertEqual(0x2710, result.value[0].value.params.value.rtc_accuracy)

    def test_should_parse_LightCTL_ModelParams(self):
        data = bytes([0x03, 0x13, 0x00, 0x11, 0x01, 0x30])

        result = ModelParams.parse(data)
        self.assertEqual(0x1303, result.value[0].value.model_id.value)
        self.assertEqual(0x1100, result.value[0].value.params.value.min_temp_range)
        self.assertEqual(0x3001, result.value[0].value.params.value.max_temp_range)

    def test_should_parse_TimeGetResp(self):
        data = bytes([0x02, 0x9D, 0x36, 0xE5, 0x20, 0x00, 0x01, 0x24, 0x01, 0x40])

        result = TimeGetResp.parse(data)
        self.assertEqual(0x02, result.value.instance_index)
        self.assertEqual(0x20E5369D, result.value.date.value.tai_seconds)
        self.assertEqual(0x01, result.value.date.value.subsecond)
        self.assertEqual(0x0124, result.value.date.value.tai_utc_delta)
        self.assertEqual(0x40, result.value.date.value.time_zone_offset)
        self.assertEqual(f"27-6-2017 15:30:{1 / 256} (UTC+0.0)", repr(result.value.date))

    def test_should_parse_TimeSourceGetResp(self):
        data = bytes([0x02, 0xE5, 0x07, 12, 7, 23, 59, 59, 0xE7, 0x03])

        result = TimeSourceGetResp.parse(data)
        self.assertEqual(0x02, result.value.instance_index)
        self.assertEqual(0x07E5, result.value.rtc_date.value.year)
        self.assertEqual(12, result.value.rtc_date.value.month)
        self.assertEqual(7, result.value.rtc_date.value.day)
        self.assertEqual(23, result.value.rtc_date.value.hour)
        self.assertEqual(59, result.value.rtc_date.value.minute)
        self.assertEqual(59, result.value.rtc_date.value.second)
        self.assertEqual(0x03E7, result.value.rtc_date.value.millisecond)
        self.assertEqual(f"7-12-{0x07E5} 23:59:59.{0x03E7}", repr(result.value.rtc_date))

    def test_should_parse_MeshMessageReq1_2ByteOpcode(self):
        data = bytes([0x01, 0x02, 0x80, 0x8e, 0x12, 0x34, 0x56, 0x78])

        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0x808e, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([0x12, 0x34, 0x56, 0x78]), result.value.mesh_cmd.value)

    def test_should_parse_MeshMessageReq1_1ByteOpcode(self):
        data = bytes([0x01, 0x02, 0x5D, 0x9D, 0x36, 0xE5, 0x20, 0x00, 0xDD, 0x64, 0xFE, 0x01, 0x40])

        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0x5D, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([0x9D, 0x36, 0xE5, 0x20, 0x00, 0xDD, 0x64, 0xFE, 0x01, 0x40]),
                                 result.value.mesh_cmd.value)

    def test_should_parse_MeshMessageReq1_3ByteOpcode(self):
        # #byteOpecode messages always has subopcode
        data = bytes([0x01, 0x02, 0xFE, 0x36, 0x01, 0x00, 0x05, 0x34, 0x56])

        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xFE360100, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([0x05, 0x34, 0x56]), result.value.mesh_cmd.value)

    def test_should_parse_EL_message_Inhibit_Enter(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x00])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA360100, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([]), result.value.mesh_cmd.value)

    def test_should_parse_EL_message_FunctionalTestStatus(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x00])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA360100, result.value.mesh_opcode.value)
        self.assertSequenceEqual(bytes([]), result.value.mesh_cmd.value)

    def test_should_parse_EL_message_ELStateStatus_1(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x05, 0x03])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA360105, result.value.mesh_opcode.value)
        self.assertEqual(3, result.value.mesh_cmd.value)

    def test_should_parse_EL_message_ELStateStatus_2(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x05, 0x0E])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA360105, result.value.mesh_opcode.value)
        self.assertEqual(0x0E, result.value.mesh_cmd.value)

    def test_should_parse_EL_message_ELPropertyStatus(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x09, 0x80, 0xFF, 0x34, 0x12])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA360109, result.value.mesh_opcode.value)
        self.assertEqual(0xFF80, result.value.mesh_cmd.value.property_id)
        self.assertEqual(0x1234, result.value.mesh_cmd.value.property_value)


    def test_should_parse_EL_message_ELOperationalTimeStatus(self):
        data = bytes([0x01, 0x02, 0xEA, 0x36, 0x01, 0x0D, 0x67, 0x45, 0x23, 0x01, 0xEF, 0xCD, 0xAB, 0x89])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xEA36010D, result.value.mesh_opcode.value)
        self.assertEqual(0x01234567, result.value.mesh_cmd.value.el_total_operation_time)
        self.assertEqual(0x89ABCDEF, result.value.mesh_cmd.value.el_emergency_time)

    def test_should_parse_EL_message_ELTFunctionalTestStatus_1(self):
        data = bytes([0x01, 0x02, 0xE9, 0x36, 0x01, 0x03, 0x07, 0x07])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xE9360103, result.value.mesh_opcode.value)
        self.assertEqual(0x07, result.value.mesh_cmd.value.status)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Lamp_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Battery_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Circuit_fault)

    def test_should_parse_EL_message_ELTFunctionalTestStatus_2(self):
        data = bytes([0x01, 0x02, 0xE9, 0x36, 0x01, 0x03, 0x07, 0x02])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xE9360103, result.value.mesh_opcode.value)
        self.assertEqual(0x07, result.value.mesh_cmd.value.status)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Lamp_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Battery_fault)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Circuit_fault)

    def test_should_parse_EL_message_ELTFunctionalTestStatus_3(self):
        data = bytes([0x01, 0x02, 0xE9, 0x36, 0x01, 0x03, 0x07, 0x01])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xE9360103, result.value.mesh_opcode.value)
        self.assertEqual(0x07, result.value.mesh_cmd.value.status)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Lamp_fault)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Battery_fault)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Circuit_fault)

    def test_should_parse_ELT_message_ELTDurationTestStatus_1(self):
        data = bytes([0x01, 0x02, 0xE9, 0x36, 0x01, 0x07, 0x07, 0x0F, 0x34, 0x12])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xE9360107, result.value.mesh_opcode.value)
        self.assertEqual(0x07, result.value.mesh_cmd.value.status)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Lamp_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Battery_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Circuit_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Battery_duration_fault)
        self.assertEqual(0x1234, result.value.mesh_cmd.value.test_length)

    def test_should_parse_ELT_message_ELTDurationTestStatus_2(self):
        data = bytes([0x01, 0x02, 0xE9, 0x36, 0x01, 0x07, 0x07, 0x08, 0x34, 0x12])
        result = MeshMessageReq1.parse(data)
        self.assertEqual(1, result.value.instance_index)
        self.assertEqual(2, result.value.sub_index)
        self.assertEqual(0xE9360107, result.value.mesh_opcode.value)
        self.assertEqual(0x07, result.value.mesh_cmd.value.status)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Lamp_fault)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Battery_fault)
        self.assertEqual(False, result.value.mesh_cmd.value.result.Circuit_fault)
        self.assertEqual(True, result.value.mesh_cmd.value.result.Battery_duration_fault)
        self.assertEqual(0x1234, result.value.mesh_cmd.value.test_length)


