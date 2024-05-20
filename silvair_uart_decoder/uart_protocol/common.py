import enum


class CommandCode(enum.IntEnum):
    PingRequest = 0x01
    PongResponse = 0x02
    InitDeviceEvent = 0x03
    CreateInstancesRequest = 0x04
    CreateInstancesResponse = 0x05
    InitNodeEvent = 0x06
    MeshMessageRequest = 0x07
    StartNodeRequest = 0x09
    StartNodeResponse = 0x0B
    FactoryResetRequest = 0x0C
    FactoryResetResponse = 0x0D
    FactoryResetEvent = 0x0E
    MeshMessageResponse = 0x0F
    CurrentStateRequest = 0x10
    CurrentStateResponse = 0x11
    Error = 0x12
    ModemFirmwareVersionRequest = 0x13
    ModemFirmwareVersionResponse = 0x14
    SensorUpdateRequest = 0x15
    AttentionEvent = 0x16
    SoftResetRequest = 0x17
    SoftResetResponse = 0x18
    SensorUpdateResponse = 0x19
    DeviceUUIDRequest = 0x1A
    DeviceUUIDResponse = 0x1B
    SetFaultRequest = 0x1C
    SetFaultResponse = 0x1D
    ClearFaultRequest = 0x1E
    ClearFaultResponse = 0x1F
    StartTestRequest = 0x20
    StartTestResponse = 0x21
    TestFinishedRequest = 0x22
    TestFinishedResponse = 0x23
    FirmwareVersionSetRequest = 0x24
    FirmwareVersionSetResponse = 0x25
    BatteryStatusSetRequest = 0x26
    BatteryStatusSetResponse = 0x27
    MeshMessageRequest1 = 0x28
    TimeSourceSetRequest = 0x29
    TimeSourceSetResponse = 0x2A
    TimeSourceGetRequest = 0x2B
    TimeSourceGetResponse = 0x2C
    TimeGetRequest = 0x2D
    TimeGetResponse = 0x2E
    SensorSettingUpdateRequest = 0x2F
    SensorSettingUpdateResponse = 0x30
    DfuInitRequest = 0x80
    DfuInitResponse = 0x81
    DfuStatusRequest = 0x82
    DfuStatusResponse = 0x83
    DfuPageCreateRequest = 0x84
    DfuPageCreateResponse = 0x85
    DfuWriteDataEvent = 0x86
    DfuPageStoreRequest = 0x87
    DfuPageStoreResponse = 0x88
    DfuStateCheckRequest = 0x89
    DfuStateCheckResponse = 0x8A
    DfuCancelRequest = 0x8B
    DfuCancelResponse = 0x8C


class AttentionState(enum.IntEnum):
    Off = 0x00
    On = 0x01


class DeviceState(enum.IntEnum):
    InitDevice = 0x00
    Device = 0x01
    InitNode = 0x02
    Node = 0x03


class ErrorId(enum.IntEnum):
    Invalid_CRC = 0x00
    Invalid_Cmd = 0x01
    Invalid_Len = 0x02
    Invalid_State = 0x03
    Invalid_Param = 0x04
    Timeout = 0x05
    No_License_For_Model_Reg = 0x06
    No_Resources_For_Model_Reg = 0x07
    Mesh_Message_Request_Process_Error = 0x08


class DFUStatus(enum.IntEnum):
    Success = 0x01
    Insufficient_Resources = 0x04
    Invalid_Object = 0x05
    Operation_Not_Permitted = 0x08
    Operation_Failed = 0x0A
    Firmware_Successfully_Updated = 0xFF


class DFUState(enum.IntEnum):
    DFU_In_Progress = 0x00
    DFU_Not_In_Progress = 0x01


class ELState(enum.IntEnum):
    Normal = 0x03
    Emergency = 0x05
    Extended_Emergency = 0x06
    Rest = 0x08
    Inhibit = 0x0A
    Duration_Test_In_Progress = 0x0C
    Functional_Test_In_Progress = 0x0E
    Battery_Discharged = 0x0F


class PropertyID(enum.IntEnum):
    EL_Lightness = 0xFF80
    EL_Prolong_Time = 0xFF83


class TestStatus(enum.IntEnum):
    Test_Finished = 0x00
    Test_Result_Unknown = 0x07


class AccessName(enum.IntEnum):
    Read_Only = 0x01
    Read_Write = 0x03


class SettingName(enum.IntEnum):
    Sensor_Sensitivity = 0xFF90
    Sensor_Sensitivity_Steps = 0xFF91


class ModelName(enum.IntEnum):
    Configuration_Server = 0x0000
    Configuration_Client = 0x0001
    Health_Server = 0x0002
    Health_Client = 0x0003
    Generic_OnOff_Server = 0x1000
    Generic_Level_Server = 0x1002
    Generic_Default_Transition_Time_Server = 0x1004
    Generic_Power_OnOff_Server = 0x1006
    Generic_Power_OnOff_SetupServer = 0x1007
    Generic_Power_Level_Server = 0x1009
    Generic_Power_Level_SetupServer = 0x100A
    Generic_Battery_Server = 0x100C
    Generic_Location_Server = 0x100E
    Generic_Location_Setup_Server = 0x100F
    Generic_Admin_Property_Server = 0x1011
    Generic_Manufacturer_Property_Server = 0x1012
    Generic_User_Property_Server = 0x1013
    Generic_Client_Property_Server = 0x1014
    Sensor_Server = 0x1100
    Sensor_Setup_Server = 0x1101
    Time_Server = 0x1200
    Time_Setup_Server = 0x1201
    Scene_Server = 0x1203
    Scene_Setup_Server = 0x1204
    Scheduler_Server = 0x1206
    Scheduler_Setup_Server = 0x1207
    Light_Lightness_Server = 0x1300
    Light_Lightness_Setup_Server = 0x1301
    Light_CTL_Server = 0x1303
    Light_CTL_Setup_Server = 0x1304
    Light_CTL_Temperature_Server = 0x1306
    Light_HSL_Server = 0x1307
    Light_HSL_SetupServer = 0x1308
    Light_HSL_Hue_Server = 0x130A
    Light_HSL_Saturation_Server = 0x130B
    Light_xyL_Server = 0x130C
    Light_xyL_Setup_Server = 0x130D
    Light_LC_Server = 0x130F
    Light_LC_Setup_Server = 0x1310
    Generic_OnOff_Client = 0x1001
    Generic_Level_Client = 0x1003
    Generic_Default_Transition_Time_Client = 0x1005
    Generic_Power_OnOff_Client = 0x1008
    Generic_Power_Level_Client = 0x100B
    Generic_Battery_Client = 0x100D
    Generic_Location_Client = 0x1010
    Generic_Property_Client = 0x1015
    Sensor_Client = 0x1102
    Time_Client = 0x1202
    Scene_Client = 0x1205
    Scheduler_Client = 0x1208
    Light_Lightness_Client = 0x1302
    Light_CTL_Client = 0x1305
    Light_HSL_Client = 0x1309
    Light_xyL_Client = 0x130E
    Light_LC_Client = 0x1311
    EL_Test_Server = 0xE500


class OpcodeName(enum.IntEnum):
    Generic_OnOff_Get = 0x8201
    Generic_OnOff_Set = 0x8202
    Generic_OnOff_Set_Unacknowledged = 0x8203
    Generic_OnOff_Status = 0x8204
    Generic_Level_Get = 0x8205
    Generic_Level_Set = 0x8206
    Generic_Level_Set_Unacknowledged = 0x8207
    Generic_Level_Status = 0x8208
    Generic_Delta_Set = 0x8209
    Generic_Delta_Set_Unacknowledged = 0x820A
    Generic_Move_Set = 0x820B
    Generic_Move_Set_Unacknowledged = 0x820C
    Generic_Default_Transition_Time_Get = 0x820D
    Generic_Default_Transition_Time_Set = 0x820E
    Generic_Default_Transition_Time_Set_Unacknowledged = 0x820F
    Generic_Default_Transition_Time_Status = 0x8210
    Generic_OnPowerUp_Get = 0x8211
    Generic_OnPowerUp_Status = 0x8212
    Generic_OnPowerUp_Set = 0x8213
    Generic_OnPowerUp_Set_Unacknowledged = 0x8214
    Generic_Power_Level_Get = 0x8215
    Generic_Power_Level_Set = 0x8216
    Generic_Power_Level_Set_Unacknowledged = 0x8217
    Generic_Power_Level_Status = 0x8218
    Generic_Power_Last_Get = 0x8219
    Generic_Power_Last_Status = 0x821A
    Generic_Power_Default_Get = 0x821B
    Generic_Power_Default_Status = 0x821C
    Generic_Power_Range_Get = 0x821D
    Generic_Power_Range_Status = 0x821E
    Generic_Power_Default_Set = 0x821F
    Generic_Power_Default_Set_Unacknowledged = 0x8220
    Generic_Power_Range_Set = 0x8221
    Generic_Power_Range_Set_Unacknowledged = 0x8222
    Generic_Battery_Get = 0x8223
    Generic_Battery_Status = 0x8224
    Generic_Location_Global_Get = 0x8225
    Generic_Location_Global_Status = 0x40
    Generic_Location_Local_Get = 0x8226
    Generic_Location_Local_Status = 0x8227
    Generic_Location_Global_Set = 0x41
    Generic_Location_Global_Set_Unacknowledged = 0x42
    Generic_Location_Local_Set = 0x8228
    Generic_Location_Local_Set_Unacknowledged = 0x8229
    Generic_Manufacturer_Properties_Get = 0x822A
    Generic_Manufacturer_Properties_Status = 0x43
    Generic_Manufacturer_Property_Get = 0x822B
    Generic_Manufacturer_Property_Set = 0x44
    Generic_Manufacturer_Property_Set_Unacknowledged = 0x45
    Generic_Manufacturer_Property_Status = 0x46
    Generic_Admin_Properties_Get = 0x822C
    Generic_Admin_Properties_Status = 0x47
    Generic_Admin_Property_Get = 0x822D
    Generic_Admin_Property_Set = 0x48
    Generic_Admin_Property_Set_Unacknowledged = 0x49
    Generic_Admin_Property_Status = 0x4A
    Generic_User_Properties_Get = 0x822E
    Generic_User_Properties_Status = 0x4B
    Generic_User_Property_Get = 0x822F
    Generic_User_Property_Set = 0x4C
    Generic_User_Property_Set_Unacknowledged = 0x4D
    Generic_User_Property_Status = 0x4E
    Generic_Client_Properties_Get = 0x4F
    Generic_Client_Properties_Status = 0x50
    Sensor_Descriptor_Get = 0x8230
    Sensor_Descriptor_Status = 0x51
    Sensor_Get = 0x8231
    Sensor_Status = 0x52
    Sensor_Column_Get = 0x8232
    Sensor_Column_Status = 0x53
    Sensor_Series_Get = 0x8233
    Sensor_Series_Status = 0x54
    Sensor_Cadence_Get = 0x8234
    Sensor_Cadence_Set = 0x55
    Sensor_Cadence_Set_Unacknowledged = 0x56
    Sensor_Cadence_Status = 0x57
    Sensor_Settings_Get = 0x8235
    Sensor_Settings_Status = 0x58
    Sensor_Setting_Get = 0x8236
    Sensor_Setting_Set = 0x59
    Sensor_Setting_Set_Unacknowledged = 0x5A
    Sensor_Setting_Status = 0x5B
    Time_Get = 0x8237
    Time_Set = 0x5C
    Time_Status = 0x5D
    Time_Role_Get = 0x8238
    Time_Role_Set = 0x8239
    Time_Role_Status = 0x823A
    Time_Zone_Get = 0x823B
    Time_Zone_Set = 0x823C
    Time_Zone_Status = 0x823D
    TAI_UTC_Delta_Get = 0x823E
    TAI_UTC_Delta_Set = 0x823F
    TAI_UTC_Delta_Status = 0x8240
    Scene_Get = 0x8241
    Scene_Recall = 0x8242
    Scene_Recall_Unacknowledged = 0x8243
    Scene_Status = 0x5E
    Scene_Register_Get = 0x8244
    Scene_Register_Status = 0x8245
    Scene_Store = 0x8246
    Scene_Store_Unacknowledged = 0x8247
    Scene_Delete = 0x829E
    Scene_Delete_Unacknowledged = 0x829F
    Scheduler_Action_Get = 0x8248
    Scheduler_Action_Status = 0x5F
    Scheduler_Get = 0x8249
    Scheduler_Status = 0x824A
    Scheduler_Action_Set = 0x60
    Scheduler_Action_Set_Unacknowledged = 0x61
    Light_Lightness_Get = 0x824B
    Light_Lightness_Set = 0x824C
    Light_Lightness_Set_Unacknowledged = 0x824D
    Light_Lightness_Status = 0x824E
    Light_Lightness_Linear_Get = 0x824F
    Light_Lightness_Linear_Set = 0x8250
    Light_Lightness_Linear_Set_Unacknowledged = 0x8251
    Light_Lightness_Linear_Status = 0x8252
    Light_Lightness_Last_Get = 0x8253
    Light_Lightness_Last_Status = 0x8254
    Light_Lightness_Default_Get = 0x8255
    Light_Lightness_Default_Status = 0x8256
    Light_Lightness_Range_Get = 0x8257
    Light_Lightness_Range_Status = 0x8258
    Light_Lightness_Default_Set = 0x8259
    Light_Lightness_Default_Set_Unacknowledged = 0x825A
    Light_Lightness_Range_Set = 0x825B
    Light_Lightness_Range_Set_Unacknowledged = 0x825C
    Light_CTL_Get = 0x825D
    Light_CTL_Set = 0x825E
    Light_CTL_Set_Unacknowledged = 0x825F
    Light_CTL_Status = 0x8260
    Light_CTL_Temperature_Get = 0x8261
    Light_CTL_Temperature_Range_Get = 0x8262
    Light_CTL_Temperature_Range_Status = 0x8263
    Light_CTL_Temperature_Set = 0x8264
    Light_CTL_Temperature_Set_Unacknowledged = 0x8265
    Light_CTL_Temperature_Status = 0x8266
    Light_CTL_Default_Get = 0x8267
    Light_CTL_Default_Status = 0x8268
    Light_CTL_Default_Set = 0x8269
    Light_CTL_Default_Set_Unacknowledged = 0x826A
    Light_CTL_Temperature_Range_Set = 0x826B
    Light_CTL_Temperature_Range_Set_Unacknowledged = 0x826C
    Light_HSL_Get = 0x826D
    Light_HSL_Hue_Get = 0x826E
    Light_HSL_Hue_Set = 0x826F
    Light_HSL_Hue_Set_Unacknowledged = 0x8270
    Light_HSL_Hue_Status = 0x8271
    Light_HSL_Saturation_Get = 0x8272
    Light_HSL_Saturation_Set = 0x8273
    Light_HSL_Saturation_Set_Unacknowledged = 0x8274
    Light_HSL_Saturation_Status = 0x8275
    Light_HSL_Set = 0x8276
    Light_HSL_Set_Unacknowledged = 0x8277
    Light_HSL_Status = 0x8278
    Light_HSL_Target_Get = 0x8279
    Light_HSL_Target_Status = 0x827A
    Light_HSL_Default_Get = 0x827B
    Light_HSL_Default_Status = 0x827C
    Light_HSL_Range_Get = 0x827D
    Light_HSL_Range_Status = 0x827E
    Light_HSL_Default_Set = 0x827F
    Light_HSL_Default_Set_Unacknowledged = 0x8280
    Light_HSL_Range_Set = 0x8281
    Light_HSL_Range_Set_Unacknowledged = 0x82
    Light_xyL_Get = 0x8283
    Light_xyL_Set = 0x8284
    Light_xyL_Set_Unacknowledged = 0x8285
    Light_xyL_Status = 0x8286
    Light_xyL_Target_Get = 0x8287
    Light_xyL_Target_Status = 0x8288
    Light_xyL_Default_Get = 0x8289
    Light_xyL_Default_Status = 0x828A
    Light_xyL_Range_Get = 0x828B
    Light_xyL_Range_Status = 0x828C
    Light_xyL_Default_Set = 0x828D
    Light_xyL_Default_Set_Unacknowledged = 0x828E
    Light_xyL_Range_Set = 0x828F
    Light_xyL_Range_Set_Unacknowledged = 0x8290
    Light_LC_Mode_Get = 0x8291
    Light_LC_Mode_Set = 0x8292
    Light_LC_Mode_Set_Unacknowledged = 0x8293
    Light_LC_Mode_Status = 0x8294
    Light_LC_OM_Get = 0x8295
    Light_LC_OM_Set = 0x8296
    Light_LC_OM_Set_Unacknowledged = 0x8297
    Light_LC_OM_Status = 0x8298
    Light_LC_Light_OnOff_Get = 0x8299
    Light_LC_Light_OnOff_Set = 0x829A
    Light_LC_Light_OnOff_Set_Unacknowledged = 0x829B
    Light_LC_Light_OnOff_Status = 0x829C
    Light_LC_Property_Get = 0x829D
    Light_LC_Property_Set = 0x62
    Light_LC_Property_Set_Unacknowledged = 0x63
    Light_LC_Property_Status = 0x64
    Emergency_Lighting_Opcode = 0xFE3601
    ELT_Functional_Test_Start = 0xE9360101
    ELT_Functional_Test_Stop = 0xE9360102
    ELT_Functional_Test_Get = 0xE9360100
    ELT_Functional_Test_Status = 0xE9360103
    ELT_Duration_Test_Start = 0xE9360105
    ELT_Duration_Test_Stop = 0xE9360106
    ELT_Duration_Test_Get = 0xE9360104
    ELT_Duration_Test_Status = 0xE9360107
    EL_Inhibit_Enter = 0xEA360100
    EL_Inhibit_Exit = 0xEA360102
    EL_Rest_Enter = 0xEA36010E
    EL_Rest_Exit = 0xEA360110
    EL_State_Get = 0xEA360104
    EL_State_Status = 0xEA360105
    EL_Property_Status = 0xEA360109
    EL_Operation_Time_Get = 0xEA36010A
    EL_Operation_Time_Clear = 0xEA36010B
    EL_Operation_Time_Status = 0xEA36010D
