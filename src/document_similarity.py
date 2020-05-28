from gensim.models import LdaModel
from gensim import models, similarities
import numpy as np
from gensim.corpora import Dictionary
import time
import pickle
from scipy.stats import entropy
from scipy.spatial.distance import jensenshannon

print("Imported")
corpus = pickle.load(open(r"Database\corpus_file.pkl", "rb"))


def train_lda(corpus):
    num_topics = 100
    chunksize = 1000
    dictionary = Dictionary(corpus)
    lda_corpus = [dictionary.doc2bow(doc) for doc in corpus]

    t1 = time.time()

    # low alpha means each document is only represented by a small number of topics, and vice versa
    # low eta means each topic is only represented by a small number of words, and vice versa

    lda = LdaModel(corpus=lda_corpus, num_topics=num_topics, id2word=dictionary,
                   alpha=1e-2, eta=5e-2, chunksize=chunksize,
                   minimum_probability=0.0, passes=2)

    t2 = time.time()
    print("Time to train LDA model on ", len(corpus), "articles", (t2 - t1) / 60, "min")
    return dictionary, lda_corpus, lda


def jensen_shannon(query, matrix):
    p = query[:, None]  # original shape of query was (100,) , which means ---> (number of topics,)
    print(p.shape)  # shape becomes (100,1)

    q = matrix.T  # transpose matrix
    print(q.shape)  # shape --> (number of topics, total documents)
    return jensenshannon(p, q)

    # m = 0.5 * (p + q)
    # return np.sqrt(0.5 * (entropy(p, m) + entropy(q, m)))


def execute_training_of_lda(corpus):
    dictionary, lda_corpus, lda = train_lda(corpus)

    t3 = time.time()
    doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in lda[lda_corpus]])
    t4 = time.time()

    print("Time to get topic distribution", (t4 - t3) / 60, "min")
    pickle.dump(dictionary, open(r'LdaModel/dictionary.pkl', "wb"))
    pickle.dump(doc_topic_dist, open(r'LdaModel/doc_topic_distribution.pkl', "wb"))
    lda.save(r'LdaModel/model')
    print("All files are ready----")

def get_most_similar_documents(query,matrix,k=10):
    """
    This function implements the Jensen-Shannon distance above
    and retruns the top k indices of the smallest jensen shannon distances
    """
    sims = jensen_shannon(query, matrix)    # list of jensen shannon distances
    print(max(sims))
    print(sorted(sims, reverse=True)[:10])
    return sims.argsort()[:k]   # the top k positional index of the smallest Jensen Shannon distances

def get_similar_documents(doc_corpus):
    dictionary = pickle.load(open(r"LdaModel/dictionary.pkl", "rb"))
    doc_topic_dist = pickle.load(open(r"LdaModel/doc_topic_distribution.pkl", "rb"))
    lda = LdaModel.load(r"LdaModel/model")
    titles = pickle.load(open(r"DataBase/title_file.pkl", "rb"))

    bow = dictionary.doc2bow(doc_corpus)
    doc_distribution = np.array([tup[1] for tup in lda.get_document_topics(bow=bow)])

    most_sim_ids = get_most_similar_documents(doc_distribution, doc_topic_dist)
    return most_sim_ids
    # print()
    # for i in most_sim_ids:
    #     print(titles[i])
    #     print("===================")


# if __name__ == '__main__':
#
#     # t1 = time.time()
#     # print("Starting training...")
#     # execute_training_of_lda(corpus)
#     # t2 = time.time()
#     # print("Total time taken: ", (t2-t1)/60, "min")
#
#     doc_corpus = corpus[78]
#     get_similar_documents(doc_corpus)
