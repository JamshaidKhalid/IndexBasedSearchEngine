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

    # originalPath = input("Enter path of file: ")
    print(originalPath)
    targetPath = "newDataSet"
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
    tokenList = list(lexiconContent.keys())[-1]
    tokenID = lexiconContent[tokenList]
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
            titleList = titleString.split()
            docID += 1
            tempTokenId = tokenID
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
        forwardIndexContent.update(newPreviousForwardData)
        reverseIndexContent.update(Inv_index)
        metaDataContent.update(newMetaData)
        lexiconedContent.update(newParsedFiles)

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
