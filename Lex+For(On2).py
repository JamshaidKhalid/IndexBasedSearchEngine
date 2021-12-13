import json
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

#tokenization start from here
tokenID=0
docID=0
stemmed=" "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
directory = 'dummydata'
ss=SnowballStemmer("english")
list1=[]
previousData={}
# https://www.geeksforgeeks.org/python-initializing-dictionary-with-empty-lists/
# Initlaizing the dictionary in list format so that we can have the format 0:[]

previousForwardData=defaultdict(list)
lexiconFile = open("lexicon.json","w")
forwardIndexFile = open("forwardIndex.json","w")

list2 = []
docID=0
tokenID=0
for root, dirs, files in os.walk(directory):


    for filename in files:
        currentFile =(os.path.join(root, filename))
          
        print((currentFile))
        print(docID)
        stop_words = set(stopwords.words('english'))
        f = open(currentFile) 
        list1=[]
        data = json.load(f)
        for i in data:
          for j in i['content']:
            list1.append(j)

            list2String = "".join(list1)

            list2 = list2String.split()
        docID+=1
         
        for w in list2:
            if w not in stop_words:
              if w not in  punctuations:
                stemmed_word = ss.stem(w)
                string_encode = stemmed_word.encode("ascii", "ignore")
                string_decode = string_encode.decode()
                

                # filtered_sentence.append(stemmed_word)
                if string_decode not in previousData:
                  previousData[string_decode]=tokenID
                  tokenID+=1
                if string_decode in previousData:
                  previousForwardData[docID].append(previousData[string_decode])
                  


json.dump(previousData,lexiconFile)
json.dump(previousForwardData,forwardIndexFile)
lexiconFile.close()
forwardIndexFile.close()
end = time.time()
print(end-start)
