# this file include source code of this beautiful repositry --> https://github.com/acrosson/nlp/tree/master/subject_extraction

import warnings
warnings.filterwarnings('ignore')
import os
import sqlite3
import re
import numpy as np
from gensim.parsing.preprocessing import STOPWORDS
from nltk.tokenize import word_tokenize, sent_tokenize

import nltk
# from nltk.stem import WordNetLemmatizer

from nltk import DefaultTagger, UnigramTagger, BigramTagger, TrigramTagger
import pickle

class SubjectTrigramTagger(object):
    """ Creates an instance of NLTKs TrigramTagger with a backoff
    tagger of a bigram tagger a unigram tagger and a default tagger that sets
    all words to nouns (NN)
    """

    def __init__(self, train_sents):
        """
        train_sents: trained sentences which have already been tagged.
                Currently using Brown, conll2000, and TreeBank corpuses
        """

        t0 = DefaultTagger('NN')
        t1 = UnigramTagger(train_sents, backoff=t0)
        t2 = BigramTagger(train_sents, backoff=t1)
        self.tagger = TrigramTagger(train_sents, backoff=t2)

    def tag(self, tokens):
        return self.tagger.tag(tokens)

class AutoTags:

    def __init__(self):
        self.NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
        self.VERBS = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']

    def clean_document(self, document):
        """Remove enronious characters. Extra whitespace and stop words"""
        document = re.sub('[^A-Za-z .-]+', ' ', document)
        document = ' '.join(document.split())
        document = ' '.join([i for i in document.split() if i not in STOPWORDS])
        return document


    def tokenize_sentences(self, document):
        sentences = sent_tokenize(document)
        sentences = [word_tokenize(sent) for sent in sentences]
        return sentences


    def get_entities(self, document):
        """Returns Named Entities using NLTK Chunking"""
        entities = []
        sentences = self.tokenize_sentences(document)

        # Part of Speech Tagging
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        for tagged_sentence in sentences:
            for chunk in nltk.ne_chunk(tagged_sentence):
                if type(chunk) == nltk.tree.Tree:
                    entities.append(' '.join([c[0] for c in chunk]).lower())
        return entities


    def word_freq_dist(self, document):
        """Returns a word count frequency distribution"""
        words = nltk.tokenize.word_tokenize(document)
        words = [word.lower() for word in words if word not in STOPWORDS]
        fdist = nltk.FreqDist(words)
        return fdist

    def extract_subject(self, document):
        # Get most frequent Nouns
        fdist = self.word_freq_dist(document)
        most_freq_nouns = [w for w, c in fdist.most_common(10)
                           if nltk.pos_tag([w])[0][1] in self.NOUNS]

        # Get Top 10 entities
        entities = self.get_entities(document)
        entities = list(set(entities))
        top_10_entities = [w for w, c in nltk.FreqDist(entities).most_common(10)]

        # Get the subject noun by looking at the intersection of top 10 entities
        # and most frequent nouns. It takes the first element in the list
        subject_nouns = [entity for entity in top_10_entities
                         if entity.split()[0] in most_freq_nouns]
        if len(subject_nouns) != 0:
            return subject_nouns[0]
        else:
            return ""


    # def trained_tagger(self,existing=False):
    #     """Returns a trained trigram tagger
    #     existing : set to True if already trained tagger has been pickled
    #     """
    #     if existing:
            # trigram_tagger = pickle.load(
            #     open(r'DataBase/trained_tagger.pkl', 'rb'))
            # return trigram_tagger

    #     # Aggregate trained sentences for N-Gram Taggers
    #     train_sents = nltk.corpus.brown.tagged_sents()
    #     train_sents += nltk.corpus.conll2000.tagged_sents()
    #     train_sents += nltk.corpus.treebank.tagged_sents()

    #     # Create instance of SubjectTrigramTagger and persist instance of it
    #     trigram_tagger = SubjectTrigramTagger(train_sents)
    #     pickle.dump(trigram_tagger, open(r'DataBase/trained_tagger.pkl', 'wb'))

    #     return trigram_tagger

    def merge_multi_word_subject(self, sentences, subject):
        """Merges multi word subjects into one single token
        ex. [('steve', 'NN', ('jobs', 'NN')] -> [('steve jobs', 'NN')]
        """
        if len(subject.split()) == 1:
            return sentences
        subject_lst = subject.split()
        sentences_lower = [[word.lower() for word in sentence]
                           for sentence in sentences]
        for i, sent in enumerate(sentences_lower):
            if subject_lst[0] in sent:
                for j, token in enumerate(sent):
                    start = subject_lst[0] == token
                    exists = subject_lst == sent[j:j + len(subject_lst)]
                    if start and exists:
                        del sentences[i][j + 1:j + len(subject_lst)]
                        sentences[i][j] = subject
        return sentences

    def tag_sentences(self, subject, document):
        """Returns tagged sentences using POS tagging"""
        trigram_tagger = pickle.load(open(r'DataBase/trained_tagger.pkl', 'rb'))

        # Tokenize Sentences and words
        sentences = self.tokenize_sentences(document)
        self.merge_multi_word_subject(sentences, subject)

        # Filter out sentences where subject is not present
        sentences = [sentence for sentence in sentences if subject in
                     [word.lower() for word in sentence]]

        # Tag each sentence
        tagged_sents = [trigram_tagger.tag(sent) for sent in sentences]
        return tagged_sents

    def get_svo(self, sentence, subject):
        """Returns a dictionary containing:
        subject : the subject determined earlier
        action : the action verb of particular related to the subject
        object : the object the action is referring to
        phrase : list of token, tag pairs for that lie within the indexes of
                    the variables above
        """
        subject_idx = next((i for i, v in enumerate(sentence)
                            if v[0].lower() == subject), None)
        data = {'subject': subject}
        for i in range(subject_idx, len(sentence)):
            found_action = False
            for j, (token, tag) in enumerate(sentence[i + 1:]):
                if tag in self.VERBS:
                    data['action'] = token
                    found_action = True
                if tag in self.NOUNS and found_action == True:
                    data['object'] = token
                    data['phrase'] = sentence[i: i + j + 2]
                    return data
        return {}


    def get_auto_tags_from_document(self, text, doc_id):
        document = text
        document = self.clean_document(document)

        entities = self.get_entities(document)

        if len(entities) == 0:
            auto_tags = word_tokenize(document.lower())
            auto_tags = list(set(auto_tags))
            # cleaning the auto tags futher for better search
            # auto_tags = clean_auto_tags(auto_tags)
            auto_tags = [word for word in auto_tags if word not in STOPWORDS and len(word) > 2]
            return auto_tags, []

        entities = list(set(entities))

        # final list for storing automatic generated tags (auto_tags)
        auto_tags = entities

        subject = self.extract_subject(document)
        if subject == "":
            # If there is no subject then tokenize the summary to get better tags than tokenizing the whole documents

            # conn = sqlite3.connect("Document_finder_db2.db")
            # c = conn.cursor()
            # c.execute(f"SELECT summary FROM document_summary where doc_id='{doc_id}' ")
            # temp_summary = c.fetchone()
            # conn.close()
            #
            # temp_tags = list(set(word_tokenize(temp_summary[0])))
            # auto_tags += temp_tags
            # auto_tags = [word for word in auto_tags if word not in STOPWORDS and len(word) > 2]
            # return str(auto_tags), ""
            return auto_tags, []

        tagged_sents = self.tag_sentences(subject, document)

        svos = [self.get_svo(sentence, subject)
                for sentence in tagged_sents]
        svos_list = []
        for svo in svos:
            if svo:
                svo_word = svo["subject"] + " " + svo["action"] + " " + svo["object"]
                svos_list.append(svo_word)

                auto_tags.append(svo_word)

        auto_tags = [word for word in auto_tags if word not in STOPWORDS and len(word) > 2]
        return auto_tags, svos_list
