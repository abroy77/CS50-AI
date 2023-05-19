import nltk
import sys
import os
import string
import math
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
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
    files = [os.path.join(directory, filename) for filename in os.listdir(directory)]
    data = {}
    for file in files:
        with open(file, 'r') as f:
            text = f.read()
            data[os.path.basename(file)] = text
    
    return data



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tokens = nltk.word_tokenize(document)
    stopwords = nltk.corpus.stopwords.words("english")
    words = [word.lower() for word in tokens if word not in stopwords and word not in string.punctuation]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_docs = len(documents)
    # get all words in all documents
    words = set()
    for doc_words in documents.values():
        words.update(set(doc_words))
    # since it's a set all words are unique

    # loop through each unique word
    idfs = {}
    for word in words:
        # count the number of documents that contain the word
        num_docs_with_word = sum(word in doc_words for doc_words in documents.values())
        # calculate the idf
        idf = math.log(num_docs / num_docs_with_word)
        idfs[word] = idf
    
    return idfs



    



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = {}
    # loop through each file
    for filename, words in files.items():
        # calculate the tfidf for each word in the query
        tfidf = 0
        for word in query:
            tf = words.count(word)
            tfidf += tf * idfs[word]
        tfidfs[filename] = tfidf
    
    
    filenames = sorted(tfidfs.keys(), key = lambda x: tfidfs[x], reverse=True)

    filenames = filenames[:n]

    return filenames




def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idfs = {}
    qtds = {}
    # loop through sentences
    for sentence, words in sentences.items():
        idf=0
        # loop through query
        for word in query:
            if word in words:
                idf+= idfs[word]
        sentence_idfs[sentence]=idf
        qtd=0
        #loop through words
        for word in words:
            if word in query:
                qtd+=1
        qtd = qtd/len(words)
        qtds[sentence]=qtd
    
    top_sentences = sorted(sentence_idfs.keys(), key = lambda x: (sentence_idfs[x], qtds[x]), reverse=True)
    top_sentences = top_sentences[:n]
    return top_sentences


if __name__ == "__main__":
    main()
