import sys
from lxml import etree
import re
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)

from j2735_ref_tables import saej2735_bsm_refdf, saej2735_spat_refdf, saej2735_rsa_refdf, saej2735_tim_refdf, saej2735_rsa_refdf, saej2735_map_refdf
from ieee16093_ref_tables import ieee16093_wsmp_refdf
from ieee16092_ref_tables import ieee16092_spdu_refdf

# GLOBAL ACCESSED DATAFRAMES/VARIABLES
assessdf = pd.DataFrame(columns=["field", "parent", "message", "length", "value", "compliant", "occurrences"]) # DataFrame where each row is the_files of analysis for a field.
faildf = pd.DataFrame(columns=["field", "parent", "message", "length", "value", "occurrences", "fail description"])   # DataFrame where each row is the_files of analysis for a FAILED field.
# skipdf = pd.DataFrame(columns=["field", "parent", "message"]) # DataFrame where each row is a skipped line (not a checked field).
iop_file = True
iop_file_fail_desc = ""

# ------- DEFINE QUANTITATIVE EVALUATION METHODS -------
# Eval Method 0: compare with min, max
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
def bit_string(row, field, iop_fail_desc):
    target_bitlen = row.get('val1').values[0]
    try:
        field_bitlen = int(re.findall("bit length (\d+)", field.attrib.get('showname'))[0])
    except IndexError:
        iop_fail_desc = iop_fail_desc + "Incorrect format for bit string. "
        return False
    if (field_bitlen <= target_bitlen):
        return True
    else:
        return False

# Eval Method 3: boolean
def boolean_check(fieldval):
    if ((fieldval == 0) or (fieldval == 1)):
        return True
    else:
        return False

# Eval Method 4: hashalg list
def hashalg_list(field):
    hashname = re.findall("HashAlgorithm: (\w+)", field.attrib.get('showname'))[0]
    if ((hashname == "sha256") or (hashname == "sha384") or (hashname == "sm3")):
        return True
    else:
        return False

# Eval Method 5: IA5 string
def ia5str(row, fieldval, fieldlen):
    minlength = row.get('val1').values[0]
    maxlength = row.get('val2').values[0]
    if (not (minlength <= fieldlen) and not (fieldlen >= maxlength)):
        return False
    try: 
        fieldval.encode(encoding = 'ascii')
    except UnicodeEncodeError:
        return False
    return True

# Eval Method 6: UTF8 string
def utf8str(row, fieldval, fieldlen):
    minlength = row.get('val1').values[0]
    maxlength = row.get('val2').values[0]
    if (not (minlength <= fieldlen) and not (fieldlen >= maxlength)):
        return False
    try: 
        fieldval.encode(encoding = 'UTF-8')
    except UnicodeEncodeError:
        return False
    return True

# Eval Method 7: signer
def signer(field):
    signername = re.findall("signer: (\w+)", field.attrib.get('showname'))[0]
    if ((signername == "digest") or (signername == "certificate")):
        return True
    else:
        return False

# ------- ANALYZE PDML METHOD: Given a tree (parsed XML file), will iterate through every field of each relevant message to determine interoperability and compliance to standards. -------
def analyze(tree):
    global iop_file
    global iop_file_fail_desc
    for packet in tree.getroot():   # recursively move through packets/protocols
        iop_packet = True
        for proto in packet:
            iop_message = True
            refdf = None
            messagename = None
            # DETERMINE PROTOCOL AND MESSAGE TYPE, SET CORRESPONDING REFERENCE DATAFRAME
            if ("j2735" in proto.attrib.get('name')):   # SAE J2735
                messageId = proto.find(".//field[@name='j2735_2016.messageId']")
                if (messageId != None):
                    messagename = "SAE J2735: " + re.findall("messageId: (.+)", messageId.attrib.get('showname'))[0]
                    codenum = int(messageId.attrib.get('show'))
                    match codenum:
                        case 20:    # BSM
                            refdf = saej2735_bsm_refdf
                        case 27:    # RSA 
                            refdf = saej2735_rsa_refdf
                        case 19:    # SPaT
                            refdf = saej2735_spat_refdf
                        case 31:    # TIM 
                            refdf = saej2735_tim_refdf
                        case 18:    # MAP
                            refdf = saej2735_map_refdf
                        case _:
                            iop_file = False
                            iop_file_fail_desc = iop_file_fail_desc + "Invalid messageId: " + messageId + "\n"
            elif ("16093" in proto.attrib.get('name')): # IEEE 1609.3
                messagename = "IEEE 1609.3: WAVE Short Message Protocol"
                refdf = ieee16093_wsmp_refdf 
            elif ("16092" in proto.attrib.get('name')): # IEEE 1609.2
                messagename = "IEEE 1609.2: WAVE Security Signed Data"
                refdf = ieee16092_spdu_refdf
            else:
                continue

            if (messagename is not None):
                print(messagename) 
                print("--------------------------------------------")          

            # SET MESSAGE REFERENCE TABLE VARIABLES FOR SEQUENCE CHECKING
            if ((refdf is not None) and (not refdf.empty)):
                mand_index = 0 
                while ((refdf.iloc[mand_index].get('mandatory') != True)):
                    mand_index += 1

                lastmand_index = len(refdf.index) - 1
                while (refdf.iloc[lastmand_index].get('mandatory') != True):
                    lastmand_index -= 1
            
                # ------- IoP ANALYSIS -------
                for field in proto.iter():  # iteratively move through fields
                    iop_tag = True
                    iop_length = True
                    iop_value = True
                    iop_sequence = True
                    iop_field = True
                    iop_fail_desc = ""

                    fieldname = str(field.attrib.get('name'))
                    parentname = str(field.getparent().attrib.get('name'))
                    
                    if (fieldname == "per.optional_field_bit"): # optional field handler
                        if ("True" in str(field.attrib.get('showname'))):
                            fieldname = "j2735_2016." + re.findall('\(([^ ]+?) ', field.attrib.get('showname'))[0]
                        else:
                            continue

                    row = refdf.loc[(refdf['field'] == fieldname) & (refdf['parent'] == parentname)]    # get row based on field name and parent name

                    if ((len(row.index) != 1)): # (there should only be 1 entry per unique pair of field name and parent name)
                        if ((len(row.index) != 0) and not row.empty):
                            iop_tag = False
                            iop_fail_desc = iop_fail_desc + "Invalid/Repeated tag. "
                        # if (row.empty):
                        #     skipdf.loc[len(skipdf.index)] = [fieldname, parentname, messagename]
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
                        
                        # LENGTH EVALUATION
                        fieldlen = int(field.attrib.get('size'), 10)
                        if ((fieldlen < 1) or (fieldlen > row.get('length').values[0])):
                            iop_length = False
                            iop_fail_desc = iop_fail_desc + "Incorrect length: " + str(fieldlen) + " should be " + str(row.get('length').values[0]) + ". "
                        
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
                                if (not (re.findall("bit length", str(field.attrib.get('showname'))))):
                                    continue
                                else:
                                    iop_value = bit_string(row, field, iop_fail_desc)
                            case 3:
                                iop_value = boolean_check(fieldval)
                            case 4: 
                                fieldval = re.findall("HashAlgorithm: (\w+)", str(field.attrib.get('showname')))[0]
                                iop_value = hashalg_list(field)
                            case 5: 
                                fieldval = re.findall(": (.+)", str(field.attrib.get('showname')))[0]
                                iop_value = ia5str(row, fieldval, fieldlen)
                            case 6:
                                fieldval = re.findall(": (.+)", str(field.attrib.get('showname')))[0]
                                iop_value = utf8str(row, fieldval, fieldlen)
                            case 7: 
                                fieldval = re.findall("signer: (\w+)", str(field.attrib.get('showname')))[0]
                                iop_value = signer(field)
                            case _:
                                iop_value = False
                                iop_fail_desc = iop_fail_desc + "Invalid evaluation method. "
                                continue 
                        if (not iop_value):   # field failed evaluation
                            iop_fail_desc = iop_fail_desc + "Value out of range/invalid. " 

                        # SAVE FIELD RESULTS
                        if (not iop_tag or not iop_length or not iop_value or not iop_sequence):    # at least one T/L/V metric failed
                            iop_field = False
                            iop_message = False
                            iop_packet = False
                            iop_file = False
                            row_fail = faildf.loc[(faildf['field'] == fieldname) & (faildf['parent'] == parentname) & (faildf['message'] == messagename)]
                            if (len(row_fail) != 0):
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, messagename, fieldlen, fieldval, row_fail.tail(1).get('occurrences').values[0] + 1, iop_fail_desc.rstrip()]
                            else:
                                faildf.loc[len(faildf.index)] = [fieldname, parentname, messagename, fieldlen, fieldval, 1, iop_fail_desc.rstrip()]

                        row_assess = assessdf.loc[(assessdf['field'] == fieldname) & (assessdf['parent'] == parentname) & (assessdf['message'] == messagename) & (assessdf['compliant'] == iop_field)]
                        if (len(row_assess) != 0):
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, messagename, fieldlen, fieldval, iop_field, row_assess.tail(1).get('occurrences').values[0] + 1]
                        else:
                            assessdf.loc[len(assessdf.index)] = [fieldname, parentname, messagename, fieldlen, fieldval, iop_field, 1]
                            
                        # ------- PRINT FIELD RESULTS -------
                        print("Tag:", fieldname, ">", iop_tag)
                        print("Length:", fieldlen, ">", iop_length)
                        print("Value:", fieldval, ">", iop_value)
                        print("Field Compliant:", iop_field)    
                        print("Message Interoperable:", iop_message, "\n")
                        
            print("***Packet Interoperable:", iop_packet, "\n")

        if (iop_file_fail_desc != ""):
            print(iop_file_fail_desc)

    # PRINT OVERALL RESULTS
    print("-------------------------------------------------------------------------------------------------------------------\n")
    if (iop_file):
        print("File Interoperability: PASS")
    else:
        print("File Interoperability: FAIL")
        print(faildf)
    print("\n-------------------------------------------------------------------------------------------------------------------\n")
    print(assessdf)
    # print(skipdf)


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