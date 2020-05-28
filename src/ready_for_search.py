import sqlite3
import pickle

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from gensim.parsing.preprocessing import STOPWORDS
import re

class MakeDataForSearch:
    def __init__(self, data, titles,summaries,documents,svos):
        self.data, self.titles, self.summaries, self.documents, self.svos = self.get_all_texts_summary_titles_documents()

    def fetch_all_texts(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT text from document_info")
        tup = c.fetchall()
        conn.close()
        return tup

    def fetch_all_titles(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT title from document_info")
        tup = c.fetchall()
        conn.close()
        return tup
    def fetch_all_summary(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT summary from document_summary")
        tup = c.fetchall()
        conn.close()
        return tup
    def fetch_all_svos(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT auto_tags from document_tags")
        tup = c.fetchall()
        conn.close()
        return tup
    def fetch_all_documentsWithExtensions(self):
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute("SELECT document,extension from document_info")
        tup = c.fetchall()
        conn.commit()
        conn.close()
        return tup

    def get_all_texts_summary_titles_documents(self):
        svos_file = []
        texts = self.fetch_all_texts()
        titles = self.fetch_all_titles()
        summaries = self.fetch_all_summary()
        svos = self.fetch_all_svos()
        tup = self.fetch_all_documentsWithExtensions()

        data_file = [text[0] for text in texts]
        title_file = [title[0] for title in titles]
        summary_file = [summary[0] for summary in summaries]

        for i in range(len(svos)):
            lst = svos[i][0][1:-1].split("'")
            lst = [word for word in lst if word not in STOPWORDS and len(word) > 2]
            svo = [word for word in lst if len(word.split()) > 1]
            svos_file.append(svo)

        blob_list = [tup[k][0] for k in range(len(tup))]
        entension_list = [tup[k][1] for k in range(len(tup))]
        index_list = [i for i in range(len(tup))]

        dictionary = {k: {"document": x, "extension": y} for (k, x, y) in zip(index_list, blob_list, entension_list)}

        return data_file, title_file, summary_file, dictionary, svos_file


def get_corpus(text):
    """
    Function to clean text of websites, email addresess and any punctuation
    We also lower case the text
    """
    pattern = r"((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)"
    text = str(text)
    text = re.sub(pattern, " ", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    text = word_tokenize(text)
    # return text
    text = [word for word in text if word not in STOPWORDS]
    lemmed = [WordNetLemmatizer().lemmatize(word) for word in text if len(word) > 2]
    lemmed = [WordNetLemmatizer().lemmatize(word, pos='v') for word in lemmed]
    return lemmed


def get_latest_text_title():
    conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
    c = conn.cursor()
    c.execute("SELECT title,text from document_info where rowid = (SELECT MAX(rowid) FROM document_info)")
    tup = c.fetchall()
    conn.close()
    return tup

def get_latest_tags():
    conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
    c = conn.cursor()
    c.execute("SELECT manual_tags,auto_tags from document_tags where rowid = (SELECT MAX(rowid) FROM document_tags)")
    tup = c.fetchone()
    conn.close()
    return tup


# corpus = []
# for i in range(len(data)):
#     corpus.append(apply_all(titles[i]) + apply_all(data[i]))

# pickle.dump(corpus, open("corpus_file.pkl","wb"))

# if __name__ == '__main__':
def maintaining_all_files():
    data = []
    titles = []
    summaries = []
    documents = {}
    svos = []
    obj = MakeDataForSearch(data, titles, summaries, documents, svos)

    pickle.dump(obj.data, open(r"DataBase/data_file.pkl", "wb"))
    pickle.dump(obj.titles, open(r"DataBase/title_file.pkl", "wb"))
    pickle.dump(obj.summaries, open(r"DataBase/summary_file.pkl", "wb"))
    pickle.dump(obj.documents, open(r"DataBase/document_file.pkl", "wb"))
    pickle.dump(obj.svos, open(r"DataBase/svos_file.pkl", "wb"))

    print("Files is updated")

    # appending to the main corpus
    corpus = pickle.load(open(r"DataBase/corpus_file.pkl", "rb"))

    temp = get_latest_text_title()
    text = temp[0][1]
    title = temp[0][0]
    corpus.append(get_corpus(text)+get_corpus(title))

    pickle.dump(corpus, open(r"DataBase/corpus_file.pkl", "wb"))

    # appending to the tags corpus
    final_auto_tags = pickle.load(open(r"DataBase/tags_pickle.pkl", "rb"))

    tup = get_latest_tags()
    temp_auto_tags = tup[1][1:-1].split("'")
    temp_manual_tags = tup[0][1:-1].split("'")

    auto_tags = temp_manual_tags + temp_auto_tags
    auto_tags = [word for word in auto_tags if word not in STOPWORDS and len(word) > 2]

    final_auto_tags.append(auto_tags)

    pickle.dump(final_auto_tags, open(r"DataBase/tags_pickle.pkl", "wb"))

    # appending to title corpus
    title_corpus = pickle.load(open(r"DataBase/title_corpus.pkl", "rb"))
    title_corpus.append(get_corpus(title))

    pickle.dump(title_corpus, open(r"DataBase/title_corpus.pkl", "wb"))


    print("corpus is updated")



