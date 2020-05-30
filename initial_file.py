import pickle
import numpy as np
from nltk import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger
from tqdm import tqdm
import os

print("Downloading NLTK Dependencies...")
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
print("\n\nAll external dependencies of NLTK is downloaded..\n")
print("Extracting Word Embeddings From Globe Embeddings File..")


def load_word_embeddings():

    if os.path.exists(os.path.join(os.getcwd(), "word_embeddings.json")):
        print("word_embeddings.json file already exists.\n")
        return False

    global word_embeddings
    word_embeddings = {}

    try:
        f = open(r'DataBase/glove.6B.100d.txt', encoding="utf-8")
    except FileNotFoundError:
        print('''\n\nIf you do not have Glove-Embeddings File, then first download it from this link..''')
        print("https://www.kaggle.com/terenceliu4444/glove6b100dtxt")
        print("And put 'glove.6B.100d.txt' file in DataBase folder of this project\n\n")
        raise Exception("Glove-Embeddings File Not Found!")

    for line in tqdm(f, desc="Extracting.."):
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        word_embeddings[word] = coefs
    f.close()
    return True


if load_word_embeddings():
    pickle.dump(word_embeddings, open("word_embeddings.json", "wb"))
    print("Word Embeddings has been extracted, and saved to word_embeddings.json file..\n")


def trained_tagger():
    """Returns a trained trigram tagger
    existing : set to True if already trained tagger has been pickled
    """

    if os.path.exists(os.path.join(os.getcwd(), r"DataBase/trained_tagger.pkl")):
        print("Trained Tagger File already Exists..")
        return

    # Aggregate trained sentences for N-Gram Taggers
    train_sents = nltk.corpus.brown.tagged_sents()
    train_sents += nltk.corpus.conll2000.tagged_sents()
    train_sents += nltk.corpus.treebank.tagged_sents()

    t0 = DefaultTagger('NN')
    t1 = UnigramTagger(train_sents, backoff=t0)
    t2 = BigramTagger(train_sents, backoff=t1)
    trigram_tagger = TrigramTagger(train_sents, backoff=t2)

    pickle.dump(trigram_tagger, open(r'DataBase/trained_tagger.pkl', 'wb'))


print("Creating Tagger file...\n")

trained_tagger()

print("completed")


