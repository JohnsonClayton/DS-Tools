#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt


data_dict = {} 

noise_level = 0
current_classifier = 0
first_data = True
counter = 0



class Classifiers:
    def __init__(self):
        self._classifier_list = []

    def add(self, classifier):
        self._classifier_list.append(classifier)

    def addAccToClassifier(self, classifier_id, seed, data):
        self._classifier_list[classifier_id].addAccData(seed, data)

    def addMemToClassifier(self, classifier_id, seed, data):
        self._classifier_list[classifier_id].addMemData(seed, data)

class Classifier:
    def __init__(self):
        self._acc = {0:[]}
        self._mem = {0:[]}

    def __str__(self):
        return str(self._acc)

    def addAccData(self, noise, acc):
        if noise in self._acc:
            self._acc[noise].append(acc)
        else:
            self._acc[noise] = [acc]

    def addMemData(self, noise, acc):
        if noise in self._acc:
            self._mem[noise].append(acc)
        else:
            self._mem[noise] = [acc]

    def _stats(self, data=[]):
        mean = 0
        for val in data:
          mean += val
        mean = mean / len(data)

        std = 0
        for val in data:
          std += math.pow(val - mean, 2)
        std = std / (len(data)-1)
        std = math.sqrt(std)

        ##print("mean: {}".format(mean))
        ##print("std : {}".format(std))
        ##print("variance: {}".format(std**2)) <-- This isn't correct if you've passed the data in as percentages

        return mean, std

    def calcAccStats(self):
        # Calculate statistics for IB3
        data = self._acc
        mean_list = []
        err_list = []
        for noise in data.keys():
            # Calculate the mean of all these tests
            mean, std = self._stats(data[noise])
            #print('Mean: {}\tStd: {}'.format(mean, std))

            mean_list.append(mean)
            err_list.append(std)

        return mean_list, err_list

    def calcMemStats(self):
        # Calculate statistics for IB3
        data = self._mem
        mean_list = []
        err_list = []
        for noise in data.keys():
            # Calculate the mean of all these tests
            mean, std = self._stats(data[noise])
            #print('Mean: {}\tStd: {}'.format(mean, std))

            mean_list.append(mean)
            err_list.append(std)

        return mean_list, err_list


    def getAcc(self):
        return self._acc

ib1 = Classifier()
ib2 = Classifier()
ib3 = Classifier()

classifiers = Classifiers()
classifiers.add(ib1)
classifiers.add(ib2)
classifiers.add(ib3)

noise_list = []

for line in open('./ib1-3_output'):
    ##print(line)
    line_arr = line.split(' ')
    if 'noise' in line_arr:
        new_noise_level = int(line_arr[3][:-1])
        #print('new noise level: {}'.format(new_noise_level))

        if not new_noise_level in noise_list:
            noise_list.append(new_noise_level)
        
        if new_noise_level != noise_level:
            # Create the new dictionary entry with arrays for the new data
            data_dict[new_noise_level] = [[], [], []]
            noise_level = new_noise_level
            #print('new place added in dictionary!')

    elif 'IB1' in line_arr:
        #print('IB1')
        #data_dict[noise_level][0].append(
        #print(line_arr[3]) # <- we can use this to get the number of instances in the CD 
        current_classifier = 0
        classifiers.addMemToClassifier(current_classifier, noise_level, int(line_arr[3]))
    elif 'IB2' in line_arr:
        #print('IB2')
        current_classifier = 1
        classifiers.addMemToClassifier(current_classifier, noise_level, int(line_arr[3]))
    elif 'IB3' in line_arr:
        #print('IB3')
        current_classifier = 2
        classifiers.addMemToClassifier(current_classifier, noise_level, int(line_arr[3]))

    elif 'Correctly' in line_arr:
        if first_data:
            first_data = False
        else:
            # Convert the percentage value of the classifier to a float
            acc = float([val for val in line_arr if val != ''][-2])
            #print(acc)

            #data_dict[noise_level][current_classifier][counter] = acc
            classifiers.addAccToClassifier(current_classifier, noise_level, acc)

            # Reset so we ignore the next first line
            first_data = True


# Calculate the means for acc
ib1_acc_mean, ib1_acc_err = ib1.calcAccStats()
ib2_acc_mean, ib2_acc_err = ib2.calcAccStats()
ib3_acc_mean, ib3_acc_err = ib3.calcAccStats()

# Print the data
plt.errorbar(noise_list, ib1_acc_mean, ib1_acc_err, color='blue', label='IB1')
plt.errorbar(noise_list, ib2_acc_mean, ib2_acc_err, color='green', label='IB2')
plt.errorbar(noise_list, ib3_acc_mean, ib3_acc_err, color='red', label='IB3')
plt.xlabel('Noise Levels (%)')
plt.xticks(noise_list)
plt.ylabel('Accuracy (%)')

plt.legend()
plt.title('Instance-Based Classifier Accuracy with Increasing\nNoise on the LED Dataset')
plt.savefig('ib1-3_accuracy.png')

plt.tight_layout()
plt.show()



# Calculate the means for mem
ib1_mem_mean, ib1_mem_err = ib1.calcMemStats()
ib2_mem_mean, ib2_mem_err = ib2.calcMemStats()
ib3_mem_mean, ib3_mem_err = ib3.calcMemStats()

# Print the data
plt.errorbar(noise_list, ib1_mem_mean, ib1_mem_err, color='blue', label='IB1')
plt.errorbar(noise_list, ib2_mem_mean, ib2_mem_err, color='green', label='IB2')
plt.errorbar(noise_list, ib3_mem_mean, ib3_mem_err, color='red', label='IB3')
plt.xlabel('Noise Levels (%)')
plt.xticks(noise_list)
plt.ylabel('Instances Saved')

plt.legend()
plt.title('Instance-Based Classifier Instances Saved with Increasing\nNoise on the LED Dataset')
plt.savefig('ib1-3_memory.png')

plt.tight_layout()
plt.show()
