import warnings
warnings.filterwarnings('ignore')

import re
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity


import PyPDF2
from docx import Document

import textract


def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

valid_extensions = {'docx', 'pptx', 'txt', 'pdf'}

class PreProcess:

    def __init__(self, file):
        self.file = file

    def check_extension(self):
        if self.file.split('.')[-1] in valid_extensions:
            return True
        else:
            return False


    def get_extension(self):
        return self.file.split('.')[-1]


    def get_text_from_docx_document(self):
        try:
            doc = Document(self.file)
            temp = ''
            for para in doc.paragraphs:
                temp += para.text
            return temp
        except Exception:
            print('Raising......')
            raise Exception

    #     text = textract.process(file)
    #     text = str(text)[2:]
    #     return text

    def get_text_from_pdf_document(self):
        file_obj = open(self.file, "rb")
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
        page_numbers = pdf_reader.numPages
        temp = ''

        for i in range(page_numbers):
            page_obj = pdf_reader.getPage(i)
            temp += page_obj.extractText()
        file_obj.close()
        return temp


    def get_text_from_txt_document(self):
        #     text = textract.process(file)
        #     text = str(text)[2:]
        try:
            f = open(self.file, "r")
            temp = f.read()

        except UnicodeDecodeError:
            #         print("\n\nI am in except block\n\n")
            try:
                f = open(self.file, "r", encoding="utf-8")
                temp = f.read()
            except:
                print("Sorry! can't decode encodings!")
                raise Exception("Sorry! can't decode bytes")
        # except Exception:
        #     print('Another exception occured')
        #     raise Exception
        finally:
            f.close()
            return temp



    def get_text_from_pptx_document(self):
        text = textract.process(self.file)
        text = str(text)[2:]
        return text


    def remove_escape_sequences(self, text):
        pattern = r"\\[a-z]"
        text = re.sub(pattern, " ", text)
        return text


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


def cleaning_for_summarization(text):
    pattern = r"((\S+)?(http(s)?)(\S+))|((\S+)?(www)(\S+))|((\S+)?(\@)(\S+)?)"
    text = re.sub(pattern, " ", text)

    sentences = sent_tokenize(text)
    #     for j in range(len(sentences)):
    #         sentences[j] = re.sub("[^a-zA-Z]"," ",sentences[j])

    clean_sentences = sentences

    for j in range(len(clean_sentences)):
        clean_sentences[j] = word_tokenize(clean_sentences[j])

    return clean_sentences


def get_summary(text, word_embeddings):
    tokenized_sent = cleaning_for_summarization(text)

    sentence_vectors = []
    for i in tokenized_sent:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i]) / (len(i) + 0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    # similarity matrix
    sim_mat = np.zeros([len(tokenized_sent), len(tokenized_sent)])

    for i in range(len(tokenized_sent)):
        for j in range(len(tokenized_sent)):
            if i != j:
                sim_mat[i][j] = \
                cosine_similarity(sentence_vectors[i].reshape(1, 100), sentence_vectors[j].reshape(1, 100))[0, 0]

    nx_graph = nx.from_numpy_array(sim_mat)
    scores = nx.pagerank(nx_graph)

    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(tokenized_sent)), reverse=True)
    summarize_text = []
    if len(ranked_sentence) == 1:
        summarize_text.append(" ".join(ranked_sentence[0][1]))
    elif len(ranked_sentence) == 0:
        summarize_text = []
    else:
        for i in range(2):
            summarize_text.append(" ".join(ranked_sentence[i][1]))

    if len(". ".join(summarize_text)) > 1400:
        summary = summarize_text[0]
    else:
        summary = ". ".join(summarize_text)

    return summary

