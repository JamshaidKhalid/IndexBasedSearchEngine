import json
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
import time
from operator import itemgetter
from nltk.corpus import stopwords
ss = SnowballStemmer("english")
stop_words = set(stopwords.words("english"))

lexiconFile = open("lexicon.json", "r")
reverseIndexFile = open("reverseIndex.json", "r")
metaDataFile = open("metaData.json","r")
titleLexiconFile = open("titleLex.json", "r")
titleReverseIndexFile = open("titleRevIndex.json", "r")

lexFileData= json.load(lexiconFile)



invertedFileData= json.load(reverseIndexFile)
titlelexFileData= json.load(titleLexiconFile)



titleinvertedFileData= json.load(titleReverseIndexFile)
# print(titlelexFileData)
# print(titleinvertedFileData)  
metaData = json.load(metaDataFile)



def singleWordSearch(searchInput):
 try:
   docs=[]
   docs1=[]
   #  if the word exist in our data then show the docs
   searchQuery= ss.stem(searchInput)

   start=time.time()
   if searchQuery in titlelexFileData:
    #  if the word is in title
       wordID1=0
       wordID1= titlelexFileData[searchQuery]
      #  print(searchQuery)
       numberOfDocuments1=titleinvertedFileData[str(wordID1)]
       docs1=OrderedDict(sorted(numberOfDocuments1.items(), key=lambda item: len(item[1]), reverse=True))
       data1 = {}
       for i in docs1:
      
        dataArray1=(metaData[str(i)])
        data1[dataArray1[0]]= dataArray1[1]

       return data1
       
     
     
   if searchQuery in lexFileData:
    #  if the word is in content
      wordID=0

      wordID = lexFileData[searchQuery]


      numberOfDocuments=invertedFileData[str(wordID)]
      docs = OrderedDict(sorted(numberOfDocuments.items(), key=lambda item: len(item[1]), reverse=True))
      # print(docs)
      # print(docs1)


      data = {}
      for i in docs:
        if i not in docs1:
          # The document shouldn't be first printed
         dataArray=(metaData[str(i)])
        data[dataArray[0]]= dataArray[1]

    #   print(data)
      return data

 except:
   #  Else show that the words didn't exist in our data
    print("The word didn't exist in our data")
def scoreGenerator(hitlists):
  # print(hitlists)
  return len(hitlists)

    


def multiWordSearch(search):
  try:
      docList=[]
      for i in search:
        if i in titlelexFileData:
          
        # if the word didn't find in lexicon then it would show the exception
          search_word_ids1 = [titlelexFileData[word] for word in search if ((word not in stop_words))]
          # Having the word Id's from lexicon of the word entered by user
          inverted_index_entries = [titleinvertedFileData[str(word_id)] for word_id in search_word_ids1 if word_id != -1]
          # Having the indexes and docs from inverted Index
          
          return searchResult(inverted_index_entries, docList)
          
          

      for i in search:
        
        if i in lexFileData:
         
        
         # if the word didn't find in lexicon then it would show the exception
         search_word_ids = [lexFileData[word] for word in search if ((word not in stop_words))]
         # Having the word Id's from lexicon of the word entered by user
         inverted_index_entries = [invertedFileData[str(word_id)] for word_id in search_word_ids if word_id != -1]
         # Having the indexes and docs from inverted Index
         
         return searchResult(inverted_index_entries, docList)

  except:
      print("The word is not in our data set!")


def searchResult(inverted_index_entries, docList):
         docs_with_score = []
         # iie is for inverted index entries (IIE)
         for i, iie in enumerate(inverted_index_entries):
           # Looping the inverted index enteries
           for doc in iie:
             # Traversing the docs in dictionary as it will have the format {docID:[indexes]}
 
             current_doc_hitlists = [iie[doc]]
             
             # having the indexes of current document in the loop in current doc hitlist
           
             for remaining_iie in inverted_index_entries[i + 1:]:
               # for the next document to check the gap between words
               if doc in remaining_iie:
                 # if the doc is in in the remaining inverted index entries
                 current_doc_hitlists.append(remaining_iie[doc])
                 # so append the hilist with that index of the next doc
                 del remaining_iie[doc]
                 # and delete the doc value so that we are done with that doc
             docs_with_score.append((doc,scoreGenerator(current_doc_hitlists)))
           
             # if the two words are in the same doc it will append the indexes of two docs in one list
             # Appending score with that doc so that we can make sure the search quality
         sorted(docs_with_score, key=lambda x: x[1])
         docs_with_score.sort(key=lambda x: x[1], reverse=True)
         # Sorting it on the base of the score(descending order)
         
        # print(docs_with_score1)
         data = {}
         for i in docs_with_score:
          # print(docs_with_score1)
          
          if i[0] not in docList:
          #  print(i)
           dataArray=(metaData[str(i[0])])
           data[dataArray[0]]= dataArray[1]

         return data

def search(searchInput):
  
  searchInput=searchInput.lower()
  # Converting the word into lower case alphabets
  search= searchInput.split()
  # Splittting the word so that it would be easy to go for mulit and single word approach
  for s in range(len(search)):
    search[s]=ss.stem(search[s])
    # Converting all the words in their stemmed form to process in multiword Query
  
  
  if(len(search)>  1):
  
        result = multiWordSearch(search)
        return result
          
     # Multiword Search Query will be if it is greater than length 1
  else:
     # Else it will be a single word
        result = singleWordSearch(searchInput)
        return result
