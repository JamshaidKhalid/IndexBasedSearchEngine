import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os
import time
import string

#YOU DON'T NEED TO RUN THIS FILE SEPARATELY
#IT IS AUTOMATICALLY RUN WHEN LEXICONGENERATOR.PY IS RUN


# noting starting time
start = time.time()
stemmed = " "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''

# PLEASE
# Locate dataset folder and this program in the same directory and use the path in following form
directory = 'DataSet'
# OR ENTER THE PATH OF DATASET in following form WHILE TESTING THIS PROGRAM.
# directory = 'D:\\DSA Project\\main\\testDataSet'

# Using SnowBall stemmer to stem words like programming to 'program'
ss = SnowballStemmer("english")

# initializing the list
wordsList = []
wordsString = ""
# Dictionary intilaizaiton
previousData = {}

# Initializing it in defaultDictList so that in JSON we can have the format 0:[]
previousReverseData = defaultdict(list)
previousForwardData = defaultdict(list)


# Writing files in w mode later will change it to append mode
lexiconFile = open("titleLex.json", "w")
forwardIndexFile = open("titleForIndex.json", "w")
reverseIndexFile = open("titleRevIndex.json", "w")

# tokenID assigns the wordID and docID assigns the docID
docID = 0
tokenID = 0
# stopwords to remove
stop_words = stopwords.words('english')
newStopWords = ['a', 'b', 'c', 'd', 'e', '', 'f', 'g', 'h', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
stop_words.extend(newStopWords)
# Checking the whole directory
for root, dirs, files in os.walk(directory):
    # parsing all the files in it
    for filename in files:

        # each time the loop runs, currentFile will have the complete path and name of each next file
        currentFile = (os.path.join(root, filename))
        print(docID)
        print((currentFile))

        # opening currentFile as f, currentFile has the path of file
        f = open(currentFile)

        # Now, Data has the text of whole json file in form of Dictionary
        data = json.load(f)
        # indexes=[]

        # traversing data as json is now loaded in data as dictionary

        for i in range(len(data)):
            # indexes=[]

            innerDict = {}
            outerDict = {}
            hitList = []
            hits = 0
            list1 = data[i]
            # parsing the CONTENT only to form the lexicon
            words = list1['title']

            # now WORDS has all the text of content of json.

            # we will join words at spaces to form wordsString
            wordsString = "".join(words)

            # print(urlString)
            # Removing punctuations like @# etc
            wordsString = wordsString.translate(
                str.maketrans('', '', string.punctuation))

            # converting the String into List using split at space

            wordsList = wordsString.split()
            # print(wordsList)

            #  Optimized to O(n)
            # One document is traversed
            docID += 1

            # traversing each word in wordList to assign them wordIDs along with checking any repeatation

            for w in range(len(wordsList)):
                indexes = []

                wordID = 0
                if not(wordsList[w].lower() in stop_words) and wordsList[w].isalpha():
                    # print(w)
                    # If the word is not a stop word
                    # Stemming of the word
                    stemmed_word = ss.stem(wordsList[w])
                    string_encode = stemmed_word.encode("ascii", "ignore")

                    # Removing the uniCode
                    string_decode = string_encode.decode()
                    # Checking if the word is already in lexicon or not

                    if string_decode == ss.stem(wordsList[w]):

                        indexes.append(w)

                    # print(type(previousData[string_decode]))
                    if string_decode in previousData:
                        wordID = previousData[string_decode]
                        if wordID in innerDict:

                            # Error here have to apply else for new words
                            # print(wordID)
                            array = list(innerDict[wordID])
                            # print(array)
                            array.append(w)
                            # hits= len(array)
                            # print(array)
                            innerDict[wordID] = array
                        else:
                            innerDict.__setitem__(
                                previousData[string_decode], indexes)

                    # if tokenID in previousForwardData.keys():
                    #     print(w)

                    if string_decode not in previousData and string_decode not in stop_words:
                        previousData[string_decode] = tokenID
                    # if previousData[string_decode] not in previousForwardData[docID]:
                        innerDict.__setitem__(tokenID, indexes)
                        previousForwardData.__setitem__(docID, innerDict)

                        tokenID += 1


#the following lines generate inverted index and also sotres indexes of that wordID with their docID
#in the format {wordID1: {docID1: [index1, index2], {docID2: [index3, index4]}}}
invertedIndex = {}
#we traverse all docIDs from previousForwardData as previousForwardData now contains the complete forward index with word indexes
for docID in previousForwardData:
    for wordID in previousForwardData[docID]:
        if str(wordID) not in invertedIndex:
            invertedIndex[str(wordID)] = {}
        invertedIndex[str(wordID)][str(docID)] = previousForwardData[docID][wordID]


# writing lexicon, forward index, reverseIndex to their respective opened files in json format
json.dump(previousData, lexiconFile)
json.dump(previousForwardData, forwardIndexFile)
json.dump(invertedIndex, reverseIndexFile)


# closing files
lexiconFile.close()
reverseIndexFile.close()
# forwardIndexFile.close()

# noting end time
end = time.time()
# Time taken by the program
print((end - start) / 60, "minutes")
