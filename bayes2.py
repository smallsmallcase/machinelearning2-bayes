# @Time    : 2017/10/6 16:31
# @Author  : Jalin Hu
# @File    : bayes.py
# @Software: PyCharm


import numpy
import re
import random


def text_parse(bigstring):
    words = re.split(r'\W*', bigstring)
    return [word.lower() for word in words if len(word) > 1]


# def load_data_set():
#     posting_list = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
#                     ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
#                     ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
#                     ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
#                     ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
#                     ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
#     class_vect = [0, 1, 0, 1, 0, 1]
#     return posting_list, class_vect


def create_vlcab_list(data_set):
    vocab_set = set()
    for document in data_set:
        vocab_set = vocab_set | set(document)
    return list(vocab_set)


def bagof_word2vec(vocablist, inputset):
    returnvec = [0] * len(vocablist)
    for word in inputset:
        if word in vocablist:
            returnvec[vocablist.index(word)] += 1
        else:
            print('word:', word, 'is not in the list')
    return returnvec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numwords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)  # 计算p(ci),文档属于侮辱类的概率
    # p0Num = numpy.zeros(numwords)
    # p1Num = numpy.zeros(numwords)
    # p0denom = 0.0
    # p1denom = 0.0
    p0Num = numpy.ones(numwords)
    p1Num = numpy.ones(numwords)
    p0denom = 2.0
    p1denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0denom += sum(trainMatrix[i])
    p1vect = numpy.log(p1Num / p1denom)
    p0vect = numpy.log(p0Num / p0denom)
    return p1vect, p0vect, pAbusive


def classifyNB(vec2classify, p0vec, p1vec, pClass1):
    p1 = sum(vec2classify * p1vec) + numpy.log(pClass1)
    p0 = sum(vec2classify * p0vec) + numpy.log(1 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


if __name__ == '__main__':
    # postingList, classVec = load_data_set()
    postingList = []
    classVec = []
    for i in range(1, 26):
        with open('email/spam/%d.txt' % i, 'r') as f:
            text = f.read()
            postingList.append(text_parse(text))
            classVec.append(1)
        with open('email/ham/%d.txt' % i, 'r') as f:
            text = f.read()
            postingList.append(text_parse(text))
            classVec.append(0)
    myVocabList = create_vlcab_list(postingList)
    print('词库是：', myVocabList, '\n', '词库的长度是：', len(myVocabList))
    trainsetindex = list(range(50))
    testsetindex = []
    for i in range(10):
        randomindex = int(random.uniform(0, len(trainsetindex)))
        testsetindex.append(randomindex)
        del (trainsetindex[i])

    trainMat = []
    errorcount = 0
    for postinDoc in postingList:
        trainMat.append(bagof_word2vec(myVocabList, postinDoc))
    p1V, p0V, pAb = trainNB0(trainMat, classVec)

    for i in testsetindex:
        thisDoc = numpy.array(bagof_word2vec(myVocabList, postingList[i]))  # 测试样本向量化
        if classifyNB(thisDoc, p0V, p1V, pAb) != classVec[i]:
            errorcount += 1
            print('错误的测试集：', postingList[i])
    accuricy = float(errorcount / len(testsetindex) * 100)
    print('错误率：%.2f%%' % accuricy)
