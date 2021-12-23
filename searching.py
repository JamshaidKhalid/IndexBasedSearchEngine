import json
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
import time
from operator import itemgetter


ss = SnowballStemmer("english")

lexiconFile = open("lexicon.json", "r")
# forwardIndexFile = open("forwardIndex.json", "r")
reverseIndexFile = open("reverseIndex.json", "r")
metaDataFile = open("metaData.json","r")
lexFileData= json.load(lexiconFile)

# forwardFileData= json.load(forwardIndexFile)

invertedFileData= json.load(reverseIndexFile)

metaData = json.load(metaDataFile)

search= input("Enter the word to search in document\n")
searchQuery= ss.stem(search)
start=time.time()

wordID=0
dataDict={}
hitListDict={}
wordID = lexFileData[searchQuery]
numberOfDocuments=invertedFileData[str(wordID)]
docs = OrderedDict(sorted(numberOfDocuments.items(), key=lambda item: len(item[1]), reverse=True))
for i in docs:
   print(i)
   dataArray=(metaData[str(i)])
   print("Title")
   print(dataArray[0])
   print("URL")
   print(dataArray[1])
end = time.time()
print(end-start)
