import json
import nltk
import unicodedata
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords



#tokenization start from here

ps = PorterStemmer()
list1=[]
# Removing the stopword 
stop_words = set(stopwords.words('english'))
f = open('dataSet.json') 
# Loading the JSON File 

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
for i in data['content']:
    #adding character into the lists
    list1.append(i)
    
list2String = "".join(list1)
#joining the characters to form words
print(list2String)
#For Unicode Characters
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
     stemmed_word = ps.stem(token)
     stemmed.append(stemmed_word)

print(stemmed)


#Removing the duplicates if any in the string

final = list(dict.fromkeys(stemmed))
print(final)

textfile = open("lexicon.json", "w")
tokenID=0
textfile.write("{")
for element in final:

    textfile.write('{0}{1}{2}{3}{4}{5}{6}{7}\n'.format("\"",tokenID,"\"",":","\"",element,"\"",","))
    tokenID+=1
textfile.write("}")
textfile.close()
# Closing file
f.close()