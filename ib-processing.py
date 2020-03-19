#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt


data_dict = {} 

noise_level = 0
current_classifier = 0
first_data = True
counter = 0

def stats(data=[]):
    mean = 0
    for val in data:
      mean += val
    mean = mean / len(data)

    std = 0
    for val in data:
      std += math.pow(val - mean, 2)
    std = std / (len(data)-1)
    std = math.sqrt(std)

    #print("mean: {}".format(mean))
    #print("std : {}".format(std))
    #print("variance: {}".format(std**2)) <-- This isn't correct if you've passed the data in as percentages

    return mean, std


class Classifiers:
    def __init__(self):
        self._classifier_list = []

    def add(self, classifier):
        self._classifier_list.append(classifier)

    def addDataToClassifier(self, classifier_id, seed, data):
        self._classifier_list[classifier_id].addToData(seed, data)

class Classifier:
    def __init__(self):
        self._data = {0:[]}

    def __str__(self):
        return str(self._data)

    def addToData(self, noise, acc):
        if noise in self._data:
            self._data[noise].append(acc)
        else:
            self._data[noise] = [acc]

    def getData(self):
        return self._data

ib1 = Classifier()
ib2 = Classifier()
ib3 = Classifier()

classifiers = Classifiers()
classifiers.add(ib1)
classifiers.add(ib2)
classifiers.add(ib3)

for line in open('./ib1-3_output'):
    #print(line)
    line_arr = line.split(' ')
    if 'noise' in line_arr:
        new_noise_level = int(line_arr[3][:-1])
        print('new noise level: {}'.format(new_noise_level))
        
        if new_noise_level != noise_level:
            # Create the new dictionary entry with arrays for the new data
            data_dict[new_noise_level] = [[], [], []]
            noise_level = new_noise_level
            print('new place added in dictionary!')

    elif 'IB1' in line_arr:
        print('IB1')
        #data_dict[noise_level][0].append(
        #print(line_arr) <- we can use this to get the number of instances in the CD 
        current_classifier = 0

    elif 'IB2' in line_arr:
        print('IB2')
        current_classifier = 1
    elif 'IB3' in line_arr:
        print('IB3')
        current_classifier = 2

    elif 'Correctly' in line_arr:
        if first_data:
            first_data = False
        else:
            # Convert the percentage value of the classifier to a float
            acc = float([val for val in line_arr if val != ''][-2])
            print(acc)

            #data_dict[noise_level][current_classifier][counter] = acc
            classifiers.addDataToClassifier(current_classifier, noise_level, acc)

            # Reset so we ignore the next first line
            first_data = True

#print(ib1)
#print(ib2)
#print(ib3)

# Calculate statistics for IB1
data = ib1.getData()
ib1_mean = []
ib1_err = []
print('IB1:')
for noise in data.keys():
    print(noise) # + ' : ' + str(data[noise]))

    # Calculate the mean of all these tests
    mean, std = stats(data[noise])
    print('Mean: {}\tStd: {}'.format(mean, std))

    ib1_mean.append(mean)
    ib1_err.append(std)

# Calculate statistics for IB2
data = ib2.getData()
ib2_mean = []
ib2_err = []
print('IB2:')
for noise in data.keys():
    print(noise) # + ' : ' + str(data[noise]))

    # Calculate the mean of all these tests
    mean, std = stats(data[noise])
    print('Mean: {}\tStd: {}'.format(mean, std))

    ib2_mean.append(mean)
    ib2_err.append(std)

# Calculate statistics for IB3
data = ib3.getData()
ib3_mean = []
ib3_err = []
print('IB3:')
for noise in data.keys():
    print(noise) # + ' : ' + str(data[noise]))

    # Calculate the mean of all these tests
    mean, std = stats(data[noise])
    print('Mean: {}\tStd: {}'.format(mean, std))

    ib3_mean.append(mean)
    ib3_err.append(std)

noise_levels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

# Print the data
plt.errorbar(noise_levels, ib1_mean, ib1_err, color='blue', label='IB1')
plt.errorbar(noise_levels, ib2_mean, ib2_err, color='green', label='IB2')
plt.errorbar(noise_levels, ib3_mean, ib3_err, color='red', label='IB3')
plt.xlabel('Noise Levels (%)')
plt.xticks(noise_levels)
plt.ylabel('Accuracy (%)')

plt.legend()
plt.title('Instance-Based Classifier Accuracy with Increasing\nNoise on the LED Dataset')
plt.savefig('ib1-3_noise_graph.png')

plt.tight_layout()
plt.show()
