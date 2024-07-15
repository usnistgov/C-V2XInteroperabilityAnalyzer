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
saej2735_bsm_ref = [    # col[0] = field name, col[1] = parent name, col[2]] = eval method, col[3] = ref value 1, col[4] = ref value 2, col[5] = mandatory?
    ["j2735_2016.msgCnt", "j2735_2016.coreData_element", 0, 0, 127, True], # start of coreData (mandatory)
    ["j2735_2016.id", "j2735_2016.coreData_element", 1, 4, 00, True],
    ["j2735_2016.secMark", "j2735_2016.coreData_element", 0, 0, 65535, True],
    ["j2735_2016.lat", "j2735_2016.coreData_element", 0, -900000000, 900000001, True],
    ["j2735_2016.long", "j2735_2016.coreData_element", 0, -1799999999, 1800000001, True],
    ["j2735_2016.elev", "j2735_2016.coreData_element", 0, -4096, 61439, True],
    ["j2735_2016.semiMajor", "j2735_2016.accuracy_element", 0, 0, 255, True],
    ["j2735_2016.semiMinor", "j2735_2016.accuracy_element", 0, 0,255, True],
    ["j2735_2016.orientation", "j2735_2016.accuracy_element", 0, 0, 65535, True],
    ["j2735_2016.transmission", "j2735_2016.coreData_element", 0, 0, 7, True],
    ["j2735_2016.speed", "j2735_2016.coreData_element", 0, 0, 8191, True],
    ["j2735_2016.heading", "j2735_2016.coreData_element", 0, 0, 28800, True],
    ["j2735_2016.angle", "j2735_2016.coreData_element", 0, -126, 127, True],
    ["j2735_2016.long", "j2735_2016.accelSet_element", 0, -2000, 2001, True],
    ["j2735_2016.lat", "j2735_2016.accelSet_element", 0, -2000, 2001, True],
    ["j2735_2016.vert", "j2735_2016.accelSet_element", 0, -127, 127, True],
    ["j2735_2016.yaw", "j2735_2016.accelSet_element", 0, -32767, 32767, True],
    ["j2735_2016.wheelBrakes", "j2735_2016.brakes_element", 2, 5, 00, True],
    ["j2735_2016.traction", "j2735_2016.brakes_element", 0, 0, 3, True],
    ["j2735_2016.abs", "j2735_2016.brakes_element", 0, 0, 3, True],
    ["j2735_2016.scs", "j2735_2016.brakes_element", 0, 0, 3, True],
    ["j2735_2016.brakeBoost", "j2735_2016.brakes_element", 0, 0, 2, True],
    ["j2735_2016.auxBrakes", "j2735_2016.brakes_element", 0, 0, 2, True],
    ["j2735_2016.width", "j2735_2016.size_element", 0, 0, 1023, True],
    ["j2735_2016.length", "j2735_2016.size_element", 0, 0, 4095, True],
    ["j2735_2016.partII.Id", "j2735_2016.PartIIcontent_element", 0, 0, 63, False], # start of partII (optional)
    ["j2735_2016.events", "j2735_2016.PartII_Value_element", 2, 13, 00, False],
    ["j2735_2016.year", "j2735_2016.utcTime_element", 0, 0, 4095, False],
    ["j2735_2016.month", "j2735_2016.utcTime_element", 0, 0, 12, False],
    ["j2735_2016.day", "j2735_2016.utcTime_element", 0, 0, 31, False],
    ["j2735_2016.hour", "j2735_2016.utcTime_element", 0, 0, 31, False],
    ["j2735_2016.minute", "j2735_2016.utcTime_element", 0, 0, 60, False],
    ["j2735_2016.second", "j2735_2016.utcTime_element", 0, 0, 65535, False],
    ["j2735_2016.offset", "j2735_2016.utcTime_element", 0, -840, 840, False],
    ["j2735_2016.long", "j2735_2016.initialPosition_element", 0, -1799999999, 1800000001, False],
    ["j2735_2016.lat", "j2735_2016.initialPosition_element", 0, -900000000, 900000001, False],
    ["j2735_2016.elevation", "j2735_2016.initialPosition_element", 0, -4096, 61439, False],
    ["j2735_2016.heading", "j2735_2016.initialPosition_element", 0, 0, 28800, False],
    ["j2735_2016.transmission", "j2735_2016.TransmissionAndSpeed_element", 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.TransmissionAndSpeed_element", 0, 0, 8191, False],
    ["j2735_2016.semiMajor", "j2735_2016.posAccuracy_element", 0, 0, 255, False],
    ["j2735_2016.semiMinor", "j2735_2016.posAccuracy_element", 0, 0, 255, False],
    ["j2735_2016.orientation", "j2735_2016.posAccuracy_element", 0, 0, 65535, False],
    ["j2735_2016.timeConfidence", "j2735_2016.initialPosition_element", 0, 0, 39, False],
    ["j2735_2016.pos", "j2735_2016.posConfidence_element", 0, 0, 15, False],
    ["j2735_2016.elevation", "j2735_2016.posConfidence_element", 0, 0, 15, False],
    ["j2735_2016.heading", "j2735_2016.speedConfidence_element", 0, 0, 7, False],
    ["j2735_2016.speed", "j2735_2016.speedConfidence_element", 0, 0, 7, False],
    ["j2735_2016.throttle", "j2735_2016.speedConfidence_element", 0, 0, 3, False],
    ["j2735_2016.radiusOfCurve", "j2735_2016.pathPrediction_element", 0, -32767, 32767, False],
    ["j2735_2016.confidence", "j2735_2016.pathPrediction_element", 0, 0, 200, False],
    ["j2735_2016.lights", "j2735_2016.PartII_Value_element", 3, 9, 00, False],
    ["j2735_2016.sspRights", "j2735_2016.vehicleAlerts_element", 0, 0, 31, False],
    ["j2735_2016.sirenUse", "j2735_2016.vehicleAlerts_element", 0, 0, 3, False],
    ["j2735_2016.lightsUse", "j2735_2016.vehicleAlerts_element", 0, 0, 7, False],
    ["j2735_2016.multi", "j2735_2016.vehicleAlerts_element", 0, 0, 3, False],
    ["j2735_2016.sspRights", "j2735_2016.events_element", 0, 0, 31, False],
    ["j2735_2016.event", "j2735_2016.events_element", 2, 16, 00, False],
    ["j2735_2016.responseType", "j2735_2016.vehicleAlerts_element", 0, 0, 6, False],
    ["j2735_2016.typeEvent", "j2735_2016.description_element", 0, 0, 65535, False],
    ["j2735_2016.priority", "j2735_2016.description_element", 1, 1, 00, False],
    ["j2735_2016.heading", "j2735_2016.description_element", 2, 16, 00, False],
    ["j2735_2016.extent", "j2735_2016.description_element", 0, 0, 15, False],
    ["j2735_2016.sspRights", "j2735_2016.trailers_element", 0, 0, 31, False],
    ["j2735_2016.pivotOffset", "j2735_2016.connection_element", 0, -1024, 1023, False],
    ["j2735_2016.pivotAngle", "j2735_2016.connection_element", 0, 0, 28800, False],
    ["j2735_2016.pivots", "j2735_2016.connection_element", 3, 00, 00, False],
    ["j2735_2016.classification", "j2735_2016.PartII_Value_element", 0, 0, 255, False],
    ["j2735_2016.keyType", "j2735_2016.classDetails_element", 0, 0, 255, False],
    ["j2735_2016.role", "j2735_2016.classDetails_element", 0, 0, 22, False],
    ["j2735_2016.iso3883", "j2735_2016.classDetails_element", 0, 0, 100, False],
    ["j2735_2016.hpmsType", "j2735_2016.classDetails_element", 0, 0, 15, False],
    ["j2735_2016.vehicleType", "j2735_2016.classDetails_element", 0, 0, 15, False],
    ["j2735_2016.responseEquip", "j2735_2016.classDetails_element", 0, 9985, 10113, False],
    ["j2735_2016.responderType", "j2735_2016.classDetails_element", 0, 9729, 9742, False],
    ["j2735_2016.fuelType", "j2735_2016.classDetails_element", 0, 0, 15, False],
    ["j2735_2016.height", "j2735_2016.vehicleData_element", 0, 0, 127, False],
    ["j2735_2016.front", "j2735_2016.bumpers_element", 0, 0, 127, False],
    ["j2735_2016.rear", "j2735_2016.bumpers_element", 0, 0, 127, False],
    ["j2735_2016.mass", "j2735_2016.vehicleData_element", 0, 0, 255, False],
    ["j2735_2016.trailerWeight", "j2735_2016.vehicleData_element", 0, 0, 64255, False],
    ["j2735_2016.front", "j2735_2016.bumpers_element", 0, 0, 127, False],
    ["j2735_2016.isRaining", "j2735_2016.weatherReport_element", 0, 1, 3, False],
    ["j2735_2016.rainRate", "j2735_2016.weatherReport_element", 0, 0, 65535, False],
    ["j2735_2016.precipSituation", "j2735_2016.weatherReport_element", 0, 1, 15, False],
    ["j2735_2016.solarRadiation", "j2735_2016.weatherReport_element", 0, 0, 65535, False],
    ["j2735_2016.friction", "j2735_2016.weatherReport_element", 0, 0, 101, False],
    ["j2735_2016.roadFriction", "j2735_2016.weatherReport_element", 0, 0, 50, False],
    ["j2735_2016.airTemp", "j2735_2016.weatherProbe_element", 0, 0, 191, False],
    ["j2735_2016.airPressure", "j2735_2016.weatherProbe_element", 0, 0, 255, False],
    ["j2735_2016.statusFront", "j2735_2016.rainRates_element", 0, 0, 6, False],
    ["j2735_2016.rateFront", "j2735_2016.rainRates_element", 0, 0, 127, False],
    ["j2735_2016.statusRear", "j2735_2016.rainRates_element", 0, 0, 6, False],
    ["j2735_2016.rateRear", "j2735_2016.rainRates_element", 0, 0, 127, False],
    ["j2735_2016.obDist", "j2735_2016.obstacle_element", 0, 0, 32767, False],
    ["j2735_2016.obDist", "j2735_2016.obstacle_element", 0, 0, 28800, False],
    ["j2735_2016.year", "j2735_2016.dateTime_element", 0, 0, 4095, False],
    ["j2735_2016.month", "j2735_2016.dateTime_element", 0, 0, 12, False],
    ["j2735_2016.day", "j2735_2016.dateTime_element", 0, 0, 31, False],
    ["j2735_2016.hour", "j2735_2016.dateTime_element", 0, 0, 31, False],
    ["j2735_2016.minute", "j2735_2016.dateTime_element", 0, 0, 60, False],
    ["j2735_2016.second", "j2735_2016.dateTime_element", 0, 0, 65535, False],
    ["j2735_2016.offset", "j2735_2016.dateTime_element", 0, -840, 840, False],
    ["j2735_2016.vertEvent", "j2735_2016.obstacle_element", 2, 5, 00, False],
    ]
saej2735_bsm_refdf = pd.DataFrame(saej2735_bsm_ref, columns = ["field", "parent", "eval method", "val1", "val2", "mandatory"])

saej2735_spat_ref = [
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 0, 0, 527040, False],
    ["j2735_2016.region", "j2735_2016.id_element", 0, 0, 6553, False],
    ["j2735_2016.id", "j2735_2016.id_element", 0, 0, 65535, True],
    ["j2735_2016.revision", "j2735_2016.IntersectionState_element", 0, 0, 127, True],
    ["j2735_2016.signalGroup", "j2735_2016.MovementState_element", 0, 0, 255, True],
    ["j2735_2016.eventState", "j2735_2016.MovementEvent_element", 0, 0, 9, True],
]
saej2735_spat_refdf = pd.DataFrame(saej2735_spat_ref, columns = ["field", "parent", "eval method", "val1", "val2", "mandatory"])

saej2735_rsa_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 0, 0, 127, True],
    ["j2735_2016.typeEvent", "j2735_2016.value_element", 0, 0, 65535, True],
]
saej2735_rsa_refdf = pd.DataFrame(saej2735_rsa_ref, columns = ["field", "parent", "eval method", "val1", "val2", "mandatory"])

saej2735_tim_ref = [
]
saej2735_tim_refdf = pd.DataFrame(saej2735_tim_ref, columns = ["field", "parent", "eval method", "val1", "val2", "mandatory"])

saej2735_map_ref = [
]
saej2735_map_refdf = pd.DataFrame(saej2735_map_ref, columns = ["field", "parent", "eval method", "val1", "val2", "mandatory"]) 

# GLOBAL ACCESSED DATAFRAMES/VARIABLES
assessdf = pd.DataFrame(columns=["field", "parent", "length", "value", "compliant", "occurrences"]) # DataFrame where each row is the results of analysis for a field.
faildf = pd.DataFrame(columns=["field", "parent", "length", "value", "compliant", "occurrences"])   # DataFrame where each row is the results of analysis for a FAILED field.

iop_result = True
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
    if(fieldlen == targetval):
        return True
    else:
        return False
    
# Eval Method 2: bit string
def bit_string(row, field):
    target_bitlen = row.get('val1').values[0]
    field_bitlen = int(re.findall(r"bit length (\d+)", field.attrib.get('showname'))[0])
    if (field_bitlen == target_bitlen):
        return True
    else:
        return False

#Eval Method 3: boolean
def boolean_check(row, fieldval):
    if((fieldval == 0) or (fieldval == 1)):
        return True
    else:
        return False

# ANALYZE PDML METHOD: Given a tree (parsed XML file), will iterate through every field of each relevant message to determine interoperability and compliance to standards.
def analyze(tree):
    global iop_result
    global iop_fail_desc
    for packet in tree.getroot():   # recursively move through packets/protocols
        for proto in packet:
            messageId = proto.find(".//field[@name='j2735_2016.messageId']")
            if (messageId != None):
                # DETERMINE MESSAGE TYPE
                codenum = int(messageId.attrib.get('show'))
                match codenum:
                    case 20:    # BSM
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_bsm_refdf
                    case 27:    # RSA
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_rsa_refdf
                    case 19:    # SPaT
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_spat_refdf
                    case 31:    # TIM
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_tim_refdf
                    case 18:    # MAP
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_map_refdf
                    case _:
                        iop_result = False
                        iop_fail_desc = iop_fail_desc + "Invalid messageId: " + messageId + "\n"
                print("-------------------------------------------")

                # SET MESSAGE REFERENCE TABLE VARIABLES FOR SEQUENCE CHECKING
                if (not refdf.empty):
                    mand_index = 0 
                    while ((refdf.iloc[mand_index].get('mandatory') != True)):
                        mand_index += 1

                    lastmand_index = len(refdf.index) - 1
                    while (refdf.iloc[lastmand_index].get('mandatory') != True):
                        lastmand_index -= 1
                
                # IoP ANALYSIS
                    for field in proto.iter():  # iteratively move through fields
                        parentname = str(field.getparent().attrib.get('name'))
                        fieldname = str(field.attrib.get('name'))
                        fieldlen = int(field.attrib.get('size'), 10)
                        
                        if (fieldname == "per.optional_field_bit"): # optional field handler
                            if ("True" in str(field.attrib.get('showname'))):
                                fieldname = "j2735_2016." + re.findall(r'\(([^ ]+?) ', field.attrib.get('showname'))[0]
                            else:
                                continue

                        row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)]    # get row based on field name and parent name

                        if (len(row) == 1): # (there should only be 1 entry per unique pair of field name and parent name)
                            # SEQUENCE CHECKING
                            fieldmand_ref = row.get('mandatory').values[0]
                            lastmand_reached = False
                            if (fieldmand_ref): # if field is mandatory
                                if (mand_index == lastmand_index):  # if reached the end of the mandatory fields in table
                                        lastmand_reached = True
                                if ((fieldname != refdf.iloc[mand_index].get('field')) and not lastmand_reached):   # if current (mandatory) field does not match the intended mandatory field in sequence
                                    iop_result = False
                                    iop_fail_desc = iop_fail_desc + "Sequence incorrect: was " + fieldname + " but should be " + refdf.iloc[mand_index].get('field') + "\n"
                                else:
                                    if (mand_index < lastmand_index):   # if haven't reached the end of the mandatory fields in table
                                        mand_index += 1
                                        while ((refdf.iloc[mand_index].get('mandatory') != True) and (mand_index < lastmand_index)):    # go to next mandatory field in table
                                            mand_index += 1

                            # CONVERT STRING (FROM DATAFILE) TO INT VALUES    
                            try: 
                                fieldval = int(field.attrib.get('show'), 10)
                            except ValueError:
                                fieldval = int(field.attrib.get('value'), 16) 
                            print("Tag:", fieldname)
                            print("Length:", fieldlen)
                            print("Value:", fieldval)

                            # QUANTITATIVE EVALUATION
                            eval_method = row.get('eval method').values[0]
                            match eval_method:  # determine how the field should be evaluated based on standard
                                case 0:
                                    print("Method: Compare Min-Max")
                                    eval_result = compare_min_max(row, fieldval)
                                case 1:
                                    print("Method: Octet Count")
                                    eval_result = octet_count(row, fieldlen)
                                case 2:
                                    print("Method: Bit string")
                                    eval_result = bit_string(row, field)
                                case 3:
                                    print("Method: Boolean")
                                    eval_result = boolean_check(row, fieldval)
                                case _:
                                    iop_result = False
                                    iop_fail_desc = iop_fail_desc + "Invalid evaluation method for " + fieldname + "\n"
                                    continue
                                
                            # SAVE RESULTS
                            if (not eval_result):   # field failed evaluation
                                iop_result = False
                                iop_fail_desc = iop_fail_desc + "Value out of range: " + fieldname + "\n"
                                row_fail = faildf.loc[(faildf['field'] == fieldname) & (faildf['parent'] == parentname)]
                                if (len(row_fail) != 0):
                                    faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, False, row_fail.tail(1).get('occurrences').values[0] + 1]
                                else:
                                    faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, False, 1]
                            
                            row_assess = assessdf.loc[(assessdf['field'] == fieldname) & (assessdf['parent'] == parentname) & (assessdf['compliant'] == eval_result)]
                            if (len(row_assess) != 0):
                                assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, eval_result, row_assess.tail(1).get('occurrences').values[0] + 1]
                            else:
                                assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, eval_result, 1]
                            
                            print("Field Compliant:", assessdf.tail(1).get('compliant').values[0])
                            print("Interoperable:", iop_result)
                            print()
    # PRINT RESULTS
    print("--------------------------------------------------------------------------------------\n")
    if (iop_result):
        print("Interoperability: PASS")
    else:
        print("Interoperability: FAIL")
        print("\n" + iop_fail_desc)
        print(faildf)
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