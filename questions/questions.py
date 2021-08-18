import nltk
import sys
import os
import string
import numpy as np


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = os.listdir(directory)
    result = dict()

    for file in data:
        path = os.path.join(directory, file)
        f = open(path, "r")
        result[file] = f.read()

    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    result = []

    # converting all the words to lowercase
    words = nltk.word_tokenize(document.lower())

    for word in words:
        if (
            word not in nltk.corpus.stopwords.words("english")
            and word not in string.punctuation
        ):
            result.append(word)

    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    words = dict()

    # get the number of times every word appears in every document
    for document in documents:

        seenWords = set()
        for word in documents[document]:

            if word not in seenWords:

                seenWords.add(word)

                if not word in words:
                    words[word] = 1
                else:
                    words[word] += 1

    # calculate the IDF for every word
    for word in words:
        words[word] = np.log(len(documents) / words[word])

    return words


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """

    filesDetails = dict()

    # for every file get its tf-idf
    for file in files:
        filesDetails[file] = 0
        for word in query:
            filesDetails[file] += files[file].count(word) * idfs[word]

    # order the results
    result = [
        file
        for file, count in sorted(
            filesDetails.items(), key=lambda item: item[1], reverse=True
        )
    ]

    # return n results
    return result[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    sentecesDetails = []

    for sentence in sentences:
        data = [sentence, 0, 0]

        for word in query:
            if word in sentences[sentence] and word in idfs:

                # get the total idf value
                data[1] += idfs[word]

                # get the term density value
                data[2] += sentences[sentence].count(word) / len(sentences[sentence])

        sentecesDetails.append(data)

    # order the results
    result = [
        sentence
        for sentence, idf, td in sorted(
            sentecesDetails, key=lambda item: (item[1], item[2]), reverse=True
        )
    ]

    # return n results
    return result[:n]


if __name__ == "__main__":
    main()
