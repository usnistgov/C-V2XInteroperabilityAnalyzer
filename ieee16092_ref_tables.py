import pandas as pd

# Eval methods: 
# 0 = compare with max, min (val1, val2)
# 1 = octet count (val1, 00)
# 2 = bit string (val1, 00)
# 3 = boolean (00, 00)
# 4 = hashalg list (00, 00)

ieee16092_spdu_ref = [
    ["16092.version", "16092", 1, 0, 3, 3, True],
    ["16092.hashalg", "16092.content", 1, 4, 00, 00, True],
    ["16092.version", "16092.tabsData", 1, 0, 3, 3, False],
    ["16092.psid", "16092.headerInfo", 8, 0, 0, 18446744073709551615, True],
    ["16092.generationTime64", "16092.headerInfo", 8, 0, 0, 18446744073709551615, False],
    ["16092.hashedid", "16092.signer", 8, 1, 8, 00, False],
    ["16092.ecc_key_y", "16092.signature", 32, 1, 32, 00, True],
    ["16092.s", "16092.signature", 32, 1, 32, 00, True],
]
ieee16092_spdu_refdf = pd.DataFrame(ieee16092_spdu_ref, columns = ["field", "parent", "length", "eval method", "val1", "val2", "mandatory"])