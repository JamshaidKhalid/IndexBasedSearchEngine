import json
import re
import nltk
import unicodedata
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.util import pr
from collections import defaultdict
import os
import time
import string


start = time.time()
tokenID = 0
docID = 0
stemmed = " "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
directory = 'dummyDataSet'
ss = SnowballStemmer("english")
# Using SnowBall stemmer to stem words like programming to 'program'

wordsList = []
previousData = {}
# Dictionary intilaizaiton
seen = set()

previousReverseData = defaultdict(list)
# Initializing it in defaultDictList so that in JSON we can have the format 0:[]
previousForwardData = defaultdict(list)
lexiconFile = open("lexicon.json", "w")
forwardIndexFile = open("forwardIndex.json", "w")
reverseIndexFile = open("reverseIndex.json", "w")
# Writing files in w mode later will change it to append mode
docID = 0
tokenID = 0
for root, dirs, files in os.walk(directory):
    # Checking the whole director
    for filename in files:
        # parsing all the files in it
        currentFile = (os.path.join(root, filename))

        print((currentFile))

        stop_words = set(stopwords.words('english'))
        # Removing stop words
        f = open(currentFile)
        data = json.load(f)
        # Data have the content of whole file in form of Dictionary

        for i in range(len(data)):

            list1 = data[i]
            letters = list1['content']
            # parsing the content only to form the lexicon
            wordsString = "".join(letters)
            wordsString = wordsString.translate(str.maketrans('', '', string.punctuation))
            # Removing punctuations like @# etc
            wordsList = wordsString.split()

            #  Optimized to O(n)
            docID += 1
            # One document is traversed

            for w in wordsList:
                if ((w not in stop_words)):
                    # If the word is not a stop word
                    stemmed_word = ss.stem(w)
                    # Stemming of the word
                    string_encode = stemmed_word.encode("ascii", "ignore")
                    
                    string_decode = string_encode.decode()
                    # Removing the uniCode
                    if string_decode not in previousData:
                        # Checking for the words
                        previousData[string_decode] = tokenID
                        tokenID += 1
                        # Incrementing the WordID
                        # print(type(previousData[string_decode]))

                    if (string_decode in previousData):
                        # If the string is in already in the dictionary
                        # count[previousData[string_decode]] += 1
                        if previousData[string_decode] not in previousForwardData[docID]:
                            # The format will be like docID:[wordID,wordID]
                            # We will add hitlist and indexes later on in forward index
                            # not to have the forward index again repeated
                            previousForwardData[docID].append(previousData[string_decode])
                    if (string_decode in previousData):
                        # For Reverse Index
                        # The format will be like wordID:[docID,docID]
                        previousReverseData[previousData[string_decode]].append(docID)

for i in previousReverseData:
    # Removing duplicates from invertedIndex
    previousReverseData[i] = list(dict.fromkeys(previousReverseData[i]))

json.dump(previousData, lexiconFile)
json.dump(previousForwardData, forwardIndexFile)
json.dump(previousReverseData, reverseIndexFile)
lexiconFile.close()
reverseIndexFile.close()
forwardIndexFile.close()
end = time.time()
# Time taken by the program
# Writing and closing the files
print((end - start) / 60)
