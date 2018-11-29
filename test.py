from collections import deque
import numpy as np
from numpy_ringbuffer import RingBuffer

# d = deque([], 5)
#
# for c in '123456789101112':
#     d.appendleft(c)
#     # print(list(d))
#     x = list(d)
#     print(x)
#     # v = [(np.mean((x[i], x[i + 1]))) for i in range(len(x) - 1)]
#     if(len(x) == 5):
#         v = sum(int(i) for i in x)
#         v = v / 5
#         print(v)

def _sma(l):
    for number in range(10):
       number = number + 1

       if number == l:
          break    # break here

       print('Number is ' + str(number))


# _sma(5)


# r = RingBuffer(capacity=4, dtype=np.int)
# for c in '123456789':
#     r.append(c)   # r.appendleft(False)
#     print(np.array(r))  # array([False, True])

# import time
# starttime = time.time()
# print("Start")
# while True:
#     print(((time.time() - starttime) % 60.0))

#     print("tick")
#     time.sleep(60.0 - ((time.time() - starttime) % 60.0))

#
# import numpy as np
# from matplotlib import pyplot as plt
#
# data = {"x": np.arange(50), "y": np.random.random(50)}
#
#
# avg, sigma = data['y'].mean(), data['y'].std()
# mask_highs = data['y'] > avg + sigma
# mask_lows = data['y'] < avg - sigma
# mask_middle = ~ mask_highs & ~ mask_lows
# plt.scatter(data['x'][mask_highs],data['y'][mask_highs],c="green")
# plt.scatter(data['x'][mask_lows],data['y'][mask_lows],c="black")
# plt.scatter(data['x'][mask_middle],data['y'][mask_middle],c="blue")
#
# plt.axhline(avg + sigma, c="red")
# plt.axhline(avg - sigma, c="red")
# plt.show()