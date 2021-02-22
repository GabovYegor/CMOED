import csv
import random
import math
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.distributions.empirical_distribution import ECDF

random_seed = 79
data_elem_size = 107

def getDataFromFile(attribureNum):
    with open('machine.data', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        data = []
        for row in spamreader:
            data.append(int(row[attribureNum]))
    return data

def generateSample(data):
    random.seed(random_seed)
    data = random.sample(data, data_elem_size)
    return data

def printData(data):
    count = 0
    for i in data:
        count = count + 1
        if(count > 20):
            count = 0
            print(i)
        else:
            print(i, end =" "),
    print()

data = getDataFromFile(8)
data = generateSample(data)
print("Сформированная выборка:")
printData(data)
print("Ранжированный ряд:")
printData(sorted(data))

countedData = Counter(sorted(data))
count = 0
print('Варианционный ряд:')
for i in sorted(set(data)):
    count = count + 1
    if (count > 10):
        count = 0
        print(f'{i:3} ==> {countedData[i]:1}')
    else:
        print(f'{i:3} ==> {countedData[i]:1}', end=" ")
print()

intervalNum = int(1 + 3.322 * math.log10(data_elem_size))
print('Количество интервалов определенное по формуле Стерджесса = ',intervalNum)
print('Минимальное значение в выборке = ', min(data))
print('Максимальное значение в выборке = ', max(data))
dataRange = max(data) - min(data)
intervalSize = int(dataRange / intervalNum)
print('Размах выборки = ', max(data) - min(data))

isInBucket = lambda x: min(int((abs(x) - min(data)) / dataRange * intervalNum), intervalNum-1)
borders = [(min(data) + dataRange/intervalNum*i, min(data) + dataRange/intervalNum*(i+1)) for i in range(intervalNum)]
buckets = [[] for i in range(intervalNum)]
for value in data:
    buckets[isInBucket(value)].append(value)

print('Интервальный ряд')
print('  Интервал    абс. част.     относ. част')
for i in range(0, intervalNum):
    print(f'{(min(data) + intervalSize*i):3} - {min(data) + intervalSize*(i+1):3}'
          f'{len(buckets[i]):10} {len(buckets[i])/len(data):25}')

fig, ax = plt.subplots()
ax.hist(data, bins=intervalNum, density=False, edgecolor='black', facecolor='white')
center_of_borders = [(border[0] + border[1])/2 for border in borders]
y = [len(bucket) for bucket in buckets]
ax.plot(center_of_borders, y, '--k')
ax.set_xlabel('Значение')
ax.set_ylabel('Абсолютная частота')
ax.set_title('Гистограмма и полигон абсолютных частот')
fig.tight_layout()
plt.show()

fig, ax = plt.subplots()
ax.hist(data, intervalNum, weights=np.ones(len(data)) / len(data), density=False, edgecolor='black', facecolor='white')
center_of_borders = [(border[0] + border[1])/2 for border in borders]
y = [len(bucket)/data_elem_size  for bucket in buckets]
ax.plot(center_of_borders, y, '--k')
ax.set_xlabel('Значение')
ax.set_ylabel('Относительная частота')
ax.set_title('Гистограмма и полигон относительных частот')
fig.tight_layout()
plt.show()

maxBucketLen = 0
for bucket in buckets:
    if(maxBucketLen < len(bucket)/len(data)):
        maxBucketLen = len(bucket)/len(data)

absValues = []
sum = 0
print(sum)
for bucket in buckets:
    sum = sum + len(bucket)/len(data)
    absValues.append(sum)

ecdf = ECDF(absValues)
fig, ax = plt.subplots()
ax.set_xlabel('x')
ax.set_ylabel('F(x)')
ax.set_title('Эмпирическая функция распределения относительных частот')
ax.axis(xmin=maxBucketLen, xmax=max(ecdf.x))
ax.axis(ymin=-0.05, ymax=1.05)

for i in range(len(ecdf.x)-1):
    xs = [0, ecdf.x[i]]
    ys = [ecdf.y[i]] * 2
    ax.plot(xs, ys, 'r:', alpha=0.2)
    ax.plot(ecdf.x[i], ecdf.y[i], "k.") # точки
    xs = [ecdf.x[i], ecdf.x[i+1]]
    ys = [ecdf.y[i]] * 2
    ax.plot(xs, ys, 'k-')
ax.plot(ecdf.x[-1], ecdf.y[-1], "k.")
plt.show()



