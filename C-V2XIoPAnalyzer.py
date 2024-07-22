import sys
from lxml import etree
import re
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

# Eval methods: 
# 0 = compare with max, min (val1, val2)
# 1 = octet count (val1, 00)
# 2 = bit string (val1, 00)
# 3 = boolean (00, 00)

# REFERENCE TABLES PER MESSAGE
saej2735_bsm_ref = [    # col[0] = field name, col[1] = parent name, col[2] = length, col[3] = eval method, col[4] = ref value 1, col[5] = ref value 2, col[6] = mandatory?
    ["j2735_2016.msgCnt", "j2735_2016.coreData_element", 1, 0, 0, 127, True],  # start of coreData (mandatory)
    ["j2735_2016.id", "j2735_2016.coreData_element", 4, 1, 4, 00, True],
    ["j2735_2016.secMark", "j2735_2016.coreData_element", 2, 0, 0, 65535, True],
    ["j2735_2016.lat", "j2735_2016.coreData_element", 4, 0, -900000000, 900000001, True],
    ["j2735_2016.long", "j2735_2016.coreData_element", 4, 0, -1799999999, 1800000001, True],
    ["j2735_2016.elev", "j2735_2016.coreData_element", 2, 0, -4096, 61439, True],
    ["j2735_2016.semiMajor", "j2735_2016.accuracy_element", 1, 0, 0, 255, True],
    ["j2735_2016.semiMinor", "j2735_2016.accuracy_element", 1, 0, 0, 255, True],
    ["j2735_2016.orientation", "j2735_2016.accuracy_element", 2, 0, 0, 65535, True],
    ["j2735_2016.transmission", "j2735_2016.coreData_element", 1, 0, 0, 7, True],
    ["j2735_2016.speed", "j2735_2016.coreData_element", 2, 0, 0, 8191, True],
    ["j2735_2016.heading", "j2735_2016.coreData_element", 2, 0, 0, 28800, True],
    ["j2735_2016.angle", "j2735_2016.coreData_element", 1, 0, -126, 127, True],
    ["j2735_2016.long", "j2735_2016.accelSet_element", 2, 0, -2000, 2001, True],
    ["j2735_2016.lat", "j2735_2016.accelSet_element", 2, 0, -2000, 2001, True],
    ["j2735_2016.vert", "j2735_2016.accelSet_element", 1, 0, -127, 127, True],
    ["j2735_2016.yaw", "j2735_2016.accelSet_element", 2, 0, -32767, 32767, True],
    ["j2735_2016.wheelBrakes", "j2735_2016.brakes_element", 1, 2, 5, 00, True],
    ["j2735_2016.traction", "j2735_2016.brakes_element", 1, 0, 0, 3, True],
    ["j2735_2016.abs", "j2735_2016.brakes_element", 1, 0, 0, 3, True],
    ["j2735_2016.scs", "j2735_2016.brakes_element", 1, 0, 0, 3, True],
    ["j2735_2016.brakeBoost", "j2735_2016.brakes_element", 1, 0, 0, 2, True],
    ["j2735_2016.auxBrakes", "j2735_2016.brakes_element", 1, 0, 0, 2, True],
    ["j2735_2016.width", "j2735_2016.size_element", 2, 0, 0, 1023, True],
    ["j2735_2016.length", "j2735_2016.size_element", 2, 0, 0, 4095, True],
    ["j2735_2016.partII.Id", "j2735_2016.PartIIcontent_element", 1, 0, 0, 63, False],  # start of partII (optional)
    ["j2735_2016.events", "j2735_2016.PartII_Value_element", 2, 2, 13, 00, False],
    ["j2735_2016.year", "j2735_2016.utcTime_element", 2, 0, 0, 4095, False],
    ["j2735_2016.month", "j2735_2016.utcTime_element", 1, 0, 0, 12, False],
    ["j2735_2016.day", "j2735_2016.utcTime_element", 1, 0, 0, 31, False],
    ["j2735_2016.hour", "j2735_2016.utcTime_element", 1, 0, 0, 31, False],
    ["j2735_2016.minute", "j2735_2016.utcTime_element", 1, 0, 0, 60, False],
    ["j2735_2016.second", "j2735_2016.utcTime_element", 2, 0, 0, 65535, False],
    ["j2735_2016.offset", "j2735_2016.utcTime_element", 2, 0, -840, 840, False],
    ["j2735_2016.long", "j2735_2016.initialPosition_element", 4, 0, -1799999999, 1800000001, False],
    ["j2735_2016.lat", "j2735_2016.initialPosition_element", 4, 0, -900000000, 900000001, False],
    ["j2735_2016.elevation", "j2735_2016.initialPosition_element", 2, 0, -4096, 61439, False],
    ["j2735_2016.heading", "j2735_2016.initialPosition_element", 2, 0, 0, 28800, False],
    ["j2735_2016.transmission", "j2735_2016.TransmissionAndSpeed_element", 1, 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.TransmissionAndSpeed_element", 2, 0, 0, 8191, False],
    ["j2735_2016.semiMajor", "j2735_2016.posAccuracy_element", 1, 0, 0, 255, False],
    ["j2735_2016.semiMinor", "j2735_2016.posAccuracy_element", 1, 0, 0, 255, False],
    ["j2735_2016.orientation", "j2735_2016.posAccuracy_element", 2, 0, 0, 65535, False],
    ["j2735_2016.timeConfidence", "j2735_2016.initialPosition_element", 1, 0, 0, 39, False],
    ["j2735_2016.pos", "j2735_2016.posConfidence_element", 1, 0, 0, 15, False],
    ["j2735_2016.elevation", "j2735_2016.posConfidence_element", 1, 0, 0, 15, False],
    ["j2735_2016.heading", "j2735_2016.speedConfidence_element", 1, 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.speedConfidence_element", 1, 0, 0, 7, False],
    ["j2735_2016.throttle", "j2735_2016.speedConfidence_element", 1, 0, 0, 3, False],
    ["j2735_2016.radiusOfCurve", "j2735_2016.pathPrediction_element", 2, 0, -32767, 32767, False],
    ["j2735_2016.confidence", "j2735_2016.pathPrediction_element", 1, 0, 0, 200, False],
    ["j2735_2016.lights", "j2735_2016.PartII_Value_element", 2, 3, 9, 00, False],
    ["j2735_2016.sspRights", "j2735_2016.vehicleAlerts_element", 1, 0, 0, 31, False],
    ["j2735_2016.sirenUse", "j2735_2016.vehicleAlerts_element", 1, 0, 0, 3, False],
    ["j2735_2016.lightsUse", "j2735_2016.vehicleAlerts_element", 1, 0, 0, 63, False],
    ["j2735_2016.multi", "j2735_2016.vehicleAlerts_element", 1, 0, 0, 3, False],
    ["j2735_2016.sspRights", "j2735_2016.events_element", 1, 0, 0, 31, False],
    ["j2735_2016.event", "j2735_2016.events_element", 2, 2, 16, 00, False],
    ["j2735_2016.responseType", "j2735_2016.vehicleAlerts_element", 1, 0, 0, 6, False],
    ["j2735_2016.typeEvent", "j2735_2016.description_element", 2, 0, 0, 65535, False],
    ["j2735_2016.priority", "j2735_2016.description_element", 1, 1, 1, 00, False],
    ["j2735_2016.heading", "j2735_2016.description_element", 2, 2, 16, 00, False],
    ["j2735_2016.extent", "j2735_2016.description_element", 1, 0, 0, 15, False],
    ["j2735_2016.sspRights", "j2735_2016.trailers_element", 1, 0, 0, 31, False],
    ["j2735_2016.pivotOffset", "j2735_2016.connection_element", 1, 0, -1024, 1023, False],
    ["j2735_2016.pivotAngle", "j2735_2016.connection_element", 2, 0, 0, 28800, False],
    ["j2735_2016.pivots", "j2735_2016.connection_element", 1, 3, 0, 00, False],
    ["j2735_2016.classification", "j2735_2016.PartII_Value_element", 1, 0, 0, 255, False],
    ["j2735_2016.keyType", "j2735_2016.classDetails_element", 1, 0, 0, 255, False],
    ["j2735_2016.role", "j2735_2016.classDetails_element", 1, 0, 0, 22, False],
    ["j2735_2016.iso3883", "j2735_2016.classDetails_element", 1, 0, 0, 100, False],
    ["j2735_2016.hpmsType", "j2735_2016.classDetails_element", 1, 0, 0, 15, False],
    ["j2735_2016.vehicleType", "j2735_2016.classDetails_element", 1, 0, 0, 15, False],
    ["j2735_2016.responseEquip", "j2735_2016.classDetails_element", 2, 9985, 10113, False],
    ["j2735_2016.responderType", "j2735_2016.classDetails_element", 2, 9729, 9742, False],
    ["j2735_2016.fuelType", "j2735_2016.classDetails_element", 1, 0, 0, 15, False],
    ["j2735_2016.height", "j2735_2016.vehicleData_element", 1, 0, 0, 127, False],
    ["j2735_2016.front", "j2735_2016.bumpers_element", 1, 0, 0, 127, False],
    ["j2735_2016.rear", "j2735_2016.bumpers_element", 1, 0, 0, 127, False],
    ["j2735_2016.mass", "j2735_2016.vehicleData_element", 1, 0, 0, 255, False],
    ["j2735_2016.trailerWeight", "j2735_2016.vehicleData_element", 2, 0, 0, 64255, False],
    ["j2735_2016.front", "j2735_2016.bumpers_element", 1, 0, 0, 127, False],
    ["j2735_2016.isRaining", "j2735_2016.weatherReport_element", 1, 1, 3, False],
    ["j2735_2016.rainRate", "j2735_2016.weatherReport_element", 2, 0, 0, 65535, False],
    ["j2735_2016.precipSituation", "j2735_2016.weatherReport_element", 1, 1, 15, False],
    ["j2735_2016.solarRadiation", "j2735_2016.weatherReport_element", 2, 0, 0, 65535, False],
    ["j2735_2016.friction", "j2735_2016.weatherReport_element", 1, 0, 0, 101, False],
    ["j2735_2016.roadFriction", "j2735_2016.weatherReport_element", 1, 0, 0, 50, False],
    ["j2735_2016.airTemp", "j2735_2016.weatherProbe_element", 1, 0, 0, 191, False],
    ["j2735_2016.airPressure", "j2735_2016.weatherProbe_element", 1, 0, 0, 255, False],
    ["j2735_2016.statusFront", "j2735_2016.rainRates_element", 1, 0, 0, 6, False],
    ["j2735_2016.rateFront", "j2735_2016.rainRates_element", 1, 0, 0, 127, False],
    ["j2735_2016.statusRear", "j2735_2016.rainRates_element", 1, 0, 0, 6, False],
    ["j2735_2016.rateRear", "j2735_2016.rainRates_element", 1, 0, 0, 127, False],
    ["j2735_2016.obDist", "j2735_2016.obstacle_element", 1, 0, 0, 32767, False],
    ["j2735_2016.obDist", "j2735_2016.obstacle_element", 1, 0, 0, 28800, False],
    ["j2735_2016.year", "j2735_2016.dateTime_element", 2, 0, 0, 4095, False],
    ["j2735_2016.month", "j2735_2016.dateTime_element", 1, 0, 0, 12, False],
    ["j2735_2016.day", "j2735_2016.dateTime_element", 1, 0, 0, 31, False],
    ["j2735_2016.hour", "j2735_2016.dateTime_element", 1, 0, 0, 31, False],
    ["j2735_2016.minute", "j2735_2016.dateTime_element", 1, 0, 0, 60, False],
    ["j2735_2016.second", "j2735_2016.dateTime_element", 2, 0, 0, 65535, False],
    ["j2735_2016.offset", "j2735_2016.dateTime_element", 2, 0, -840, 840, False],
    ["j2735_2016.vertEvent", "j2735_2016.obstacle_element", 1, 2, 5, 00, False],
    ]
saej2735_bsm_refdf = pd.DataFrame(saej2735_bsm_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])

saej2735_spat_ref = [
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 2, 0, 0, 527040, False],
    ["j2735_2016.region", "j2735_2016.id_element", 2, 0, 0, 65535, False],
    ["j2735_2016.id", "j2735_2016.id_element", 2, 0, 0, 65535, True],
    ["j2735_2016.revision", "j2735_2016.IntersectionState_element", 1, 0, 0, 127, True],
    ["j2735_2016.status", "j2735_2016.IntersectionState_element", 2, 2, 16, 00, True],
    ["j2735_2016.moy", "j2735_2016.IntersectionState_element", 2, 0, 0, 527040, False],
    ["j2735_2016.timeStamp", "j2735_2016.IntersectionState_element", 2, 0, 0, 65535, False],
    ["j2735_2016.laneID", "j2735_2016.IntersectionState_element", 2, 0, 0, 255, False],
    ["j2735_2016.signalGroup", "j2735_2016.MovementState_element", 1, 0, 0, 255, True],
    ["j2735_2016.eventState", "j2735_2016.MovementEvent_element", 1, 0, 0, 9, True],
    ["j2735_2016.startTime", "j2735_2016.timing_element", 2, 0, 0, 36001, False],
    ["j2735_2016.minEndTime", "j2735_2016.timing_element", 2, 0, 0, 36001, False],
    ["j2735_2016.maxEndTime", "j2735_2016.timing_element", 2, 0, 0, 36001, False],
    ["j2735_2016.likelyTime", "j2735_2016.timing_element", 2, 0, 0, 36001, False],
    ["j2735_2016.confidence", "j2735_2016.timing_element", 2, 0, 0, 15, False],
    ["j2735_2016.nextTime", "j2735_2016.timing_element", 2, 0, 0, 36001, False],
    ["j2735_2016.type", "j2735_2016.AdvisorySpeed_element", 1, 0, 0, 3, False],
    ["j2735_2016.speed", "j2735_2016.AdvisorySpeed_element", 2, 0, 0, 500, False], # double length problem
    ["j2735_2016.confidence", "j2735_2016.AdvisorySpeed_element", 2, 0, 0, 7, False],
    ["j2735_2016.distance", "j2735_2016.AdvisorySpeed_element", 2, 0, 0, 10000, False], # double length problem
    ["j2735_2016.class", "j2735_2016.AdvisorySpeed_element", 2, 0, 0, 255, False],
    ["j2735_2016.connectionID", "j2735_2016.ConnectionManeuverAssist_element", 2, 0, 0, 10000, False],
    ["j2735_2016.queueLength", "j2735_2016.ConnectionManeuverAssist_element", 2, 0, 0, 10000, False],
    ["j2735_2016.availableStorageLength", "j2735_2016.ConnectionManeuverAssist_element", 2, 0, 0, 10000, False],
    ["j2735_2016.waitOnStop", "j2735_2016.ConnectionManeuverAssist_element", 1, 3, 00, 00, False],
    ["j2735_2016.pedBicycleDetect", "j2735_2016.ConnectionManeuverAssist_element", 1, 3, 00, 00, False],
]
saej2735_spat_refdf = pd.DataFrame(saej2735_spat_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])

saej2735_rsa_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 1, 0, 0, 127, True],
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 3, 0, 0, 527040, False],
    ["j2735_2016.typeEvent", "j2735_2016.value_element", 2, 0, 0, 65535, True],
    ["j2735_2016.priority", "j2735_2016.value_element", 1, 1, 1, 00, False],
    ["j2735_2016.extent", "j2735_2016.value_element", 1, 0, 0, 15, False],
    ["j2735_2016.year", "j2735_2016.utcTime", 2, 0, 0, 4095, False],
    ["j2735_2016.month", "j2735_2016.utcTime", 1, 0, 0, 12, False],
    ["j2735_2016.day", "j2735_2016.utcTime", 1, 0, 0, 31, False],
    ["j2735_2016.hour", "j2735_2016.utcTime", 1, 0, 0, 31, False],
    ["j2735_2016.long", "j2735_2016.position_element", 4, 0, -1799999999, 1800000001, False],
    ["j2735_2016.lat", "j2735_2016.position_element", 4, 0, -900000000, 900000001, False],
    ["j2735_2016.elevation", "j2735_2016.position_element", 2, 0, -4096, 61439, False],
    ["j2735_2016.heading", "j2735_2016.position_element", 2, 0, 0, 28800, False],
    ["j2735_2016.transmission", "j2735_2016.speed_element", 1, 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.speed_element", 1, 0, 0, 8191, False],
    ["j2735_2016.semiMajor", "j2735_2016.posAccuracy_element", 1, 0, 0, 255, False],
    ["j2735_2016.semiMinor", "j2735_2016.posAccuracy_element", 1, 0, 0, 255, False],
    ["j2735_2016.orientation", "j2735_2016.posAccuracy_element", 2, 0, 0, 65535, False],
    ["j2735_2016.timeConfidence", "j2735_2016.position_element", 1, 0, 0, 39, False],
    ["j2735_2016.pos", "j2735_2016.posConfidence_element", 1, 0, 0, 15, False],
    ["j2735_2016.elevation", "j2735_2016.posConfidence_element", 1, 0, 0, 15, False],
    ["j2735_2016.heading", "j2735_2016.speedConfidence_element", 1, 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.speedConfidence_element", 1, 0, 0, 7, False],
    ["j2735_2016.throttle", "j2735_2016.speedConfidence_element", 1, 0, 0, 3, False],
    ["j2735_2016.furtherInfoID", "j2735_2016.value_element", 2, 1, 2, 00, False],
]
saej2735_rsa_refdf = pd.DataFrame(saej2735_rsa_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])

saej2735_tim_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 1, 0, 0, 127, True],
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 2, 0, 0, 527040, False],
    ["j2735_2016.packetID", "j2735_2016.value_element", 9, 1, 9, 00, False],
    ["j2735_2016.sspTimRights", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 31, True],
    ["j2735_2016.frameType", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 3, True],
    ["j2735_2016.lat", "j2735_2016.position_element", 4, 0, -900000000, 900000001, True],
    ["j2735_2016.long", "j2735_2016.position_element", 4, 0, -1799999999, 1800000001, True],
    ["j2735_2016.elevation", "j2735_2016.position_element", 2, 0, -4096, 61439, False],
    ["j2735_2016.viewAngle", "j2735_2016.roadSignID_element", 2, 2, 16, 00, True],
    ["j2735_2016.mutcdCode", "j2735_2016.roadSignID_element", 1, 0, 0, 6, False],
    ["j2735_2016.crc", "j2735_2016.roadSignID_element", 2, 1, 2, 00, False],
    ["j2735_2016.startYear", "j2735_2016.TravelerDataFrame_element", 2, 0, 0, 4095, False],
    ["j2735_2016.startTime", "j2735_2016.TravelerDataFrame_element", 3, 0, 0, 527040, True],
    ["j2735_2016.durationTime", "j2735_2016.TravelerDataFrame_element", 2, 0, 0, 32000, False], # problem, should be mandatory
    ["j2735_2016.priority", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 7, True],
    ["j2735_2016.sspLocationRights", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 31, True],
    ["j2735_2016.region", "j2735_2016.id_element", 2, 0, 0, 65535, False],
    ["j2735_2016.id", "j2735_2016.id_element", 2, 0, 0, 65535, False],
    ["j2735_2016.lat", "j2735_2016.anchor_element", 4, 0, -900000000, 900000001, False],
    ["j2735_2016.long", "j2735_2016.anchor_element", 4, 0, -1799999999, 1800000001, False],
    ["j2735_2016.elevation", "j2735_2016.anchor_element", 2, 0, -4096, 61439, False],
    ["j2735_2016.laneWidth", "j2735_2016.GeographicalPath_element", 2, 0, 0, 32767, False],
    ["j2735_2016.directionality", "j2735_2016.GeographicalPath_element", 1, 0, 0, 3, False],
    ["j2735_2016.closedPath", "j2735_2016.GeographicalPath_element", 1, 3, 00, 00, False],
    ["j2735_2016.direction", "j2735_2016.GeographicalPath_element", 2, 2, 16, 00, False],
    ["j2735_2016.scale", "j2735_2016.path_element", 2, 0, 0, 15, False],
    ["j2735_2016.x", "j2735_2016.node_XY6_element", 2, 0, -32768, 32767, False],
    ["j2735_2016.y", "j2735_2016.node_XY6_element", 2, 0, -32768, 32767, False],
    ["j2735_2016.NodeAttributeXY", "j2735_2016.localNode_element", 2, 0, 0, 11, False],
    ["j2735_2016.SegmentAttributeXY", "j2735_2016.disabled", 2, 0, 0, 37, False],
    ["j2735_2016.SegmentAttributeXY", "j2735_2016.enabled", 2, 0, 0, 37, False],
    ["j2735_2016.dWidth", "j2735_2016.attributes_element", 2, 0, -512, 511, False],
    ["j2735_2016.dElevation", "j2735_2016.attributes_element", 2, 0, -512, 511, False],
    ["j2735_2016.dWidth", "j2735_2016.attributes_element", 2, 0, -512, 511, False],
    ["j2735_2016.sspMsgRights1", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 31, True],
    ["j2735_2016.sspMsgRights2", "j2735_2016.TravelerDataFrame_element", 1, 0, 0, 31, True],
]
saej2735_tim_refdf = pd.DataFrame(saej2735_tim_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])

saej2735_map_ref = [
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 3, 0, 0, 527040, False],
    ["j2735_2016.msgIssueRevision", "j2735_2016.value_element", 1, 0, 0, 127, True],
    ["j2735_2016.layerType", "j2735_2016.value_element", 1, 0, 0, 7, False],
    ["j2735_2016.layerID", "j2735_2016.value_element", 1, 0, 0, 100, False],
    ["j2735_2016.region", "j2735_2016.id_element", 2, 0, 0, 65535, False],
    ["j2735_2016.id", "j2735_2016.id_element", 2, 0, 0, 65535, False],
    ["j2735_2016.revision", "j2735_2016.IntersectionGeometry_element", 1, 0, 0, 127, True],
    ["j2735_2016.lat", "j2735_2016.refPoint_element", 4, 0, -900000000, 900000001, True],
    ["j2735_2016.long", "j2735_2016.refPoint_element", 4, 0, -1799999999, 1800000001, True],
    ["j2735_2016.elevation", "j2735_2016.refPoint_element", 2, 0, -4096, 61439, False],
    ["j2735_2016.laneWidth", "j2735_2016.IntersectionGeometry_element", 2, 0, 0, 32767, False],
    ["j2735_2016.type", "j2735_2016.RegulatorySpeedLimit_element", 1, 0, 0, 12, False],
    ["j2735_2016.speed", "j2735_2016.RegulatorySpeedLimit_element", 2, 0, 0, 8191, False],
    ["j2735_2016.laneID", "j2735_2016.GenericLane_element", 1, 0, 0, 255, True],
    ["j2735_2016.ingressApproach", "j2735_2016.GenericLane_element", 1, 0, 0, 15, False],
    ["j2735_2016.egressApproach", "j2735_2016.GenericLane_element", 1, 0, 0, 15, False],
    ["j2735_2016.directionalUse", "j2735_2016.laneAttributes_element", 1, 2, 2, 0, True],
    ["j2735_2016.sharedWith", "j2735_2016.laneAttributes_element", 2, 2, 10, 0, True],
    ["j2735_2016.laneType", "j2735_2016.laneAttributes_element", 4, 0, 0, 7, True],
    ["j2735_2016.vehicle", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.crosswalk", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.bikeLane", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.sidewalk", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.median", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.striping", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.trackedVehicle", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.parking", "j2735_2016.laneType", 2, 2, 16, 00, False],
    ["j2735_2016.maneuvers", "j2735_2016.GenericLane_element", 2, 2, 12, 00, False],
    ["j2735_2016.x", "j2735_2016.node_XY6_element", 2, 0, -32768, 32767, True],
    ["j2735_2016.y", "j2735_2016.node_XY6_element", 2, 0, -32768, 32767, True],
    ["j2735_2016.NodeAttributeXY", "j2735_2016.localNode_element", 1, 0, 0, 11, False],
    ["j2735_2016.SegmentAttributeXY", "j2735_2016.enabled_element", 1, 0, 0, 37, False],
    ["j2735_2016.SegmentAttributeXY", "j2735_2016.disabled_element", 1, 0, 0, 37, False],
    ["j2735_2016.pathEndPointAngle", "j2735_2016.LaneDataAttribute_element", 1, 0, -150, 150, False],
    ["j2735_2016.laneCrownPointCenter", "j2735_2016.LaneDataAttribute_element", 1, 0, -128, 127, False],
    ["j2735_2016.laneCrownPointLeft", "j2735_2016.LaneDataAttribute_element", 1, 0, -128, 127, False],
    ["j2735_2016.laneCrownPointRight", "j2735_2016.LaneDataAttribute_element", 1, 0, -128, 127, False],
    ["j2735_2016.laneAngle", "j2735_2016.LaneDataAttribute_element", 1, 0, -180, 180, False],
    ["j2735_2016.type", "j2735_2016.RegulatorySpeedLimit_element", 1, 0, 0, 12, False],
    ["j2735_2016.speed", "j2735_2016.RegulatorySpeedLimit_element", 2, 0, 0, 8191, False],
    ["j2735_2016.dWidth", "j2735_2016.attributes_element", 2, 0, -512, 511, False],
    ["j2735_2016.dElevation", "j2735_2016.attributes_element", 2, 0, -512, 511, False],
    ["j2735_2016.lane", "j2735_2016.connectingLane_element", 1, 0, 0, 255, False],
    ["j2735_2016.maneuver", "j2735_2016.connectingLane_element", 2, 2, 12, 0, False],
    ["j2735_2016.region", "j2735_2016.remoteIntersection_element", 2, 0, 0, 65535, False],
    ["j2735_2016.id", "j2735_2016.remoteIntersection_element", 2, 0, 0, 65535, False],
    ["j2735_2016.signalGroup", "j2735_2016.Connection_element", 1, 0, 0, 255, False],
    ["j2735_2016.userClass", "j2735_2016.Connection_element", 1, 0, 0, 255, False],
    ["j2735_2016.connectionID", "j2735_2016.Connection_element", 1, 0, 0, 255, False],
    ["j2735_2016.LaneID", "j2735_2016.overlays_element", 1, 0, 0, 255, False]
]
saej2735_map_refdf = pd.DataFrame(saej2735_map_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"]) 

ieee16093_wsmp_ref = [
    ["16093.version", "16093", 1, 0, 3, 3, True],
    ["16093.subtype", "16093", 1, 0, 0, 0, True],
    ["16093.option", "16093", 1, 3, 00, 00, True],
    ["16093.n_ext", "16093", 1, 0, 0, 5, False],
    ["16093.channel", "16093", 1, 1, 1, 00, False],
    ["16093.rate", "16093", 1, 0, 2, 127, False],
    ["16093.txpower", "16093", 1, 0, -128, 127, False],
    ["16093.load", "16093", 1, 1, 1, 00, False],
    ["16093.confidence", "16093", 1, 0, 0, 7, False],
    ["16093.tpid", "16093", 1, 0, 0, 5, True],
    ["16093.psid", "16093", 4, 0, 0, 4294967295, True],
    ["16093.length", "16093", 2, 0, 0, 16383, True],
]
ieee16093_wsmp_refdf = pd.DataFrame(ieee16093_wsmp_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])

# GLOBAL ACCESSED DATAFRAMES/VARIABLES
assessdf = pd.DataFrame(columns=["field", "parent", "length", "value", "compliant", "occurrences"]) # DataFrame where each row is the overalls of analysis for a field.
faildf = pd.DataFrame(columns=["field", "parent", "length", "value", "occurrences", "fail description"])   # DataFrame where each row is the overalls of analysis for a FAILED field.

iop_overall = True
iop_fail_desc = ""

# DEFINE QUANTITATIVE EVALUATION METHODS
# Eval Method 0: compare with max, min
def compare_min_max(row, fieldval):
    minval = row.get('val1').values[0]
    maxval = row.get('val2').values[0]
    if((minval <= fieldval) and (fieldval <= maxval)):
        return True
    else:
        return False

# Eval Method 1: octet count
def octet_count(row, fieldlen):
    targetval = row.get('val1').values[0]
    if((fieldlen > 0) and (fieldlen <= targetval)):
        return True
    else:
        return False
    
# Eval Method 2: bit string
def bit_string(row, field, fieldname):
    global iop_fail_desc
    target_bitlen = row.get('val1').values[0]
    try:
        field_bitlen = int(re.findall(r"bit length (\d+)", field.attrib.get('showname'))[0])
    except IndexError:
        iop_fail_desc = iop_fail_desc + "Incorrect format for bit string. "
        return False
    if (field_bitlen == target_bitlen):
        return True
    else:
        return False

# Eval Method 3: boolean
def boolean_check(row, fieldval):
    if((fieldval == 0) or (fieldval == 1)):
        return True
    else:
        return False

# ANALYZE PDML METHOD: Given a tree (parsed XML file), will iterate through every field of each relevant message to determine interoperability and compliance to standards.
def analyze(tree):
    global iop_overall
    global iop_fail_desc
    for packet in tree.getroot():   # recursively move through packets/protocols
        for proto in packet:
            refdf = None
            if ("j2735" in proto.attrib.get('name')):
                messageId = proto.find(".//field[@name='j2735_2016.messageId']")
                if (messageId != None):
                    # DETERMINE MESSAGE TYPE
                    codenum = int(messageId.attrib.get('show'))
                    match codenum:
                        case 20:    # BSM
                            print(messageId.attrib.get('showname'))
                            print("-------------------------------------------") 
                            refdf = saej2735_bsm_refdf
                        case 27:    # RSA
                            print(messageId.attrib.get('showname'))
                            print("-------------------------------------------") 
                            refdf = saej2735_rsa_refdf
                        case 19:    # SPaT
                            print(messageId.attrib.get('showname'))
                            print("-------------------------------------------") 
                            refdf = saej2735_spat_refdf
                        case 31:    # TIM
                            print(messageId.attrib.get('showname'))
                            print("-------------------------------------------") 
                            refdf = saej2735_tim_refdf
                        case 18:    # MAP
                            print(messageId.attrib.get('showname'))
                            print("-------------------------------------------") 
                            refdf = saej2735_map_refdf
                        case _:
                            iop_overall = False
                            # iop_fail_desc = iop_fail_desc + "Invalid messageId: " + messageId + "\n"
            elif ("16093" in proto.attrib.get('name')):
                print(proto.attrib.get('showname'))
                print("-------------------------------------------") 
                refdf = ieee16093_wsmp_refdf 
                     

            # SET MESSAGE REFERENCE TABLE VARIABLES FOR SEQUENCE CHECKING
            if ((refdf is not None) and (not refdf.empty)):
                mand_index = 0 
                while ((refdf.iloc[mand_index].get('mandatory') != True)):
                    mand_index += 1

                lastmand_index = len(refdf.index) - 1
                while (refdf.iloc[lastmand_index].get('mandatory') != True):
                    lastmand_index -= 1
            
                # -------IoP ANALYSIS-------
                for field in proto.iter():  # iteratively move through fields
                    iop_tag = True
                    iop_length = True
                    iop_value = True
                    iop_sequence = True
                    iop_field = True
                    iop_fail_desc = ""

                    parentname = str(field.getparent().attrib.get('name'))
                    fieldname = str(field.attrib.get('name'))
                    fieldlen = int(field.attrib.get('size'), 10)
                    
                    if (fieldname == "per.optional_field_bit"): # optional field handler
                        if ("True" in str(field.attrib.get('showname'))):
                            fieldname = "j2735_2016." + re.findall(r'\(([^ ]+?) ', field.attrib.get('showname'))[0]
                        else:
                            continue

                    row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)]    # get row based on field name and parent name

                    if ((len(row.index) != 1)): # (there should only be 1 entry per unique pair of field name and parent name)
                        if ((len(row.index) != 0) and not row.empty):
                            iop_tag = False
                            iop_fail_desc = iop_fail_desc + "Invalid/Repeated tag. "
                    else:
                        # SEQUENCE CHECKING
                        fieldmand_ref = row.get('mandatory').values[0]
                        lastmand_reached = False
                        if (fieldmand_ref): # if field is mandatory
                            if (mand_index == lastmand_index):  # if reached the end of the mandatory fields in table
                                    lastmand_reached = True
                            if ((fieldname != refdf.iloc[mand_index].get('field')) and not lastmand_reached):   # if current (mandatory) field does not match the intended mandatory field in sequence
                                iop_sequence = False
                                iop_fail_desc = iop_fail_desc + "Sequence incorrect: should be " + refdf.iloc[mand_index].get('field') + ". "
                            else:
                                if (mand_index < lastmand_index):   # if haven't reached the end of the mandatory fields in table
                                    mand_index += 1
                                    while ((refdf.iloc[mand_index].get('mandatory') != True) and (mand_index < lastmand_index)):    # go to next mandatory field in table
                                        mand_index += 1
                        print("Tag:", fieldname, ">", iop_tag)
                        
                        # LENGTH EVALUATION
                        if ((fieldlen < 1) or (fieldlen > row.get('length').values[0])):
                            iop_length = False
                            iop_fail_desc = iop_fail_desc + "Incorrect length: " + str(fieldlen) + " should be " + str(row.get('length').values[0]) + ". "
                        print("Length:", fieldlen, ">", iop_length)
                        
                        # CONVERT STRING (FROM DATAFILE) TO INT VALUES    
                        try: 
                            fieldval = int(field.attrib.get('show'), 10)
                        except ValueError:
                            fieldval = int(field.attrib.get('value'), 16) 

                        # QUANTITATIVE (VALUE) EVALUATION
                        eval_method = row.get('eval method').values[0]
                        match eval_method:  # determine how the field should be evaluated based on standard
                            case 0:
                                iop_value = compare_min_max(row, fieldval)
                            case 1:
                                iop_value = octet_count(row, fieldlen)
                            case 2:
                                iop_value = bit_string(row, field, fieldname)
                            case 3:
                                iop_value = boolean_check(row, fieldval)
                            case _:
                                iop_value = False
                                iop_fail_desc = iop_fail_desc + "Invalid evaluation method. "
                                continue 
                        if (not iop_value):   # field failed evaluation
                            iop_fail_desc = iop_fail_desc + "Value out of range. "
                        print("Value:", fieldval, ">", iop_value) 
                        
                        # SAVE RESULTS
                        if (not iop_tag or not iop_length or not iop_value or not iop_sequence):
                            iop_field = False
                            iop_overall = False               
                            row_fail = faildf.loc[(faildf['field'] == fieldname) & (faildf['parent'] == parentname)]
                            if (len(row_fail) != 0):
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, row_fail.tail(1).get('occurrences').values[0] + 1, iop_fail_desc.rstrip()]
                            else:
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, 1, iop_fail_desc.rstrip()]

                        row_assess = assessdf.loc[(assessdf['field'] == fieldname) & (assessdf['parent'] == parentname) & (assessdf['compliant'] == iop_field)]
                        if (len(row_assess) != 0):
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, iop_field, row_assess.tail(1).get('occurrences').values[0] + 1]
                        else:
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, iop_field, 1]

                        print("Field Compliant:", iop_field)    
                        print("Interoperable:", iop_overall, "\n")

    # PRINT overallS
    print("-------------------------------------------------------------------------------------------------------------------\n")
    if (iop_overall):
        print("Interoperability: PASS")
    else:
        print("Interoperability: FAIL")
        print(faildf)
    print("\n-------------------------------------------------------------------------------------------------------------------\n")
    print(assessdf)

def main():
   try:
       inFile = sys.argv[1]
   except IndexError:
       print("Error: Specify a pdml file.")
       sys.exit(1)
   print("Parsing...")
   tree = etree.parse(inFile)
   print("Analyzing...\n")
   analyze(tree)

if __name__ == "__main__":
    main()