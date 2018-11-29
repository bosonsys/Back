import numpy as np
sList = [7455745, 4159745, 3050241, 4451329, 1492737, 4701441, 2997505, 625153, 5202177, 3660545, 134657, 1076225]
l = len(sList)
# print(len(sList))
data = np.zeros(l, dtype={'names':('name', 'instrument_token', 'mOpen', 'mHigh', 'mLow', 'mClose'),
                          'formats':('U10', 'i8', 'f8', 'f8', 'f8', 'f8')})
# print(data)

for n,a in enumerate(data):
    print(n, a)

    # for idx, val in enumerate(ints):
    #     print(idx, val)
