import pickle
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

        nd = self.initialize_corpus(corpus)  # Number of documents with word.
        self.reverse_index = nd
        self.calc_idf(nd)

    def initialize_corpus(self, corpus):
        nd = {}
        num_docs = 0

        for document in corpus:
            document_len = len(document)
            self.doc_len.append(document_len)
            num_docs += document_len  # num_doc will calculate the value of total words in corpus.

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

        self.average_docs_len = num_docs / self.corpus_size  # calculating average doc length
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
            'b': self.b
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


class Search:
    def __init__(self, data):
        self.data = data

    def get_top_n(self, query, documents, n=5):
        assert self.data['corpus_size'] == len(documents), "The documents given don't match the index corpus!"

        scores = self.get_scores(query)
        top_n = np.argsort(scores)[::-1][:n]
        return top_n, [documents[i] for i in top_n]

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
