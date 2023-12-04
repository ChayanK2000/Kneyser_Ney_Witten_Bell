import re
import sys
import random


class KN():
    def __init__(self, n, dict4gram, dict3gram, dict2gram, UnigramCounts, Vocab, total_words):
        self.n = (int)(n)
        self.dict4gram = dict4gram
        self.dict3gram = dict3gram
        self.dict2gram = dict2gram
        self.UnigramCounts = UnigramCounts
        self.Vocab = Vocab
        self.total_words = total_words

    def kneyser_ney(self, testdata):
        Prob = 1
        index = 0
        global sentences
        global totalsent
        global words
        sumPP = 0
        # print(sentences)
        for i in range(len(testdata)):
            if i+3 <= len(testdata)-1:
                if testdata[i] == "</s>" or testdata[i + 2] == "</s>":

                    continue

                context = testdata[i:i + 4 - 1]
                context = " ".join(context)
                word = testdata[i + 4 - 1]
                zzzz = self.answer(4, context, word)
                Prob = Prob * zzzz

                if (word == "</s>"):
                    # if not((Prob == 0) or (words[index] > 80)):

                    #     PP = (1/Prob) ** (1/words[index])
                    #     print(sentences[index] + "\t" + str(PP) + "\n")
                    #     sumPP += PP
                    #     print(sumPP)
                    print(Prob)
                    Prob = 1
                    index += 1
        # return (sumPP / (1000))
        # return sumPP
        return

    def answer(self, n, context, word):
        if n == 1:
            denom = sum(self.UnigramCounts.values())
            if word in self.UnigramCounts:
                num = max(self.UnigramCounts[word]-0.75, 0)

                Pmle = num/denom
            else:
                Pmle = random.uniform(1e-5, 1e-6)
            return Pmle
            # in if-else which means not present in data: add manually or <unk>
        if n != 4:
            context = re.split(" ", context)
            context = context[1:]
            context = " ".join(context)
        unique = self.kn_constant(context, word, n)
        if unique == 0:  # when a context does not match
            return self.answer(n - 1, context, word)
        if n == 4:
            denom = sum(self.dict4gram[context].values())
            # when context matches and word
            if word in self.dict4gram[context]:
                num = max(self.dict4gram[context][word] - 0.75, 0)

                Pmle = num/denom

            else:
                Pmle = 0

        elif n == 3:
            denom = sum(self.dict3gram[context].values())
            if word in self.dict3gram[context]:
                num = max(self.dict3gram[context][word] - 0.75, 0)

                Pmle = num/denom

            else:
                Pmle = 0

        elif n == 2:
            denom = sum(self.dict2gram[context].values())
            if word in self.dict2gram[context]:
                num = max(self.dict2gram[context][word] - 0.75, 0)

                Pmle = num/denom
            else:
                Pmle = 0

        return ((Pmle) + (0.75/denom) * unique * self.answer(n - 1, context, word))

    def kn_constant(self, context, word, n):
        # here we check everytime whether the context is present or not. if not simply return lamda const as 0
        if n == 4:
            if context in self.dict4gram:
                unique = len(self.dict4gram[context])
                # denom = sum(self.dict4gram[context].values())
                # res = unique / (unique + denom)
                return (unique)
            else:
                return 0
        if n == 3:
            if context in self.dict3gram:
                unique = len(self.dict3gram[context])
                # denom = sum(self.dict3gram[context].values())
                # res = unique / (unique + denom)
                return (unique)
            else:
                return 0
        if n == 2:
            if context in self.dict2gram:
                unique = len(self.dict2gram[context])
                # denom = sum(self.dict2gram[context].values())
                # res = unique / (unique + denom)
                return (unique)
            else:
                return 0


class WB():
    def __init__(self, n, dict4gram, dict3gram, dict2gram, UnigramCounts, Vocab, total_words):
        self.n = (int)(n)
        self.dict4gram = dict4gram
        self.dict3gram = dict3gram
        self.dict2gram = dict2gram
        self.UnigramCounts = UnigramCounts
        self.Vocab = Vocab
        self.total_words = total_words

    def witten_bell(self, testdata):
        Prob = 1
        index = 0
        global sentences
        global totalsent
        global words
        sumPP = 0
        # print(sentences)
        for i in range(len(testdata)):
            if i+3 <= len(testdata)-1:
                if testdata[i] == "</s>" or testdata[i + 2] == "</s>":

                    continue

                context = testdata[i:i + 4 - 1]
                context = " ".join(context)
                word = testdata[i + 4 - 1]

                Prob = Prob * self.answer(4, context, word)

                if (word == "</s>"):
                    # case when if due to bad cleaning or rarely if a sentence is ultra very long, the probability go beyond 1e-325 beyond which python rounds it off to zero.
                    # if not ((Prob == 0) or (words[index] > 80)):
                    #     #thought of using log but that would interfere with other calcualtions.
                    #     PP = (1/Prob) ** (1/words[index])
                    #     print(sentences[index] + "\t" + str(PP) + "\n")
                    #     sumPP += PP
                    # print(sumPP)
                    print(Prob)
                    Prob = 1
                    index += 1
        # return (sumPP/(totalsent-1000))
        # return sumPP
        return

    def answer(self, n, context, word):
        if n == 1:
            if word in self.UnigramCounts:
                Pmle = self.UnigramCounts[word] / \
                    sum(self.UnigramCounts.values())
            else:
                Pmle = random.uniform(1e-5, 1e-6)
            return Pmle
            # in if-else which means not present in data: add manually or <unk>
        if n != 4:
            context = re.split(" ", context)
            context = context[1:]
            context = " ".join(context)
        lmbd = self.wb_constant(context, word, n)
        if lmbd == 0:  # when a context does not match
            return self.answer(n - 1, context, word)
        if n == 4:

            # when context matches but not word
            if word in self.dict4gram[context]:
                Pmle = self.dict4gram[context][word] / \
                    sum(self.dict4gram[context].values())
            else:
                Pmle = 0

        elif n == 3:
            if word in self.dict3gram[context]:
                Pmle = self.dict3gram[context][word] / \
                    sum(self.dict3gram[context].values())
            else:
                Pmle = 0

        elif n == 2:
            if word in self.dict2gram[context]:
                Pmle = self.dict2gram[context][word] / \
                    sum(self.dict2gram[context].values())
            else:
                Pmle = 0

        return ((lmbd * Pmle) + (1 - lmbd) * self.answer(n - 1, context, word))

    def wb_constant(self, context, word, n):
        # here we check everytime whether the context is present or not. if not simply return lamda const as 0
        if n == 4:
            if context in self.dict4gram:
                unique = len(self.dict4gram[context])
                denom = sum(self.dict4gram[context].values())
                res = unique / (unique + denom)
                return (1 - res)
            else:
                return 0
        elif n == 3:
            if context in self.dict3gram:
                unique = len(self.dict3gram[context])
                denom = sum(self.dict3gram[context].values())
                res = unique / (unique + denom)
                return (1 - res)
            else:
                return 0
        elif n == 2:
            if context in self.dict2gram:
                unique = len(self.dict2gram[context])
                denom = sum(self.dict2gram[context].values())
                res = unique / (unique + denom)
                return (1 - res)
            else:
                return 0


def loadtrainingData(path):
    f = open(path, 'r')
    raw = f.read()

    return (preprocess(raw))


def loadtestingData(path):
    f = open(path, 'r')
    raw = f.read()
    global sentences
    global words
    words = {}
    sentences = raw.splitlines()
    global totalsent
    totalsent = len(sentences)
    i = 0
    for sent in sentences:
        # to get words in every sentence. as 1 extra at end-compensates for </s>
        words[i] = len(re.split("[^A-Za-z]+", sent))
        i += 1
    return (preprocess(raw))


def preprocess(raw):
    raw = raw.rstrip("\n")
    raw = re.sub("[<>/]", "", raw)
    raw = re.sub("\n", " </s> </s> </s>\n<s> <s> <s> ", raw)

    raw = "<s> <s> <s> " + raw + " </s> </s> </s>"
    raw.lower()  # to accomodate the fact ki without this 'The' not same as 'the'
    train = re.split("[^A-Za-z<>/]+", raw)
    train = [i for i in train if i]

    return train


def createFourgram(data):
    listOfFourgrams = []
    # FourgramCounts = {}
    dict4gram = {}
    for i in range(len(data)):
        # print(i)
        if i+3 <= len(data)-1:
            # below if to just have 1 </s> at end
            if data[i] == "</s>" or data[i+2] == "</s>":
                continue

            context = data[i] + " " + data[i + 1] + " " + data[i + 2]

            listOfFourgrams.append(
                (data[i], data[i + 1], data[i+2], data[i+3]))

            if context in dict4gram:
                if data[i+3] in dict4gram[context]:
                    dict4gram[context][data[i + 3]] += 1
                else:
                    dict4gram[context][data[i+3]] = 1
            else:
                dict4gram[context] = {}
                dict4gram[context][data[i+3]] = 1

    return listOfFourgrams, dict4gram


def createTrigram(data):
    listOfTrigrams = []
    # TrigramCounts = {}
    dict3gram = {}
    for i in range(len(data)):
        if i+2 <= len(data)-1:
            if data[i] == "</s>" or data[i+1] == "</s>" or (data[i] == "<s>" and data[i+1] == "<s>" and data[i+2] == "<s>"):
                continue

            context = data[i] + " " + data[i + 1]

            listOfTrigrams.append(
                (data[i], data[i + 1], data[i+2]))

            if context in dict3gram:
                if data[i + 2] in dict3gram[context]:
                    dict3gram[context][data[i + 2]] += 1
                else:
                    dict3gram[context][data[i+2]] = 1
            else:
                dict3gram[context] = {}
                dict3gram[context][data[i+2]] = 1

    return listOfTrigrams, dict3gram


def createBigram(data):
    listOfBigrams = []
    dict2gram = {}
    for i in range(len(data)):
        if i+1 <= len(data)-1:
            if (data[i] == "</s>" or (data[i] == "<s>" and data[i+1] == "<s>")):
                continue

            context = data[i]

            listOfBigrams.append(
                (data[i], data[i + 1]))

            if context in dict2gram:
                if data[i+1] in dict2gram[context]:
                    dict2gram[context][data[i + 1]] += 1
                else:
                    dict2gram[context][data[i+1]] = 1
            else:
                dict2gram[context] = {}
                dict2gram[context][data[i+1]] = 1

    return listOfBigrams, dict2gram


def createUnigram(data):
    listOfUnigrams = []
    UnigramCounts = {}
    Vocab = 0
    for i in range(len(data)):
        if i+1 <= len(data)-1:
            if (data[i] == "</s>" or (data[i] == "<s>" and data[i + 1] == "<s>")):
                continue
            listOfUnigrams.append(data[i])
            if (data[i]) in UnigramCounts:
                UnigramCounts[(data[i])] += 1
            else:
                UnigramCounts[(data[i])] = 1
                Vocab += 1
    return listOfUnigrams, UnigramCounts, Vocab


if __name__ == '__main__':
    args = sys.argv
    smooth_type = args[1]
    path = args[2]
    # testpath = args[3] # used it for ass2 
    # testdata = loadtestingData(testpath)

    testdata = input("input sentence: ")
    testdata = preprocess(testdata)
    data = loadtrainingData(path)
    
    # print(data)
    # if path == "training_health.txt" or path == "./training_health.txt":
    #     testdata = loadtestingData("test_health.txt")
    # else:
    #     testdata = loadtestingData("training_technical.txt")

    listOfFourgrams, dict4gram = createFourgram(data)
    listOfTrigrams, dict3gram = createTrigram(data)
    listOfBigrams, dict2gram = createBigram(data)
    listOfUnigrams, UnigramCounts, Vocab = createUnigram(data)
    # to include "</s> in frequencies"
    UnigramCounts["</s>"] = UnigramCounts["<s>"]
    total_words = len(listOfUnigrams)
    '''
    print("\n All the possible Fourgrams are ")
    print(listOfFourgrams)
    print("\n Fourgrams along with their frequency ")
    print(FourgramCounts)
    print("\n All possible trigrams are")
    print(listOfTrigrams)
    print("\n Tri with freq ")
    print(TrigramCounts)
    print("\n All possible Bigrams are")
    print(listOfBigrams)
    print("\n Bi with freq ")
    print(BigramCounts)

    print("Fourgrams\n", dict4gram)
    print("\nThreegrams\n", dict3gram)
    print("\nBigrams\n", dict2gram)
    print("\n All possible Unigrams are")
    print(listOfUnigrams)
    print("\n Total words: ", Vocab, " with freq ")
    print(UnigramCounts)
    '''

    listOfFourgrams1, dict4gram1 = createFourgram(testdata)
    listOfTrigrams1, dict3gram1 = createTrigram(testdata)
    listOfBigrams1, dict2gram1 = createBigram(testdata)
    listOfUnigrams1, UnigramCounts1, Vocab1 = createUnigram(testdata)

    global sentences
    # print(sentences)
    if(smooth_type == "w"):
        model = WB(4, dict4gram, dict3gram, dict2gram,
                   UnigramCounts, Vocab, total_words)
        avgPP = model.witten_bell(testdata)
        # print(avgPP)
    elif(smooth_type == "k"):
        model = KN(4, dict4gram, dict3gram, dict2gram,
                   UnigramCounts, Vocab, total_words)
        avgPP = model.kneyser_ney(testdata)
        # print(avgPP)
