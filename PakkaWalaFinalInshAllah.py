import os
import json
import string
from sys import path
import unicodedata
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.util import pr

path = "D:\Programming\Search Engine Project\\nela-elections-2020\\newsdata"

tokenID = 0
docId = 0
allWordList = []


def read_text_file(file_path):
    lemma = WordNetLemmatizer()
    ps = PorterStemmer()
    ss = SnowballStemmer("english")
    # using SnowBall stemmer for better control
    # Removing the stopword
    stop_words = set(stopwords.words('english'))
    f = open(file_path, 'r')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    for i in data:
        global docId
        docId += 1
        if docId > 100000:
            break
        list1 = []
        for j in i['content']:
            list1.append(j)
            list2String = "".join(list1)

        # list1 = list(set(list1))
        # print(list2String)
        list1String = unicodedata.normalize(
            'NFKD', list2String).encode('ASCII', 'ignore')
        words = word_tokenize(list1String.decode())
        # Tokenizing the whole string

        filtered_sentence = [
            w for w in words if not w.lower() in stop_words]

        # filtered_sentence = []

        # for w in words:
        #     if not w in stop_words:
        #         filtered_sentence.append(w)

        # print(words)
        # print(filtered_sentence)
        stemmed = []
        # For stemming of the list
        for token in filtered_sentence:
            stemmed_word = lemma.lemmatize(token)
            stemmed.append(stemmed_word)

        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
        stemmed = [''.join(c for c in s if c not in punctuations)
                   for s in stemmed]
        stemmed = [s for s in stemmed if s]

        # punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~0123456789'''
        # finalString = ""
        # for char in stemmed:
        #     if char not in punctuations:
        #         finalString = finalString + char

        # listFirst = list(finalString.split(" "))
        # listFirst = list(set(listFirst))

        # print(stemmed)

        # Removing the duplicates if any in the string

        final = list(dict.fromkeys(stemmed))
        # print(final)
        # print(allWordList)

        ourDict = {}
        global allWordList

        textfile = open("lexicon.json", "a+")
        global tokenID
        for element in final:
            if element not in allWordList:
                ourDict.__setitem__(element, tokenID)
                tokenID += 1

        allWordList.extend(final)

        j = json.dumps(ourDict, indent=4)
        textfile.write(j)
        print(docId)
        textfile.close()
        # Closing file
    print(file_path)
    f.close()


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(path, file)
            read_text_file(file_path)
