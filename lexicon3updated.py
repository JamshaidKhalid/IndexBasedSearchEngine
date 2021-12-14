import json
import re
import nltk
import unicodedata
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.util import pr
from collections import defaultdict
import os
import time

start = time.time()
count = [0]

#tokenization start from here
tokenID=0
docID=0
stemmed=" "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
directory = 'DataSet'
ss=SnowballStemmer("english")

wordsList = []
previousData={}
seen = set()

previousReverseData=defaultdict(list)
previousForwardData=defaultdict(list)
lexiconFile = open("lexicon.json","w")
forwardIndexFile = open("forwardIndex.json","w")
reverseIndexFile = open("reverseIndex.json","w")
docID=0
tokenID=0
for root, dirs, files in os.walk(directory):


    for filename in files:
        currentFile =(os.path.join(root, filename))
          
        print((currentFile))
       
        stop_words = set(stopwords.words('english'))
        f = open(currentFile) 
        data = json.load(f)
        for i in range(len(data)):
       
        

         list1 = data[i]
         letters = list1['content']
         wordsString = "".join(letters)
         wordsList = wordsString.split()
        #  Optimized to O(n) 
         docID+=1
         
         for w in wordsList:
            if ((w not in stop_words) and (w not in  punctuations)):
                stemmed_word = ss.stem(w)
                string_encode = stemmed_word.encode("ascii", "ignore")
                string_decode = string_encode.decode()
                # Removing the uniCode
                if string_decode not in previousData:
                  # Checking for the words 
                  previousData[string_decode]=tokenID
                  tokenID+=1
                  # print(type(previousData[string_decode]))
                
                if (string_decode in previousData):
                    # count[previousData[string_decode]] += 1
                    if previousData[string_decode] not in previousForwardData[docID]:
                     previousForwardData[docID].append(previousData[string_decode])
                if (string_decode in previousData):
                            previousReverseData[previousData[string_decode]].append(docID)

for i in previousReverseData:   
 previousReverseData[i]  = list(dict.fromkeys(previousReverseData[i]))                


json.dump(previousData,lexiconFile)
json.dump(previousForwardData,forwardIndexFile)
json.dump(previousReverseData,reverseIndexFile)
lexiconFile.close()
reverseIndexFile.close()
forwardIndexFile.close()
end = time.time()
print((end-start)/60)
