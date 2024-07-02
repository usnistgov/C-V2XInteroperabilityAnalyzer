import sys
import pandas as pd
from lxml import etree

saej2735_bsm_ref = [ # col = field name, row[0] = parent name, row[1] = min value, row[2] = max value
    ["j2735_2016.msgCnt", "j2735_2016.coreData_element", 0, 127],
    ["j2735_2016.secMark", "j2735_2016.coreData_element", 0, 60999],
    ["j2735_2016.lat", "j2735_2016.coreData_element", -900000000, 900000001],
    ["j2735_2016.long", "j2735_2016.coreData_element", -1799999999, 1800000001],
    ["j2735_2016.elev", "j2735_2016.coreData_element", -4096, 61439],
    ["j2735_2016.transmission", "j2735_2016.coreData_element", 0, 7],
    ["j2735_2016.semiMajor", "j2735_2016.speed", 0, 255],
    ["j2735_2016.semiMinor", "j2735_2016.speed", 0,255],
    ["j2735_2016.orientation", "j2735_2016.speed", 0, 65535],
    ["j2735_2016.angle", "j2735_2016.coreData_element", -126, 127],
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
    ["j2735_2016.region", None, 0, 65535],
    ["j2735_2016.revision", None, 0, 127],
    ["j2735_2016.signalGroup", None, 0, 255],
    ["j2735_2016.eventState", None, 0, 9]
]
saej2735_spat_refdf = pd.DataFrame(saej2735_spat_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_rsa_ref = []
saej2735_rsa_refdf = pd.DataFrame(saej2735_rsa_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_tim_ref = []
saej2735_tim_refdf = pd.DataFrame(saej2735_tim_ref, columns = ["field", "parent", "minval", "maxval"])

saej2735_map_ref = []
saej2735_map_refdf = pd.DataFrame(saej2735_map_ref, columns = ["field", "parent", "minval", "maxval"]) 

# DataFrame where each row is the results of analysis for a field.
assessdf = pd.DataFrame(columns=["field", "parent", "val", "result"])

# DataFrame where each row is the results of analysis for a FAILED field.
faildf = pd.DataFrame(columns=["field", "parent", "val", "result"])

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
                    continue

                for field in proto.iter():
                    fieldname = field.attrib.get('name')
                    parentname = field.getparent().attrib.get('name')
                    row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)]
                    if (len(row) == 1):
                        # print(fieldname,",", parentname)
                        minval = row.get('minval').values[0]
                        maxval = row.get('maxval').values[0]
                        # print("min:", minval, "\t", "max:", maxval)
                        fieldval = int(field.attrib.get('show'))
                        # print("val:", fieldval)
                        if((minval <= fieldval) and (fieldval <= maxval)):
                            # print("GOOD")
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldval, "Within range"]
                        else:
                            # print("BAD")
                            iop_result = False
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, fieldval, "Out of range"]
                            faildf.loc[len(assessdf.index)] = [fieldname, parentname, fieldval, "Out of range"]
                        print(assessdf.tail(1).to_string(header = False))

            else:
                continue
    
    print("-------------------------------------------")
    if (iop_result):
        print("Interoperability: PASS")
    else:
        print("Interoperability: FAIL")
        print(faildf)
    print("-------------------------------------------")
    

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