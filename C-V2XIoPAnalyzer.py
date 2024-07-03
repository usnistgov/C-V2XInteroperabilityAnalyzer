import sys
from lxml import etree
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

saej2735_bsm_ref = [ # col = field name, row[0] = parent name, row[1] = min value, row[2] = max value
    ["j2735_2016.msgCnt", "j2735_2016.coreData_element", 0, 127],
    ["j2735_2016.secMark", "j2735_2016.coreData_element", 0, 60999],
    ["j2735_2016.lat", "j2735_2016.coreData_element", -900000000, 900000001],
    ["j2735_2016.long", "j2735_2016.coreData_element", -1799999999, 1800000001],
    ["j2735_2016.elev", "j2735_2016.coreData_element", -4096, 61439],
    ["j2735_2016.semiMajor", "j2735_2016.accuracy_element", 0, 255],
    ["j2735_2016.semiMinor", "j2735_2016.accuracy_element", 0,255],
    ["j2735_2016.transmission", "j2735_2016.coreData_element", 0, 7],
    ["j2735_2016.speed", "j2735_2016.coreData_element", 0, 8191],
    ["j2735_2016.heading", "j2735_2016.coreData_element", 0, 28800],
    ["j2735_2016.angle", "j2735_2016.coreData_element", -126, 127],
    ["j2735_2016.orientation", "j2735_2016.accuracy_element", 0, 65535],
    ["j2735_2016.long", "j2735_2016.accelSet_element", -2000, 2001],
    ["j2735_2016.lat", "j2735_2016.accelSet_element", -2000, 2001],
    ["j2735_2016.vert", "j2735_2016.accelSet_element", -127, 127],
    ["j2735_2016.yaw", "j2735_2016.accelSet_element", -32767, 32767],
    ["j2735_2016.brakeBoost", "j2735_2016.brakes_element", 0, 2],
    ["j2735_2016.width", "j2735_2016.size_element", 0, 1023],
    ["j2735_2016.length", "j2735_2016.size_element", 0, 4095],
]
saej2735_bsm_refdf = pd.DataFrame(saej2735_bsm_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_spat_ref = [
    ["j2735_2016.timeStamp", "j2735_2016.value_element", 0, 527040],
    ["j2735_2016.region", "j2735_2016.id_element", 0, 65535],
    ["j2735_2016.id", "j2735_2016.id_element", 0, 65535],
    ["j2735_2016.revision", "j2735_2016.IntersectionState_element", 0, 127],
    ["j2735_2016.signalGroup", "j2735_2016.MovementState_element", 0, 255],
    ["j2735_2016.eventState", "j2735_2016.MovementEvent_element", 0, 9],
]
saej2735_spat_refdf = pd.DataFrame(saej2735_spat_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_rsa_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 0, 127],
    ["j2735_2016.typeEvent", "j2735_2016.value_element", 0, 65535],
]
saej2735_rsa_refdf = pd.DataFrame(saej2735_rsa_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_tim_ref = [
    ["j2735_2016.msgCnt", "j2735_2016.value_element", 0, 127],
    ["j2735_2016.sspTimRights", "j2735_2016.dataFrames", 0, 31],
    ["j2735_2016.lat", "j2735_2016.position_element", -900000000,  900000001],
    ["j2735_2016.long", "j2735_2016.position_element", -1799999999, 1800000001],
    ["j2735_2016.startTime", "j2735_2016.value_element", 0, 527040],
    ["j2735_2016.durationTime", "j2735_2016.value_element", 0, 32000],
    ["j2735_2016.priority", "j2735_2016.value_element", 0, 7],
    ["j2735_2016.sspLocationRights", "j2735_2016.value_element", 0, 31],
    ["j2735_2016.x", "j2735_2016.node_XY1_element", -512, 511],
    ["j2735_2016.y", "j2735_2016.node_XY1_element", -512, 511],
    ["j2735_2016.x", "j2735_2016.node_XY2_element", -1024, 1023],
    ["j2735_2016.y", "j2735_2016.node_XY2_element", -1024, 1023],
    ["j2735_2016.x", "j2735_2016.node_XY3_element", -2048, 2047],
    ["j2735_2016.y", "j2735_2016.node_XY3_element", -2048, 2047],
    ["j2735_2016.x", "j2735_2016.node_XY4_element", -4096, 4095],
    ["j2735_2016.y", "j2735_2016.node_XY4_element", -4096, 4095],
    ["j2735_2016.x", "j2735_2016.node_XY5_element", -8192, 8191],
    ["j2735_2016.y", "j2735_2016.node_XY5_element", -8192, 8191],
    ["j2735_2016.x", "j2735_2016.node_XY6_element", -32768, 32767],
    ["j2735_2016.y", "j2735_2016.node_XY6_element", -32768, 32767],
    ["j2735_2016.lon", "j2735_2016.node_LatLon_element", -1799999999, 1800000001],
    ["j2735_2016.lat", "j2735_2016.node_LatLon_element", -900000000, 900000001],
    ["j2735_2016.sspMsgRights", "j2735_2016.value_element", 0, 31],
    ["j2735_2016.y", "j2735_2016.value_element", 0, 31],
]
saej2735_tim_refdf = pd.DataFrame(saej2735_tim_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_map_ref = [
    ["j2735_2016.msgIssueRevision", "j2735_2016.value_element", 0, 127],
]
saej2735_map_refdf = pd.DataFrame(saej2735_map_ref, columns = ["field", "parent", "minval", "maxval"]) 

# DataFrame where each row is the results of analysis for a field.
assessdf = pd.DataFrame(columns=["field name", "parent name", "length", "value", "result"])

# DataFrame where each row is the results of analysis for a FAILED field.
faildf = pd.DataFrame(columns=["field name", "parent name", "length", "value", "result"])

iop_result = True

def analyze(tree):
    global iop_result
    for packet in tree.getroot():
        for proto in packet:
            messageId = proto.find(".//field[@name='j2735_2016.messageId']")
            if (messageId != None):
                codenum = messageId.attrib.get('show')
                if (codenum == "20"): # BSM
                    print(messageId.attrib.get('showname'))
                    refdf = saej2735_bsm_refdf
                elif (codenum == "27"): # RSA
                    print(messageId.attrib.get('showname'))
                    refdf = saej2735_rsa_refdf
                elif (codenum == "19"): # SPaT
                    print(messageId.attrib.get('showname'))
                    refdf = saej2735_spat_refdf
                elif (codenum == "31"): # TIM
                    print(messageId.attrib.get('showname'))
                    refdf = saej2735_tim_refdf
                elif (codenum == "18"): # MAP
                    print(messageId.attrib.get('showname'))
                    refdf = saej2735_map_refdf
                else:
                    # raise Exception("Invalid messageId")
                    continue
                print("-------------------------------------------")

                for field in proto.iter():
                    fieldname = field.attrib.get('name')
                    parentname = field.getparent().attrib.get('name')
                    fieldlen = len(str(field.attrib.get('value')))
                    row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)]
                    if (len(row) == 1):
                        minval = row.get('minval').values[0]
                        maxval = row.get('maxval').values[0]
                        try: 
                            fieldval = int(field.attrib.get('show'), 10)
                        except ValueError:
                            fieldval = int(field.attrib.get('show'), 16)

                        if((minval <= fieldval) and (fieldval <= maxval)):
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, "Within range"]
                        else:
                            iop_result = False
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, "Out of range"]
                            faildf.loc[len(assessdf.index)] = [fieldname, parentname, fieldlen, fieldval, "Out of range"]
                        # print(assessdf.tail(1).to_string(header = False))
                        print("Tag:", fieldname)
                        print("Length:", fieldlen)
                        print("Value:", fieldval)
                        print()

            else:
                continue
    
    print("--------------------------------------------------------------------------------------")
    if (iop_result):
        print("Interoperability: PASS")
    else:
        print("Interoperability: FAIL")
        print(faildf)
    print("--------------------------------------------------------------------------------------")
    

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