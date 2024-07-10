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
saej2735_bsm_ref = [ # col[0] = field name, col[1] = parent name, col[2]] = eval method, col[3] = ref value 1, col[4] = ref value 2, col[5] = mandatory?
    ["j2735_2016.msgCnt", "j2735_2016.coreData_element", 0, 0, 127],
    ["j2735_2016.id", "j2735_2016.coreData_element", 1, 4, 00],
    ["j2735_2016.secMark", "j2735_2016.coreData_element", 0, 0, 60999],
    ["j2735_2016.lat", "j2735_2016.coreData_element", 0, -900000000, 900000001],
    ["j2735_2016.long", "j2735_2016.coreData_element", 0, -1799999999, 1800000001],
    ["j2735_2016.elev", "j2735_2016.coreData_element", 0, -4096, 61439],
    ["j2735_2016.semiMajor", "j2735_2016.accuracy_element", 0, 0, 255],
    ["j2735_2016.semiMinor", "j2735_2016.accuracy_element", 0, 0,255],
    ["j2735_2016.transmission", "j2735_2016.coreData_element", 0, 0, 7],
    ["j2735_2016.speed", "j2735_2016.coreData_element", 0, 0, 8191],
    ["j2735_2016.heading", "j2735_2016.coreData_element", 0, 0, 28800],
    ["j2735_2016.angle", "j2735_2016.coreData_element", 0, -126, 127],
    ["j2735_2016.orientation", "j2735_2016.accuracy_element", 0, 0, 65535],
    ["j2735_2016.long", "j2735_2016.accelSet_element", 0, -2000, 2001],
    ["j2735_2016.lat", "j2735_2016.accelSet_element", 0, -2000, 2001],
    ["j2735_2016.vert", "j2735_2016.accelSet_element", 0, -127, 127],
    ["j2735_2016.yaw", "j2735_2016.accelSet_element", 0, -32767, 32767],
    ["j2735_2016.wheelBrakes", "j2735_2016.brakes_element", 2, 5, 00],
    ["j2735_2016.traction", "j2735_2016.brakes_element", 0, 0, 3],
    ["j2735_2016.abs", "j2735_2016.brakes_element", 0, 0, 3],
    ["j2735_2016.scs", "j2735_2016.brakes_element", 0, 0, 3],
    ["j2735_2016.brakeBoost", "j2735_2016.brakes_element", 0, 0, 2],
    ["j2735_2016.auxBrakes", "j2735_2016.brakes_element", 0, 0, 2],
    ["j2735_2016.width", "j2735_2016.size_element", 0, 0, 1023],
    ["j2735_2016.length", "j2735_2016.size_element", 0, 0, 4095],
    ["j2735_2016.partII.Id", "j2735_2016.PartIIcontent_element", 0, 0, 63],
    ["j2735_2016.partII.events", "j2735_2016.PartII_Value_element", 2, 13, 00],
    ["j2735_2016.partII.year", "j2735_2016.utcTime_element", 0, 0, 4095],
    ["j2735_2016.partII.month", "j2735_2016.utcTime_element", 0, 0, 12],
    ["j2735_2016.partII.day", "j2735_2016.utcTime_element", 0, 0, 31],
    ["j2735_2016.partII.hour", "j2735_2016.utcTime_element", 0, 0, 31],
    ["j2735_2016.partII.minute", "j2735_2016.utcTime_element", 0, 0, 60],
    ["j2735_2016.partII.second", "j2735_2016.utcTime_element", 0, 0, 65535],
    ["j2735_2016.long", "j2735_2016.initialPosition_element", 0, -1799999999, 1800000001],
    ["j2735_2016.lat", "j2735_2016.initialPosition_element", 0, -900000000, 900000001],
    ["j2735_2016.elevation", "j2735_2016.initialPosition_element", 0, -4096, 61439],
    ["j2735_2016.heading", "j2735_2016.initialPosition_element", 0, 0, 28800],
]
saej2735_bsm_refdf = pd.DataFrame(saej2735_bsm_ref, columns = ["field", "parent", "eval method", "val1", "val2"])

saej2735_spat_ref = [
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 0, 0, 527040],
    ["j2735_2016.region", "j2735_2016.id_element", 0, 0, 65535],
    ["j2735_2016.id", "j2735_2016.id_element", 0, 0, 65535],
    ["j2735_2016.revision", "j2735_2016.IntersectionState_element", 0, 0, 127],
    ["j2735_2016.signalGroup", "j2735_2016.MovementState_element", 0, 0, 255],
    ["j2735_2016.eventState", "j2735_2016.MovementEvent_element", 0, 0, 9],
]
saej2735_spat_refdf = pd.DataFrame(saej2735_spat_ref, columns = ["field", "parent", "eval method", "val1", "val2"])

saej2735_rsa_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 0, 0, 127],
    ["j2735_2016.typeEvent", "j2735_2016.value_element", 0, 0, 65535],
]
saej2735_rsa_refdf = pd.DataFrame(saej2735_rsa_ref, columns = ["field", "parent", "eval method", "val1", "val2"])

saej2735_tim_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 0, 0, 127],
    ["j2735_2016.sspTimRights", "j2735_2016.dataFrames", 0, 0, 31],
    ["j2735_2016.lat", "j2735_2016.position_element", 0, -900000000,  900000001],
    ["j2735_2016.long", "j2735_2016.position_element", 0, -1799999999, 1800000001],
    ["j2735_2016.startTime", "j2735_2016.value_element", 0, 0, 527040],
    ["j2735_2016.durationTime", "j2735_2016.value_element", 0, 0, 32000],
    ["j2735_2016.priority", "j2735_2016.value_element", 0, 0, 7],
    ["j2735_2016.sspLocationRights", "j2735_2016.value_element", 0, 0, 31],
    ["j2735_2016.x", "j2735_2016.node_XY1_element", 0, -512, 511],
    ["j2735_2016.y", "j2735_2016.node_XY1_element", 0, -512, 511],
    ["j2735_2016.x", "j2735_2016.node_XY2_element", 0, -1024, 1023],
    ["j2735_2016.y", "j2735_2016.node_XY2_element", 0, -1024, 1023],
    ["j2735_2016.x", "j2735_2016.node_XY3_element", 0, -2048, 2047],
    ["j2735_2016.y", "j2735_2016.node_XY3_element", 0, -2048, 2047],
    ["j2735_2016.x", "j2735_2016.node_XY4_element", 0, -4096, 4095],
    ["j2735_2016.y", "j2735_2016.node_XY4_element", 0, -4096, 4095],
    ["j2735_2016.x", "j2735_2016.node_XY5_element", 0, -8192, 8191],
    ["j2735_2016.y", "j2735_2016.node_XY5_element", 0, -8192, 8191],
    ["j2735_2016.x", "j2735_2016.node_XY6_element", 0, -32768, 32767],
    ["j2735_2016.y", "j2735_2016.node_XY6_element", 0, -32768, 32767],
    ["j2735_2016.lon", "j2735_2016.node_LatLon_element", 0, -1799999999, 1800000001],
    ["j2735_2016.lat", "j2735_2016.node_LatLon_element", 0, -900000000, 900000001],
    ["j2735_2016.sspMsgRights", "j2735_2016.value_element", 0, 0, 31],
    ["j2735_2016.y", "j2735_2016.value_element", 0, 0, 31],
]
saej2735_tim_refdf = pd.DataFrame(saej2735_tim_ref, columns = ["field", "parent", "eval method", "val1", "val2"])

saej2735_map_ref = [
    ["j2735_2016.msgIssueRevision", "j2735_2016.value_element", 0, 0, 127],
]
saej2735_map_refdf = pd.DataFrame(saej2735_map_ref, columns = ["field", "parent", "eval method", "val1", "val2"]) 

# DataFrame where each row is the results of analysis for a field.
assessdf = pd.DataFrame(columns=["field", "parent", "length", "value", "compliant", "occurrences"])

# DataFrame where each row is the results of analysis for a FAILED field.
faildf = pd.DataFrame(columns=["field", "parent", "length", "value", "compliant", "occurrences"])

iop_result = True

# Eval method 0
def compare_min_max(row, fieldval):
    minval = row.get('val1').values[0]
    maxval = row.get('val2').values[0]
    if((minval <= fieldval) and (fieldval <= maxval)):
        return True
    else:
        return False

# Eval method 1
def octet_count(row, fieldlen):
    targetval = row.get('val1').values[0]
    if(fieldlen == targetval):
        return True
    else:
        return False
    
# Eval method 2
def bit_string(row, field):
    target_bitlen = row.get('val1').values[0]
    field_bitlen = int(re.findall(r"bit length (\d+)", field.attrib.get('showname'))[0])
    if (field_bitlen == target_bitlen):
        return True
    else:
        return False

# Given a tree (parsed XML file), will iterate through every field of each relevant message to determine interoperability and compliance to standards.
def analyze(tree):
    global iop_result
    for packet in tree.getroot(): # recursively move through packets/protocols
        for proto in packet:
            messageId = proto.find(".//field[@name='j2735_2016.messageId']")
            if (messageId != None):
                codenum = int(messageId.attrib.get('show'))
                match codenum: # determine message type:
                    case 20: # BSM
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_bsm_refdf
                    case 27: # RSA
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_rsa_refdf
                    case 19: # SPaT
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_spat_refdf
                    case 31: # TIM
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_tim_refdf
                    case 18: # MAP
                        print(messageId.attrib.get('showname'))
                        refdf = saej2735_map_refdf
                    case _:
                        # raise Exception("Invalid messageId")
                        continue
                print("-------------------------------------------")

                for field in proto.iter(): # iteratively move through fields
                    parentname = str(field.getparent().attrib.get('name'))
                    fieldname = str(field.attrib.get('name'))

                    row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)] # get row based on field name and parent name                       

                    fieldlen = int(field.attrib.get('size'), 10)
                    
                    if (fieldname == "per.optional_field_bit"): # optional field handler
                        if ("True" in str(field.attrib.get('showname'))):
                            fieldname = "j2735_2016." + re.findall(r'\(([^ ]+?) ', field.attrib.get('showname'))[0]
                        else:
                            continue
                    
                    if (len(row) == 1): # (there should only be 1 entry per unique pair of field name and parent name)
                        try: 
                            fieldval = int(field.attrib.get('show'), 10)
                        except ValueError:
                            fieldval = int(field.attrib.get('value'), 16) 
                        print("Tag:", fieldname)
                        print("Length:", fieldlen)
                        print("Value:", fieldval)

                        eval_method = row.get('eval method').values[0]
                        match eval_method: # determine how the field should be evaluated based on standard
                            case 0:
                                print("Method: Compare Min-Max")
                                eval_result = compare_min_max(row, fieldval)
                            case 1:
                                print("Method: Octet Count")
                                eval_result = octet_count(row, fieldlen)
                            case 2:
                                print("Method: Bit string")
                                eval_result = bit_string(row, field)
                            # case 3:
                            # case 4:
                            # case _: 
                        if (eval_result): # field passed evaluation
                            row_pass = assessdf.loc[(assessdf['field'] == fieldname) & (assessdf['parent'] == parentname)]
                            if (len(row_pass) != 0):
                                assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, True, row_pass.tail(1).get('occurrences').values[0] + 1]
                            else:    
                                assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, True, 1]
                        else: # field failed evaluation
                            iop_result = False
                            row_fail = faildf.loc[(faildf['field'] == fieldname) & (faildf['parent'] == parentname)]
                            if (len(row_fail) != 0):
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, False, row_fail.tail(1).get('occurrences').values[0] + 1]
                            else:
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, fieldlen, fieldval, False, 1]
                        
                        print("Field Compliant:", assessdf.iat[len(assessdf)-1, 4])
                        print("Interoperable:", iop_result)
                        print()
    
    print("--------------------------------------------------------------------------------------")
    if (iop_result):
        print("Interoperability: PASS")
    else:
        print("Interoperability: FAIL")
        print(faildf)
    print("--------------------------------------------------------------------------------------")
    
    print(assessdf)

def main():
   try:
       inFile = sys.argv[1]
   except IndexError:
       print("Error: Specify a pdml file.")
       sys.exit(1)
   print("Parsing...")
   tree = etree.parse(inFile)
   print("Analyzing...")
   analyze(tree)

if __name__ == "__main__":
    main()