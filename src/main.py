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
        data_tuple3 = (doc_id, title, auto_tags, manual_tags, svos)
        c.execute(sqlite_insert_blob_query3, data_tuple3)

        conn.commit()
        print("file and data inserted successfully into a table")
        conn.close()

        # call maintaining_all_files() fn for updating all files for search.
        maintaining_all_files()

    except sqlite3.Error as error:
        conn.rollback()
        print("Failed to insert data into sqlite table", error)
        raise Exception
    finally:
        if (conn):
            conn.close()
            # print("the sqlite connection is closed")

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

def main(file_upload, title):

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

        doc_id = f'news_{get_last_inserted_rowid()+15}'                # doc_id = 'news_5782'
        # doc_id = 'news_5783'
        print(doc_id)
        # title = input("Enter Title")
        # text = text
        #print(text)
        summary = get_summary(text, word_embeddings)
        #print(summary)

        # manual_tags = str(list(map(str, input("Enter manual tags").split("  "))))
        manual_tags = ""
        auto_tags_obj = AutoTags()
        auto_tags, svos = auto_tags_obj.get_auto_tags_from_document(text, doc_id)

        assert type(auto_tags) == type(svos) == str, r"tags cannot be inserted into table as its data type doesn't match the database's data type"

        print(auto_tags)
        print(manual_tags)

        insert_data_to_database(doc_id, title, text, file_upload, extension, summary, auto_tags, manual_tags, svos)


    else:
        print('Invalid Extension')

# main()


