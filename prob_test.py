import numpy as np

thresh = 1
exp = 1
sum = 0
for i in range(100000):
    if np.random.exponential() > thresh:
        sum += 1

print(sum/100000.0)
# 50, 5 -> 0.7
# 50x2, 5 -> 8.3
# 50x3, 5 -> 18.7
# 50x4, 5 -> 28.6
# 50x5, 5 -> 36.8
