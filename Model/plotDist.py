from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import sys
from itertools import groupby
from collections import Counter
import decimal 
import seaborn as sns
from numpy.random import normal
from scipy.optimize import curve_fit

#positive
filename = sys.argv[1]
file = open(filename,'r')
data = file.readlines()
array = []
for element in data:
	element = element.replace('\n', '')
	array.append(int(element))

#print len(array)
#negative
filename = sys.argv[2]
file = open(filename, 'r')
data = file.readlines()
array2 = []
for element in data:
	element = element.replace('\n', '')
	array2.append(int(element))


#positive control
density = gaussian_kde(array)
bins = np.linspace(-100,800,2971)
xs = bins
density.covariance_factor = lambda : .5
density._compute_covariance()


#negative control
density2 = gaussian_kde(array2)
bins2 = np.linspace(-100,800,2971)
xs2 = bins2
density2.covariance_factor = lambda : .5
density2._compute_covariance()

postArray = []
bins = []
#Calculates posterior probabilities 
for i in range(-100, 800):
	post = (density.evaluate(i) *0.6) / ((density.evaluate(i)*0.6)+(density2.evaluate(i)*0.4))
	postArray.append(post[0])

density = density(xs)
maxPosit = max(density)
for i in range(len(density)):
	density[i] = density[i]/maxPosit

#plt.plot(xs, density)

density2 = density2(xs2)
for i in range(len(density2)):
	density2[i] = density2[i]/maxPosit


graph = plt.plot(list(range(-100,800)), postArray)
#sepcifivity and senstivity 
plt.close()

xvalues = graph[0].get_xdata().tolist()
yvalues = graph[0].get_ydata().tolist()

#print len(xvalues), len(yvalues)
idx = xvalues.index(0)


#Caluclating Sensitivity and Specificity 
positives = []
negatives = []
xROC = []
yROC = []
accuracy = []
thresholdArray = []
threshold = 0.05
while threshold < 1:
	TP = 0
	FN = 0
	for element in array:
		element = int(element)
		if element not in xvalues:
			continue
		idx = xvalues.index(element)
		prob = yvalues[idx]
		if prob <= threshold:
			FN += 1
		else:
			TP += 1

	TN = 0
	FP = 0
	for element in array2:
		element = int(element)
		if element not in xvalues:
			continue
		idx = xvalues.index(element)
		prob = yvalues[idx]
		if prob <= threshold:
			TN += 1
		else:
			FP += 1

	positives.append((TP/(TP+FN)))
	negatives.append((TN/(TN+FP)))
	xROC.append(1-(TP/(TP+FN)))
	yROC.append((TN/(TN+FP)))
	accuracy.append((TP+TN)/(TP+TN+FP+FN))
	thresholdArray.append(threshold)
	threshold += 0.05

#plotting accuracy
'''
plt.plot(thresholdArray, accuracy, label = 'Accuracy')
plt.legend(loc ='best')
plt.xlabel('Threshold Cutoff')
plt.ylabel('Accurancy')
graph = plt.gca()
graph.set_xlim([0.10, 0.80])
graph.set_ylim([0.8,0.9])
plt.show()
'''

#ROC plot
'''
plt.plot(xROC, yROC, label= 'ROC')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc = 'best')
plt.show()
'''


#Specificity vs sensitivity  
'''
plt.plot(thresholdArray, positives, label = 'Sensitivity')
plt.plot(thresholdArray, negatives, label = 'Specificty ')
plt.legend(loc ='best')
plt.xlabel('Posterior Threshold')
plt.ylabel('Performance')
plt.show()
'''


