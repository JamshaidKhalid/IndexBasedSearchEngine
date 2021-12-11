import os
import json
import nltk
import unicodedata
from nltk import text
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from pathlib import Path

 
# assign directory
directory = 'dummyDataSet'
 
# iterate over files in
# that directory

for root, dirs, files in os.walk(directory):
    docID=0
    tokenID=0
    
    for filename in files:
        currentFile =(os.path.join(root, filename))
        print(docID)
        print((currentFile))
        ps = PorterStemmer()
        ss=SnowballStemmer("english")
#using SnowBall stemmer for better control
        list1=[]
# Removing the stopword 
        stop_words = set(stopwords.words('english'))
        f = open(currentFile)
        # returns JSON object as
        # a dictionary
        list1=[]
        data = json.load(f)
        for i in data:
          for j in i['content']:
            list1.append(j)
    
            list2String = "".join(list1)

        # print(list2String)  
        list1String = unicodedata.normalize('NFKD', list2String).encode('ASCII', 'ignore')
        words = word_tokenize(list1String.decode())
        #Tokenizing the whole string
        filtered_sentence = [w for w in words if not w.lower() in stop_words]

 
        filtered_sentence = []
 
        for w in words:
          if w not in stop_words:
            filtered_sentence.append(w)


        # print(words)
        # print(filtered_sentence)
        stemmed=""
#For stemming of the list
        for token in filtered_sentence:
         stemmed_word = ss.stem(token)
         stemmed+=(stemmed_word)+ " "

        #  print(stemmed)

        # stemmed = stemmed.translate()
#Removing the duplicates if any in the string
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~123456789'''
        finalString = ""
        for char in stemmed:
          if char not in punctuations:
           finalString = finalString + char
        final = list(dict.fromkeys(stemmed))
        print(finalString)
        #Remove repeated Words

        textfile = open("forwardIndex.txt", "a")
        
        
        # print("Hello Ahmed")
        textfile.write(str(docID))
        textfile.write(":")
        textfile.write("[")
        length= len(final)
        lexiconFile = open("lexicon.txt", "a")

      
        count=0
        
        for element in final:
           count+=1
           if(count!=length):
            
            textfile.write('{0}{1}'.format(tokenID,","))
            lexiconFile.write('{0}{1}{2}{3}{4}{5}\n'.format("\"",element,"\"",":",tokenID,","))
          
            tokenID+=1
           else:
             textfile.write('{0}'.format(tokenID))
             lexiconFile.write('{0}{1}{2}{3}{4}{5}{6}\n'.format("\"",element,"\"",":","\"",tokenID,"\"",))
             tokenID+=1
      
        textfile.write("]") 
        textfile.write(",")
      
      
        textfile.write("\n") 
        print(docID)
        
        
        # Closing file
        f.close()
        
        docID+=1

textfile.close()
with open("forwardIndex.txt",'r+') as f:
  txt = Path('forwardIndex.txt').read_text()
  data = txt.replace('\n', '')

  
  if (not(data.startswith('{'))):

    lines=f.readlines()

    # Gets the column
    column=0

    # Gets the line
    line=0

    # Gets the word
    word='{'

    lines[line]=lines[line][0:column]+word+lines[line][column:]

    # Delete the file
    f.seek(0)

    for i in lines:
        # Append the lines
        f.write(i)
  
    f.close()
    
  else:
    f.close()



with open("forwardIndex.txt",'r+') as f:
  txt = Path('forwardIndex.txt').read_text()
  data = txt.replace('\n', '')

  
  if (not(data.endswith('}'))):

    lines=f.readlines()

    # Gets the column
    column=-1

    # Gets the line
    line=-1

    # Gets the word
    word='}'

    lines[line]=lines[line][0:column]+word+lines[line][column:]

    # Delete the file
    f.seek(0)

    for i in lines:
        # Append the lines
        f.write(i)
  
    f.close()
    
  else:
    f.close()


