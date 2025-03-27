#  NIST-developed software is provided by NIST as a public service. You may use,
#  copy, and distribute copies of the software in any medium, provided that you
#  keep intact this entire notice. You may improve, modify, and create
#  derivative works of the software or any portion of the software, and you may
#  copy and distribute such modifications or works. Modified works should carry
#  a notice stating that you changed the software and should note the date and
#  nature of any such change. Please explicitly acknowledge the National
#  Institute of Standards and Technology as the source of the software.
#
#  NIST-developed software is expressly provided "AS IS." NIST MAKES NO WARRANTY
#  OF ANY KIND, EXPRESS, IMPLIED, IN FACT, OR ARISING BY OPERATION OF LAW,
#  INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, AND DATA ACCURACY. NIST
#  NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE
#  UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST DOES
#  NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR
#  THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY,
#  RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
#
#  You are solely responsible for determining the appropriateness of using and
#  distributing the software and you assume all risks associated with its use,
#  including but not limited to the risks and costs of program errors,
#  compliance with applicable laws, damage to or loss of data, programs or
#  equipment, and the unavailability or interruption of operation. This software
#  is not intended to be used in any situation where a failure could cause risk
#  of injury or damage to property. The software developed by NIST employees is
#  not subject to copyright protection within the United States.
#
#  Author: Eugene Song <eugene.song@nist.gov>
#  Author: Davide Pesavento <davide.pesavento@nist.gov>
#  Author: Tyler Wong

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

ieee16093_wsmp_ref = [  # col[0] = field name, col[1] = parent name, col[2] = length, col[3] = eval method, col[4] = ref value 1, col[5] = ref value 2, col[6] = mandatory?
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
