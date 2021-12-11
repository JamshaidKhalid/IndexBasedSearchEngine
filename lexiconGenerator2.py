import json
import nltk
import unicodedata
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


#tokenization start from here

ps = PorterStemmer()
ss=SnowballStemmer("english")
#using SnowBall stemmer for better control
list1=[]
# Removing the stopword 
stop_words = set(stopwords.words('english'))
f = open('airwars.json') 
# returns JSON object as
# a dictionary
list1=[]
data = json.load(f)
for i in data:
  for j in i['content']:
    list1.append(j)
    
    list2String = "".join(list1)

print(list2String)  
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
stemmed=[]
#For stemming of the list
for token in filtered_sentence:
     stemmed_word = ss.stem(token)
     stemmed.append(stemmed_word)

print(stemmed)


#Removing the duplicates if any in the string

final = list(dict.fromkeys(stemmed))
print(final)

textfile = open("lexicon.json", "w")
tokenID=0
textfile.write("{")
for element in final:

    textfile.write('{0}{1}{2}{3}{4}{5}{6}{7}\n'.format("\"",element,"\"",":","\"",tokenID,"\"",","))
    tokenID+=1
textfile.write("}")
textfile.close()
# Closing file
f.close()


