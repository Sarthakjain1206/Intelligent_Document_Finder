import sqlite3
import pickle
from auto_tagging_script import AutoTags

from final_script_fulldb import get_summary
from final_script_fulldb import PreProcess, valid_extensions
from ready_for_search import *
print('imported')

def convertToBinaryData(file):
    #Convert digital data to binary format
    with open(file, 'rb') as file:
        blobData = file.read()
    return blobData


def load_corpus_and_data_files_main():
    global data_lst, titles_lst, auto_tag_lst, summary_lst, document_file_dictionary, corpus_lst,auto_tags_corpus,title_corpus

    data_lst = pickle.load(open(r"DataBase/data_file.pkl", "rb"))
    titles_lst = pickle.load(open(r"DataBase/title_file.pkl", "rb"))
    auto_tag_lst = pickle.load(open(r"DataBase/svos_file.pkl", "rb"))
    summary_lst = pickle.load(open(r"DataBase/summary_file.pkl", "rb"))
    document_file_dictionary = pickle.load(open(r"DataBase/document_file.pkl", "rb"))
    corpus_lst = pickle.load(open(r"DataBase/corpus_file.pkl", "rb"))
    auto_tags_corpus = pickle.load(open(r"DataBase/tags_pickle.pkl", "rb"))
    title_corpus = pickle.load(open(r"DataBase/title_corpus.pkl", "rb"))

def dump_corpus_and_data_files_main():
    pickle.dump(data_lst, open(r"DataBase/data_file.pkl", "wb"))
    pickle.dump(titles_lst, open(r"DataBase/title_file.pkl", "wb"))
    pickle.dump(summary_lst, open(r"DataBase/summary_file.pkl", "wb"))
    pickle.dump(document_file_dictionary, open(r"DataBase/document_file.pkl", "wb"))
    pickle.dump(auto_tag_lst, open(r"DataBase/svos_file.pkl", "wb"))
    pickle.dump(corpus_lst, open(r"DataBase/corpus_file.pkl", "wb"))
    pickle.dump(auto_tags_corpus, open(r"DataBase/tags_pickle.pkl", "wb"))
    pickle.dump(title_corpus, open(r"DataBase/title_corpus.pkl", "wb"))


def insert_data_to_database(doc_id, title, text, file, extension, summary, auto_tags, manual_tags, svos):
    try:
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()

        sqlite_insert_blob_query1 = """ INSERT INTO document_info
                                              (doc_id, title, text, document,extension) VALUES (?, ?, ?, ?, ?)"""

        document = convertToBinaryData(file)
        # Convert data into tuple format
        data_tuple1 = (doc_id, title, text, document, extension)
        c.execute(sqlite_insert_blob_query1, data_tuple1)

        sqlite_insert_blob_query2 = """ INSERT INTO document_summary
                                              (doc_id, summary) VALUES (?, ?)"""

        # Convert data into tuple format
        data_tuple2 = (doc_id, summary)
        c.execute(sqlite_insert_blob_query2, data_tuple2)

        sqlite_insert_blob_query3 = """ INSERT INTO document_tags
                                          (doc_id, title, auto_tags, manual_tags,svos) VALUES (?, ?, ?, ?, ?)"""

        # Convert data into tuple format
        data_tuple3 = (doc_id, title, str(auto_tags), str(manual_tags), str(svos))
        c.execute(sqlite_insert_blob_query3, data_tuple3)

        # Load all files for our system
        load_corpus_and_data_files_main()
        
        # Update text, title, summary list
        data_lst.append(text)
        titles_lst.append(title)
        summary_lst.append(summary)

        # Giving High Priority to Manual Tags, if user provides manual tags with file.
        # Then, append only manual tags, so that it can be shown on search results window for that file.
        if manual_tags:
            print("manual_tags: ",manual_tags)
            auto_tag_lst.append(manual_tags)
        else:
            auto_tag_lst.append(auto_tags)

        # Update document_file.pkl by providing new file's extension and blob data
        curr_index = len(document_file_dictionary)
        dic = {'document': document, 'extension': extension}
        document_file_dictionary[curr_index] = dic

        # Update corpus
        curr_corpus = get_corpus(text) + get_corpus(title)
        corpus_lst.append(curr_corpus)

        # Update tag_corpus
        curr_tag_corpus = auto_tags + manual_tags
        auto_tags_corpus.append(curr_tag_corpus)

        # Update title_corpus
        curr_title_corpus = get_corpus(title)
        title_corpus.append(curr_title_corpus)
        
        # Call function to update Indexer and its files
        maintain_updating_indexer(curr_corpus, curr_title_corpus, curr_tag_corpus)

        # Now dump all files with updated content
        dump_corpus_and_data_files_main()

        print("Congo! All Files are successfully updated!")
        conn.commit()
        print("File and data inserted successfully into a table")
        conn.close()

        # call maintaining_all_files() fn for updating all files for search.
        # maintaining_all_files()

    except sqlite3.Error as error:
        conn.rollback()
        print("-----Failed to insert data into sqlite table-----", error)
        raise Exception
    except:
        print("\n=====We encounter some problem while uploading a file=====\n")
        print("Please wait! we are cleaning the all data files, so that your Database will remain consistent\nThis might take few minutes")
        maintaining_all_files()
        raise Exception

    finally:
        if (conn):
            conn.close()
            print("the sqlite connection is closed")

def get_last_inserted_rowid():
    try:
        conn = sqlite3.connect(r"DataBase/Document_finder_db2.db")
        c = conn.cursor()
        c.execute('''SELECT MAX(rowid) FROM document_info''')
        tup = c.fetchone()
        conn.close()
        return tup[0]
    except Exception:
        print('Cannot access the database right now')

def main(file_upload, title, manual_tags):

    # load_word_embeddings()
    # print('loaded')
    global word_embeddings
    word_embeddings = pickle.load(open(r"word_embeddings.json", "rb"))
    
    preprocess_obj = PreProcess(file_upload)

    if preprocess_obj.check_extension():

        extension = preprocess_obj.get_extension()

        if extension == 'docx':
            text = preprocess_obj.get_text_from_docx_document()
            text = preprocess_obj.remove_escape_sequences(text)
            
        elif extension == 'pptx':
            text = preprocess_obj.get_text_from_pptx_document()
            text = preprocess_obj.remove_escape_sequences(text)

        elif extension == 'pdf':
            text = preprocess_obj.get_text_from_pdf_document()
            text = preprocess_obj.remove_escape_sequences(text)

        else:
            text = preprocess_obj.get_text_from_txt_document()
            text = preprocess_obj.remove_escape_sequences(text)

        #doc_id = str(file_upload.split('\\')[-1]).replace('.' + extension, "")  # name of file(in local directory) as doc_id

        # title = data.title[int(re.findall("_[0-9]+",doc_id)[0][1:])-1]

        doc_id = f'news_{get_last_inserted_rowid()+5}'
        print(doc_id)
        # title = input("Enter Title")
        #print(text)
        summary = get_summary(text, word_embeddings)
        #print(summary)

        # manual_tags = str(list(map(str, input("Enter manual tags").split("  "))))
        # manual_tags = []
        auto_tags_obj = AutoTags()
        auto_tags, svos = auto_tags_obj.get_auto_tags_from_document(text, doc_id)

        # assert type(auto_tags) == type(svos) == str, r"tags cannot be inserted into table as its data type doesn't match the database's data type"

        insert_data_to_database(doc_id, title, text, file_upload, extension, summary, auto_tags, manual_tags, svos)

    else:
        print('Invalid Extension')

# main()


