import pickle
from typing import Dict, Any

import numpy as np
import math

class Indexer:
    def __init__(self, corpus, search_type, k1=1.5, b=0.75, epsilon=0.25):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

        self.search_type = search_type
        self.corpus_size = len(corpus)
        self.average_docs_len = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_len = []
        self.num_docs = 0
        nd = self.initialize_corpus(corpus)  # Number of documents with word.
        self.reverse_index = nd
        self.calc_idf(nd)

    def initialize_corpus(self, corpus):
        nd = {}

        for document in corpus:
            document_len = len(document)
            self.doc_len.append(document_len)
            self.num_docs += document_len  # num_doc will calculate the value of total words in corpus.

            frequencies = {}  # frequencies of word in current document.

            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.doc_freqs.append(frequencies)  # doc_freqs list will contain words frequencies of all documents.

            for word, freq in frequencies.items():
                if word not in nd:
                    nd[word] = 0
                nd[word] += 1  # nd will maintain Number of documents with a word

        self.average_docs_len = self.num_docs / self.corpus_size  # calculating average doc length
        return nd

    def calc_idf(self, nd):
        """
        Calculates frequencies of terms in documents and in corpus.
        This algorithm sets a floor on the idf values to eps * average_idf
        """
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in nd.items():
            idf = math.log(self.corpus_size - freq + 0.5) - math.log(freq + 0.5)
            self.idf[word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)
        self.average_idf = idf_sum / len(self.idf)

        eps = self.epsilon * self.average_idf
        for word in negative_idfs:
            self.idf[word] = eps

    def create_files(self):
        dictionary = {
            'nd': self.reverse_index,
            'corpus_size': self.corpus_size,
            'average_docs_len': self.average_docs_len,
            'doc_freqs': self.doc_freqs,
            'idf': self.idf,
            'doc_len': self.doc_len,
            'k1': self.k1,
            'epsilon': self.epsilon,
            'b': self.b,
            'num_docs': self.num_docs
        }
        print("=========================")
        print(self.search_type)
        print(type(self.search_type))
        print("=========================")
        if self.search_type == "relevance" or self.search_type == "tag" or self.search_type == "title":
            pickle.dump(dictionary, open(f"DataBase/search_file_{self.search_type}.pkl", "wb"))
            print("File is ready!")
        else:
            raise Exception("Invalid Argument 'type' of create_files()")

class UpdateIndexer:

    def __init__(self, new_corpus, search_type, epsilon=0.25):
        if new_corpus[0] is list:
            self.new_corpus = new_corpus        # It must be a list of lists --> [ [],[],[] ]
        else:
            self.new_corpus = [new_corpus]

        self.search_type = search_type
        self.prev_search_data = pickle.load(open(f"DataBase/search_file_{self.search_type}.pkl", "rb"))
        self.epsilon = epsilon
        self.curr_average_idf = 0

    def update_indexer(self):

        for document in self.new_corpus:
            document_len = len(document)
            self.prev_search_data['doc_len'].append(document_len)
            self.prev_search_data['corpus_size'] += 1
            self.prev_search_data['num_docs'] += document_len  # num_doc will calculate the value of total words in corpus.

            frequencies = {}  # frequencies of word in current document.

            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
            self.prev_search_data['doc_freqs'].append(frequencies)  # doc_freqs list will contain words frequencies of all documents.

            for word, freq in frequencies.items():
                try:
                    self.prev_search_data['nd'][word] += 1
                except KeyError:
                    self.prev_search_data['nd'][word] = 1

        self.prev_search_data['average_docs_len'] = self.prev_search_data['num_docs'] / self.prev_search_data['corpus_size']  # calculating average doc length
        # return nd

    def calc_idf(self):
        # collect idf sum to calculate an average idf for epsilon value
        idf_sum = 0
        # collect words with negative idf to set them a special epsilon value.
        # idf can be negative if word is contained in more than half of documents
        negative_idfs = []
        for word, freq in self.prev_search_data['nd'].items():
            idf = math.log(self.prev_search_data['corpus_size'] - freq + 0.5) - math.log(freq + 0.5)
            self.prev_search_data['idf'][word] = idf
            idf_sum += idf
            if idf < 0:
                negative_idfs.append(word)

        self.curr_average_idf = idf_sum / len(self.prev_search_data['idf'])

        eps = self.epsilon * self.curr_average_idf
        for word in negative_idfs:
            self.prev_search_data['idf'][word] = eps
    def dump_file(self):
        pickle.dump(self.prev_search_data, open(f"DataBase/search_file_{self.search_type}.pkl", "wb"))
        print("Search File is Updated!")


class Search:
    def __init__(self, data):
        self.data = data
        print(data['corpus_size'])

    def get_top_n(self, query, documents, n=5):
        assert self.data['corpus_size'] == len(documents), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]

        index = 0
        for i in top_n:
            if scores[i] == 0:
                break
            index += 1

        return top_n[:index], [documents[i] for i in top_n[:index]]

    def get_scores(self, query):
        """
        The ATIRE BM25 variant uses an idf function which uses a log(idf) score. To prevent negative idf scores,
        this algorithm also adds a floor to the idf value of epsilon.
        See [Trotman, A., X. Jia, M. Crane, Towards an Efficient and Effective Search Engine] for more info
        :param query:
        :return:
        """
        score = np.zeros(self.data['corpus_size'])
        doc_len = np.array(self.data['doc_len'])
        for q in query:
            q_freq = np.array([(doc.get(q) or 0) for doc in self.data['doc_freqs']])
            score += (self.data['idf'].get(q) or 0) * (q_freq * (self.data['k1'] + 1) /
                                                       (q_freq + self.data['k1'] * (
                                                                   1 - self.data['b'] + self.data['b'] * doc_len /
                                                                   self.data['average_docs_len'])))
        return score