from titleGen import *
import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os
import time
import string


# noting starting time
start = time.time()
stemmed = " "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''

# stopwords to remove
stop_words = stopwords.words('english')
newStopWords = ['a', 'b', 'c', 'd', 'e', '', 'f', 'g', 'h', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
stop_words.extend(newStopWords)

# Using SnowBall stemmer to stem words like programming to 'program'
ss = SnowballStemmer("english")

# PLEASE
# Locate dataset folder and this program in the same directory and use the path in following form
directory = 'DataSet'
# OR ENTER THE PATH OF DATASET in following form WHILE TESTING THIS PROGRAM.
# directory = 'D:\\DSA Project\\main\\testDataSet'


# initializing the the datastructures used in generation
wordsList = []
wordsString = ""
previousData = {}
parsedData = {}


# tokenID assigns the wordID and docID assigns the docID
# and fileId is saved in files.json file along with file name.
# it is used to check if a file is already parsed or not. Useful in uploading new content.
fileId = 0
docID = 0
tokenID = 0

# Initializing it in defaultDictList so that in JSON we can have the format 0:[]
# it will initialize {key:[]}
previousForwardData = defaultdict(list)
previousReverseData = defaultdict(list)
metaData = defaultdict(list)

# Writing files in w mode
lexiconFile = open("lexicon.json", "w")
forwardIndexFile = open("forwardIndex.json", "w")
invertedIndexFile = open("reverseIndex.json", "w")
metaDataFile = open("metaData.json", "w")
lexiconedFile = open("files.json", "w")


# Checking the whole directory
for root, dirs, files in os.walk(directory):
    # parsing all the files in it
    for filename in files:

        # each time the loop runs, currentFile will have the complete path and name of the file for every next iteration
        currentFile = (os.path.join(root, filename))
        print(docID)
        print((currentFile))
        # opening currentFile as f, currentFile has the path of file
        f = open(currentFile)

        # Now, Data has the text of whole json file in form of Dictionary
        data = json.load(f)

        # traversing data as json is now loaded in data as dictionary
        for i in range(len(data)):
            '''in forward index, we used multilevel dictionary. i.e dictionary within a dictionary.
                in the form of:
                {docID1: {wordID1: [index1, index2, index3, ...], wordID2: [index1...]}, doctID2: {wordID4:[index1]}, ....}'''
            # and here inner dict work is the innerdictionary of word id as key and a list of that word's indexes.
            # each time the loop runs, inner dict is emptied and it stores the data of next word.
            innerDict = {}

            # data has the all the documents of one json file but we want to parse one document at one time
            # to generate word IDs and docIDs. So we traverse data[i] which actually gives us only one document of
            # currently running file and through this approach, we can iterate through all documents of a json file.
            dataDict = data[i]
            # parsing the CONTENT only to form the lexicon

            # So now, from the data of one document, we need only content for lexicon, forward and inverted index.
            # and title, url to store metaInfo of that document.
            words = dataDict['content']
            title = dataDict['title']
            url = dataDict['url']
            # now WORDS has all the text of content of json and same for title and url.
            # we will join words at spaces to form wordsString and same for title and url.
            wordsString = "".join(words)
            titleString = "".join(title)
            urlString = "".join(url)

            # Removing punctuations like @# etc
            wordsString = wordsString.translate(
                str.maketrans('', '', string.punctuation))
            metaDataList = [titleString, urlString]

            # converting the String into List using split at space
            wordsList = wordsString.split()
            # One document is traversed
            docID += 1
            metaData.__setitem__(docID, metaDataList)
            # traversing each word in wordList to assign them wordIDs along with checking any repeatation
            for w in range(len(wordsList)):
                # index list stores the indexes of word in particular file. It is the way to store hitlists.
                indexes = []

                # this wordID is not what is written in lexicon, in lexicon, tokenID is used.
                # it is used only within the loop
                wordID = 0
                if not(wordsList[w].lower() in stop_words) and wordsList[w].isalpha():
                    # If the word is not a stop word and word is an alphabet, means it is not a number of symbol
                    # Stemming of the word
                    stemmed_word = ss.stem(wordsList[w])
                    string_encode = stemmed_word.encode("ascii", "ignore")
                    # Removing the uniCode
                    string_decode = string_encode.decode()

                    # Checking if the word is already in lexicon or not
                    if string_decode == ss.stem(wordsList[w]):
                        indexes.append(w)
                    if string_decode in previousData:
                        wordID = previousData[string_decode]
                        if wordID in innerDict:
                            array = list(innerDict[wordID])
                            array.append(w)
                            innerDict[wordID] = array
                        else:
                            innerDict.__setitem__(
                                previousData[string_decode], indexes)
                
                    if string_decode not in previousData and string_decode not in stop_words:
                        previousData[string_decode] = tokenID
                        innerDict.__setitem__(tokenID, indexes)
                        previousForwardData.__setitem__(docID, innerDict)
                        tokenID += 1
        # when a json file is traversed, no matter how manny documents, fileID is incremented.
        fileId += 1
        parsedData.__setitem__(filename, fileId)
# The above lines traverse files in the given path and generate lexicon and
# forward Index with the indexes of corresponding wordIDs in their docIDS with minimum time complexity.


# the following lines generate inverted index and also sotres indexes of that wordID with their docID
# in the format {wordID1: {docID1: [index1, index2], {docID2: [index3, index4]}}}
invertedIndex = {}
# we traverse all docIDs from previousForwardData as previousForwardData now contains the complete forward index with word indexes
for docID in previousForwardData:
    for wordID in previousForwardData[docID]:
        if str(wordID) not in invertedIndex:
            invertedIndex[str(wordID)] = {}
        invertedIndex[str(wordID)][str(
            docID)] = previousForwardData[docID][wordID]


# writing lexicon, forward index, invertedIndex to their respective opened files in json format
json.dump(previousData, lexiconFile)
json.dump(previousForwardData, forwardIndexFile)
json.dump(invertedIndex, invertedIndexFile)
json.dump(metaData, metaDataFile)
json.dump(parsedData, lexiconedFile)
# closing files
lexiconFile.close()
invertedIndexFile.close()
forwardIndexFile.close()
metaDataFile.close()
lexiconedFile.close()
# noting end time
end = time.time()
# Time taken by the program
print((end - start) / 60, "minutes")
