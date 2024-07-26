import pandas as pd

# EVAL METHODS [val1, val2]: 
# 0 = compare with min, max [min, max]
# 1 = octet count [cnt, 00]
# 2 = bit string [len, 00]
# 3 = boolean [00, 00]
# 4 = hashalg list [00, 00]
# 5 = IA5 string [minlen, maxlen]
# 6 = UTF8 string [minlen, maxlen]
# 7 = signer [00, 00]

ieee16092_spdu_ref = [
    ["16092.version", "16092", 1, 0, 3, 3, True],
    ["16092.hashalg", "16092.content", 1, 4, 00, 00, True],
    ["16092.version", "16092.tabsData", 1, 0, 3, 3, False],
    ["16092.psid", "16092.headerInfo", 8, 0, 0, 18446744073709551615, True],
    ["16092.generationTime64", "16092.headerInfo", 8, 0, 0, 18446744073709551615, False],
    ["16092.3d_lat", "16092.generationLocation", 4, 0, -900000000, 900000001, False],
    ["16092.3d_lon", "16092.generationLocation", 4, 0, -1799999999, 1800000001, False],
    ["16092.3d_elev", "16092.generationLocation", 2, 0, -4095, 61439, False],
    ["16092.signer", "16092.content", 1, 7, 00, 00, False],
    # signer = "digest"
    ["16092.hashedid", "16092.signer", 8, 1, 8, 00, False],
    ["16092.ecc_key_x", "16092.signature", 32, 1, 32, 00, False],
    ["16092.ecc_key_y", "16092.signature", 32, 1, 32, 00, False],
    ["16092.s", "16092.signature", 32, 1, 32, 00, True],
    # signer = "certificate"
    ["16092.cert_ver", "signer_certificate", 1, 0, 3, 3, False],
    ["16092.certtype", "signer_certificate", 1, 0, 0, 1, False],
    ["16092.hashedid", "issuer", 8, 1, 8, 00, False],
    ["16092.hostname", "certificateId", 7, 6, 00, 00, False],
    ["16092.cracaId", "toBeSigned", 3, 1, 3, 00, False],
    ["16092.crl_series", "toBeSigned", 2, 0, 0, 65535, False],
    ["16092.start_validity", "toBeSigned", 4, 0, 0, 2147483646, False],
    ["16092.lifetime", "toBeSigned", 2, 0, 0, 65535, False],
    ["16092.psid", "appPermission", 4, 0, 0, 4294967295, False],
    ["16092.ecc_key_y", "verificationKeyIndicator", 32, 1, 32, 00, False],
]
ieee16092_spdu_refdf = pd.DataFrame(ieee16092_spdu_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])