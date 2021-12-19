import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os
import time

start = time.time()
stemmed = " "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
directory = 'D:\Programming\Search Engine Project\\DummyData'


ss = SnowballStemmer("english")

wordsList = []

previousData = {}
previousForwardData = {}
previousReverseData = defaultdict(list)

lexiconFile = open("lexicon.json", "w")
forwardIndexFile = open("forwardIndex.json", "w")
reverseIndexFile = open("reverseIndex.json", "w")

docID = 0
tokenID = 0

for root, dirs, files in os.walk(directory):
    for filename in files:
        currentFile = (os.path.join(root, filename))
        print((currentFile))

        stop_words = set(stopwords.words('english'))

        f = open(currentFile)
        data = json.load(f)

        for i in range(len(data)):
            list1 = data[i]
            words = list1['content']
            wordsList = words.split()

            docID += 1

            for word in wordsList:
                hitlist = []
                if word not in stop_words:
                    stemmed_word = ss.stem(word)

                    string_encode = stemmed_word.encode("ascii", "ignore")
                    string_decode = string_encode.decode()

                    if string_decode not in previousData:
                        previousData[string_decode] = tokenID
                        tokenID += 1

                    for i in wordsList:
                        if string_decode in wordsList:
                            hitlist.append(i)

                    if string_decode in previousData:

                        if previousData[string_decode] not in previousForwardData.keys():
                            previousForwardData.__setitem__(docID, {
                                previousData[string_decode]: hitlist})

                        previousReverseData[previousData[string_decode]].append(
                            docID)

for i in previousReverseData:
    previousReverseData[i] = list(dict.fromkeys(previousReverseData[i]))

json.dump(previousData, lexiconFile)
json.dump(previousForwardData, forwardIndexFile)
json.dump(previousReverseData, reverseIndexFile)

lexiconFile.close()
forwardIndexFile.close()
reverseIndexFile.close()

end = time.time()
print((end - start) / 60)
