import math

data = [55.94, 59.09, 58.74, 55.94, 59.44, 57.34, 59.09, 58.04, 59.09, 59.44]

mean = 0
for val in data:
  mean += val
mean = mean / len(data)

std = 0
for val in data:
  std += math.pow(val - mean, 2)
std = std / (len(data)-1)
std = math.sqrt(std)

print("mean: {}".format(mean))
print("std : {}".format(std))
print("variance: {}".format(std**2))
