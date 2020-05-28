import pickle
import numpy as np
from nltk import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger

print("Downloading...")
import nltk
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')
nltk.download('chunk')
nltk.download('corpus')
nltk.download('brown')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('treebank')
nltk.download('conll2000')
print("All external dependencies of nltk is downloaded..")
print()
print("Extracting Word Embeddings..")

def load_word_embeddings():
    global word_embeddings
    word_embeddings = {}
    f = open(r'DataBase/glove.6B.100d.txt', encoding="utf-8")
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()

load_word_embeddings()

pickle.dump(word_embeddings,open("word_embeddings.json","wb"))
print("Word Embeddings has been extracted, and saved to word_embeddings.json file..")
print()

def trained_tagger():
    """Returns a trained trigram tagger
    existing : set to True if already trained tagger has been pickled
    """
    # Aggregate trained sentences for N-Gram Taggers
    train_sents = nltk.corpus.brown.tagged_sents()
    train_sents += nltk.corpus.conll2000.tagged_sents()
    train_sents += nltk.corpus.treebank.tagged_sents()

    t0 = DefaultTagger('NN')
    t1 = UnigramTagger(train_sents, backoff=t0)
    t2 = BigramTagger(train_sents, backoff=t1)
    trigram_tagger = TrigramTagger(train_sents, backoff=t2)

    pickle.dump(trigram_tagger, open(r'DataBase/trained_tagger.pkl', 'wb'))

    return trigram_tagger

print("Creating Tagger file...")

trained_tagger()

print("completed")
