import json
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
from operator import itemgetter


ss = SnowballStemmer("english")

lexiconFile = open("lexicon.json", "r")
forwardIndexFile = open("forwardIndex.json", "r")
reverseIndexFile = open("reverseIndex.json", "r")
metaDataFile = open("metaData.json","r")

search= input("Enter the word to search in document\n")
searchQuery= ss.stem(search)

# print(searchQuery)

lexFileData= json.load(lexiconFile)

forwardFileData= json.load(forwardIndexFile)

invertedFileData= json.load(reverseIndexFile)

metaData = json.load(metaDataFile)
wordID=0
dataDict={}
hitListDict={}

try:
   wordID = lexFileData[searchQuery]
   numberOfDocuments=invertedFileData[str(wordID)]
# print(numberOfDocuments)
   for i in numberOfDocuments:
    try:
      dataDict= forwardFileData[str(i)]
      # print(dataDict)
      indexes=dataDict[str(wordID)]
      # print(indexes)
      # print(len(indexes))
      hitListDict.__setitem__(i,len(indexes))
    except:
         pass
   sorted_dict= OrderedDict (sorted(hitListDict.items(), key=lambda x: x[1], reverse=True))


# print(sorted_dict) 
   dataArray=[]
   for i in (sorted_dict):
    print(i)
    dataArray=(metaData[str(i)])
    print("Title")
    print(dataArray[0])
    print("URL")
    print(dataArray[1])
except:
   print("The word you entered didn't exist in the data")
# print(wordID)
