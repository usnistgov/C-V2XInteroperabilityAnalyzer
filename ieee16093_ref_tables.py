import pandas as pd

# Eval methods: 
# 0 = compare with max, min (val1, val2)
# 1 = octet count (val1, 00)
# 2 = bit string (val1, 00)
# 3 = boolean (00, 00)

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