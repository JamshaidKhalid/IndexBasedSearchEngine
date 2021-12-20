import json
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict
import os
import time
import string

#noting starting time
start = time.time()
stemmed = " "
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''

# PLEASE 
# Locate dataset folder and this program in the same directory and use the path in following form
directory = 'DataSet'
#OR ENTER THE PATH OF DATASET in following form WHILE TESTING THIS PROGRAM.
# directory = 'D:\\DSA Project\\main\\testDataSet'

# Using SnowBall stemmer to stem words like programming to 'program'
ss = SnowballStemmer("english")

#initializing the list
wordsList = []
wordsString = ""

# Dictionary intilaizaiton
previousData = {}

# Initializing it in defaultDictList so that in JSON we can have the format 0:[]
previousReverseData = defaultdict(list)
previousForwardData = defaultdict(list)


# Writing files in w mode later will change it to append mode
lexiconFile = open("lexicon.json", "w")
forwardIndexFile = open("forwardIndex.json", "w")
reverseIndexFile = open("reverseIndex.json", "w")

#tokenID assigns the wordID and docID assigns the docID
docID = 0
tokenID = 0

# stopwords to remove
stop_words = stopwords.words('english')
newStopWords = ['a','b','c','d','e','','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
stop_words.extend(newStopWords)
# Checking the whole directory
for root, dirs, files in os.walk(directory):
    # parsing all the files in it
    for filename in files:
        #each time the loop runs, currentFile will have the complete path and name of each next file
        currentFile = (os.path.join(root, filename))
        print(docID)
        print((currentFile))


        # opening currentFile as f, currentFile has the path of file
        f = open(currentFile)

        # Now, Data has the text of whole json file in form of Dictionary
        data = json.load(f)

        # traversing data as json is now loaded in data as dictionary
        for i in range(len(data)):
            
            innerDict={}
            list1 = data[i]
            # parsing the CONTENT only to form the lexicon
            words = list1['content']
            #now WORDS has all the text of content of json.

            #we will join words at spaces to form wordsString
            wordsString = "".join(words)
            # Removing punctuations like @# etc
            wordsString = wordsString.translate(str.maketrans('', '', string.punctuation))


            # converting the String into List using split at space

            wordsList = wordsString.split()
            # print(wordsList)

            #  Optimized to O(n)
            # One document is traversed
            docID += 1


            #traversing each word in wordList to assign them wordIDs along with checking any repeatation
            for w in range(len(wordsList)):
                indexes = []
                if not(wordsList[w].lower()  in stop_words) and wordsList[w].isalpha():
                    # print(w)
                    # If the word is not a stop word
                    # Stemming of the word
                    stemmed_word = ss.stem(wordsList[w])
                    string_encode = stemmed_word.encode("ascii", "ignore")
                    
                    # Removing the uniCode
                    string_decode = string_encode.decode()
                    # Checking if the word is already in lexicon or not
                 
                    if(string_decode==ss.stem(wordsList[w])):
                        
                    # print(wordsList[w])
                        indexes.append(w)

                    
                    if string_decode not in previousData and string_decode not in stop_words:
                        previousData[string_decode] = tokenID
                        # Incrementing the WordID
                        # print(1)
                        
                        # print(type(previousData[string_decode]))

                    # If the string is in already in the dictionary
                 
                    
                    innerDict.__setitem__(tokenID, indexes)
                    # try:

                    # if previousData[string_decode]  in innerDict.keys():
                    previousForwardData.__setitem__(docID, innerDict)
                    tokenID += 1
                    # except:
                    #     print("something went wrong")
                        # if previousData[string_decode] not in previousForwardData[docID]:
                               
                        
                            # previousForwardData[docID].append(previousData[string_decode])
                    if (string_decode in previousData):
                        
                     
                        previousReverseData[previousData[string_decode]].append(docID)
                    
                

for i in indexes:
    print(indexes)
# Removing duplicates from invertedIndex
for i in previousReverseData:
    previousReverseData[i] = list(dict.fromkeys(previousReverseData[i]))


#writing lexicon, forward index, reverseIndex to their respective opened files in json format
json.dump(previousData, lexiconFile)
json.dump(previousForwardData, forwardIndexFile)
json.dump(previousReverseData, reverseIndexFile)

#closing files
lexiconFile.close()
reverseIndexFile.close()
forwardIndexFile.close()

#noting end time
end = time.time()
# Time taken by the program
print((end - start) / 60, "minutes")
