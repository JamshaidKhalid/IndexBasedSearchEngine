import os
import json
import nltk
import unicodedata
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

stop_words = set(stopwords.words('english'))
tokenID= 0

def Stemming(list2String):
        list1String = unicodedata.normalize('NFKD', list2String).encode('ASCII', 'ignore')
        words = word_tokenize(list1String.decode())
        #Tokenizing the whole string
        filtered_sentence = [w for w in words if not w.lower() in stop_words]


        filtered_sentence = []

        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)


        print(words)
        print(filtered_sentence)
        stemmed=" "
        #For stemming of the list
        for token in filtered_sentence:
             stemmed_word = ss.stem(token)
             stemmed+=(stemmed_word)+ " "


        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
        finalString = ""
        for char in stemmed:
                  if char not in punctuations:
                   finalString= finalString + char

        listFirst = list(finalString.split(" "))
        listFirst = list(set(listFirst))

        return listFirst


directory = 'dummydata'


#tokenization start from here
list2String = ""
ps = PorterStemmer()
ss=SnowballStemmer("english")
#using SnowBall stemmer for better control
list1=[]
for root, dirs, files in os.walk(directory):
    docID=0
    tokenID=0
    
    for filename in files:
        currentFile =(os.path.join(root, filename))
        print(docID)
        print((currentFile))
        f = open(currentFile)
        data = json.load(f)
        for i in data:
            for j in i['content']:
                list1.append(j)

                list2String = "".join(list1)
        
stemmedString = Stemming(list2String)

# print(stemmedString)
# with open('sample.txt', 'w') as f:
#     f.write(str(stemmedString))
#     f.close()
        


dict={}
# dict = previousData
for element in stemmedString:
  dict.__setitem__(element,tokenID)
  tokenID+=1




# print(dict
j = json.dumps(dict)
with open('lex.json','w') as f:
  f.write(j)
  f.close()
