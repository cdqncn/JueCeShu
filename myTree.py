from math import log
import operator


def createDataSet():
    dataSet = [[0, 0, 0, 0, 'N'],
               [0, 0, 0, 1, 'N'],
               [1, 0, 0, 0, 'Y'],
               [2, 1, 0, 0, 'Y'],
               [2, 2, 1, 0, 'Y'],
               [2, 2, 1, 1, 'N'],
               [1, 2, 1, 1, 'Y']]
    labels = ['outlook', 'temperature', 'humidity', 'windy']
    return dataSet, labels


def calcShannonEnt(dataSet):  # 计算熵
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1  # 数每一类各多少个， {'Y': 4, 'N': 3}
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1  # feature个数
    baseEntropy = calcShannonEnt(dataSet)  # 整个dataset的熵
    bestInfoGainRatio = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  # 每个feature的list
        uniqueVals = set(featList)  # 每个list的唯一值集合
        newEntropy = 0.0
        splitInfo = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  # 每个唯一值对应的剩余feature的组成子集
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            splitInfo += -prob * log(prob, 2)
        infoGain = baseEntropy - newEntropy  # 这个feature的infoGain
        if (splitInfo == 0):  # fix the overflow bug
            continue
        infoGainRatio = infoGain / splitInfo  # 这个feature的infoGainRatio增益率
        if (infoGainRatio > bestInfoGainRatio):  # 选择最大的gain ratio
            bestInfoGainRatio = infoGainRatio
            bestFeature = i  # 选择最大的gain ratio对应的feature
    return bestFeature


def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:  # 只看当第i列的值＝value时的item
            reduceFeatVec = featVec[:axis]  # featVec的第i列给除去
            reduceFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]  # ['N', 'N', 'Y', 'Y', 'Y', 'N', 'Y']
    if classList.count(classList[0]) == len(classList):
        # classList所有元素都相等，即类别完全相同，停止划分
        return classList[0]  # splitDataSet(dataSet, 0, 0)此时全是N，返回N
    if len(dataSet[0]) == 1:  # [0, 0, 0, 0, 'N']
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)  # 0－> 2
    # 选择最大的gain ratio对应的feature
    bestFeatLabel = labels[bestFeat]  # outlook -> windy
    myTree = {bestFeatLabel: {}}
    # 多重字典构建树{'outlook': {0: 'N'
    del (labels[bestFeat])  # ['temperature', 'humidity', 'windy'] -> ['temperature', 'humidity']
    featValues = [example[bestFeat] for example in dataSet]  # [0, 0, 1, 2, 2, 2, 1]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]  # ['temperature', 'humidity', 'windy']
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
        # 划分数据，为下一层计算准备
    return myTree


def majorityCnt(classList):  # 如果属性完全相同，却不具有相同的类别，则采用少数服从多数的原则进行划分
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        else:
            classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
