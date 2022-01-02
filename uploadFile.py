
def upload(originalPath):
   
    import os
    import shutil
    import json
    import string
    from collections import defaultdict
    from nltk.stem.snowball import SnowballStemmer
    from nltk.corpus import stopwords
    import time

    start = time.time()

    ss = SnowballStemmer("english")
    stop_words = stopwords.words('english')
    newStopWords = ['a', 'b', 'c', 'd', 'e', '', 'f', 'g', 'h', 'j', 'k', 'l',
                    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    stop_words.extend(newStopWords)

    print(originalPath)
    targetPath = "DataSet"
    filename = os.path.basename(originalPath)
    print(filename)
    targetFilePath = os.path.join(targetPath, filename)
    print(targetFilePath)

    newPreviousData = {}
    newPreviousForwardData = defaultdict(list)
    newPreviousReverseData = defaultdict(list)
    newMetaData = defaultdict(list)
    newParsedFiles = {}

    lexiconFile = open("lexicon.json")
    forwardIndexFile = open("forwardIndex.json")
    reverseIndexFile = open("reverseIndex.json")
    metaDataFile = open("metaData.json")
    lexiconedFile = open("files.json")

    lexiconContent = json.load(lexiconFile)
    forwardIndexContent = json.load(forwardIndexFile)
    reverseIndexContent = json.load(reverseIndexFile)
    metaDataContent = json.load(metaDataFile)
    lexiconedContent = json.load(lexiconedFile)

    docID = list(forwardIndexContent.keys())[-1]
    docID = int(docID)
    docID += 1
    tokenList = list(lexiconContent.keys())[-1]
    tokenID = lexiconContent[tokenList]
    tokenID += 1
    print(docID)
    print(tokenID)
    parsedFiles = list(lexiconedContent.keys())
    fileName = list(lexiconedContent.keys())[-1]
    fileId = lexiconedContent[fileName]
    print(fileId)

    lexiconFile.close()
    reverseIndexFile.close()
    forwardIndexFile.close()
    metaDataFile.close()

    if filename not in parsedFiles:
        f = open(originalPath)
        data = json.load(f)

        for i in range(len(data)):
            innerDict = {}
            list1 = data[i]

            words = list1['content']
            title = list1['title']
            url = list1['url']

            wordsString = "".join(words)
            titleString = "".join(title)
            urlString = "".join(url)
            wordsString = wordsString.translate(
                str.maketrans('', '', string.punctuation))

            metaDataList = [titleString, urlString]
            wordsList = wordsString.split()
            docID += 1

            for w in range(len(wordsList)):
                indexes = []

                wordID = 0
                if not(wordsList[w].lower() in stop_words) and wordsList[w].isalpha():
                    stemmed_word = ss.stem(wordsList[w])
                    string_encode = stemmed_word.encode("ascii", "ignore")
                    string_decode = string_encode.decode()

                    if string_decode == ss.stem(wordsList[w]):
                        indexes.append(w)

                    if string_decode in newPreviousData:
                        wordID = newPreviousData[string_decode]
                        if wordID in innerDict:
                            array = list(innerDict[wordID])
                            array.append(w)
                            innerDict[wordID] = array
                        else:
                            innerDict.__setitem__(
                                newPreviousData[string_decode], indexes)

                    if tokenID in newPreviousForwardData.keys():
                        print(w)

                    if string_decode not in newPreviousData and string_decode not in stop_words:
                        newPreviousData[string_decode] = tokenID
                        innerDict.__setitem__(tokenID, indexes)
                        newPreviousForwardData.__setitem__(docID, innerDict)
                        newMetaData.__setitem__(docID, metaDataList)
                        tokenID += 1

        fileId += 1
        newParsedFiles.__setitem__(filename, fileId)
        lexiconedFile.close()

        Inv_index = {}
        for docID in newPreviousForwardData:
            for wordID in newPreviousForwardData[docID]:
                if str(wordID) not in Inv_index:
                    Inv_index[str(wordID)] = {}
                Inv_index[str(wordID)][str(docID)
                                       ] = newPreviousForwardData[docID][wordID]

        lexiconContent.update(newPreviousData)
        lexiconContent = dict(sorted(lexiconContent.items(), key=lambda item:(item[1]), reverse=False))
        forwardIndexContent.update(newPreviousForwardData)
        # forwardIndexContent = dict(sorted(forwardIndexContent.items(), key=lambda item:(item[1]), reverse=False))
        reverseIndexContent.update(Inv_index)
        # reverseIndexContent = dict(sorted(reverseIndexContent.items(), key=lambda item:(item[1]), reverse=False))
        metaDataContent.update(newMetaData)
        # metaDataContent = dict(sorted(metaDataContent.items(), key=lambda item:(item[1]), reverse=False))
        lexiconedContent.update(newParsedFiles)
        # lexiconedContent = dict(sorted(lexiconedContent.items(), key=lambda item:(item[1]), reverse=False))

        lexiconFile = open("lexicon.json", "w+")
        forwardIndexFile = open("forwardIndex.json", "w+")
        reverseIndexFile = open("reverseIndex.json", "w+")
        metaDataFile = open("metaData.json", "w+")
        lexiconedFile = open("files.json", "w+")

        # writing lexicon, forward index, reverseIndex to their respective opened files in json format
        json.dump(lexiconContent, lexiconFile)
        json.dump(forwardIndexContent, forwardIndexFile)
        json.dump(reverseIndexContent, reverseIndexFile)
        json.dump(metaDataContent, metaDataFile)
        json.dump(lexiconedContent, lexiconedFile)

        # closing files
        lexiconFile.close()
        reverseIndexFile.close()
        forwardIndexFile.close()
        metaDataFile.close()
        lexiconedFile.close()

        shutil.copy(originalPath, targetPath)

    end = time.time()
    # Time taken by the program
    print((end - start) / 60, "minutes")
