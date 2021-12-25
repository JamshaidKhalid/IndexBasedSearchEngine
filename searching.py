import json
from nltk.stem.snowball import SnowballStemmer
from collections import OrderedDict
import time
from operator import itemgetter
from nltk.corpus import stopwords

def singleWordSearch(searchInput):
 try:
   #  if the word exist in our data then show the docs
   searchQuery= ss.stem(searchInput)

   start=time.time()
   
   wordID=0
   dataDict={}
   hitListDict={}
   wordID = lexFileData[searchQuery]
   numberOfDocuments=invertedFileData[str(wordID)]
   docs = OrderedDict(sorted(numberOfDocuments.items(), key=lambda item: len(item[1]), reverse=True))

   for i in docs:
      
      dataArray=(metaData[str(i)])
      print("Title")
      print(dataArray[0])
      print("URL")
      print(dataArray[1])
   end = time.time()
   print(end-start)

 except:
   #  Else show that the words didn't exist in our data
    print("The word didn't exist in our data")

def scoreGenerator(hitlists):
  # Function for generating score having the args of indexes

		score = 0

		n = len(hitlists)
    
    # n will have the lenght of array like if i entered a word chill life
    # if both are in same document in hitlists it will be like[[chilll's indexes],[life's indexes]]
    # and n will have the length 2 
		hitlist_lens = [len(hitlist) for hitlist in hitlists]
    # now fetching the length of one word like chill
		hitlist_is = [0] * n
    # initalizing the 2D array with the n

		joined_hits = []

		while hitlist_is != hitlist_lens:
      # Terminating condtion
			terminal_positions = []
			taken_from = []

			for i in range(n):
				if hitlist_is[i] == len(hitlists[i]): continue
				terminal_positions.append(hitlists[i][hitlist_is[i]])
				taken_from.append(i)

			minimum = min(terminal_positions)
			minimum_index = terminal_positions.index(minimum)
			hitlist_is[taken_from[minimum_index]] += 1

			joined_hits.append((minimum_index, minimum))

		prev_hit = joined_hits[0]

		for hit in joined_hits[1:]:
			score += 1
			if hit[0] != prev_hit[0]: 
				dist = hit[1] - prev_hit[1]
				score += 100 / (dist + 1)
			prev_hit = hit

		return score

ss = SnowballStemmer("english")
stop_words = set(stopwords.words("english"))

lexiconFile = open("lex.json", "r")
# forwardIndexFile = open("forwardIndex.json", "r")
reverseIndexFile = open("invIndex.json", "r")
metaDataFile = open("metaInfo.json","r")
lexFileData= json.load(lexiconFile)

# forwardFileData= json.load(forwardIndexFile)

invertedFileData= json.load(reverseIndexFile)

metaData = json.load(metaDataFile)
innerDict = {}
docList=[]
searchInput= input("Enter the word to search in document\n")
searchInput=searchInput.lower()
# Converting the word into lower case alphabets
search= searchInput.split()
# Splittting the word so that it would be easy to go for mulit and single word approach
for s in range(len(search)):
  search[s]=ss.stem(search[s])
  # Converting all the words in their stemmed form to process in multiword Query


if(len(search)>  1):
      try:
        # if the word didn't find in lexicon then it would show the exception
        search_word_ids = [lexFileData[word] for word in search if ((word not in stop_words))]
        # Having the word Id's from lexicon of the word entered by user
        inverted_index_entries = [invertedFileData[str(word_id)] for word_id in search_word_ids if word_id != -1]
        # Having the indexes and docs from inverted Index
        
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
        
        # print(docs_with_score)
        for i in docs_with_score:

          dataArray=(metaData[str(i[0])])
          print("Title")
          print(dataArray[0])
          print("URL")
          print(dataArray[1])
      except:
        print("The word didn't exist in our data")
		    

       


         
         
       
   # Multiword Search Query will be if it is greater than length 1
else:
   # Else it will be a single word
   singleWordSearch(searchInput)
