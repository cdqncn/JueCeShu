import matplotlib.pyplot as plt
import myTree

deciNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(Nodename, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(Nodename, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
                            textcoords='axes fraction', va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def getNumLeafs(myTree):  # 获取叶节点的数目
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])  # 递归
        else:
            numLeafs += 1
    return numLeafs


def getTreeDepth(myTree):  # 获取决策树的高度
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])  # 递归
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)  # this determines the x width of this tree
    # 计算树的高
    depth = getTreeDepth(myTree)
    # 第一个关键字为第一次划分数据集的类别标签，附带的取值表示子节点的取值
    firstStr = list(myTree.keys())[0]  # the text label for this node should be this
    # 下一个节点的位置
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    # 计算父节点和子节点的中间位置，并在此处添加简单的文本信息
    plotMidText(cntrPt, parentPt, nodeTxt)
    # 绘制此节点带箭头的注解
    plotNode(firstStr, cntrPt, parentPt, deciNode)
    # 新的树，相当于脱了一层皮
    secondDict = myTree[firstStr]
    # 按比例减少全局变量plotTree.yOff
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    #
    for key in secondDict.keys():
        # 判断子节点是否为字典类型
        if type(secondDict[key]).__name__ == 'dict':
            # 是的话表明该节点也是一个判断节点，递归调用plotTree()函数
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            # 不是的话更新x坐标值
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            # 绘制此节点带箭头的注解
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            # 绘制此节点带箭头的注解
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    # 按比例增加全局变量plotTree.yOff
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


fr = open('C:\\Users\\chend\\Desktop\\MLproject\\deciTree\\Task1\\lenses.txt')
lenses = [inst.strip().split('\t') for inst in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
lensesTree = myTree.createTree(lenses, lensesLabels)
createPlot(lensesTree)
