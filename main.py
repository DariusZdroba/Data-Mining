import os
import re
from whoosh import index
from whoosh.fields import TEXT, Schema
from whoosh.qparser import QueryParser
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download("punkt")
nltk.download("stopwords")


ps = PorterStemmer()
stop_words = set(stopwords.words("english"))
# Set up the Whoosh index schema
schema = Schema(
    title=TEXT(stored=True),
    content=TEXT,
)
index_path = "wikipedia_index2"
if not os.path.exists(index_path):
    os.makedirs(index_path)
documentsPath = "C:\\Users\\Darius\\Downloads\\Wiki\\wiki-subset-20140602.tar2"

ix = index.create_in(index_path, schema)
# Function to extract title and content from each document
def extract_title_and_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Use a regular expression to find title-content pairs

    non_matches = re.split(r'\n*\[\[(.*?)\]\]\n', content)
    non_matches.pop(0)
    titles = non_matches[::2]
    contents = non_matches[1::2]
    # Extract title and content from each match
    #words = [nltk.word_tokenize(cont) for cont in contents]
    words = []

    for cont in contents:
        c = nltk.word_tokenize(cont)
        c = [ps.stem(word) for word in c if ((word.lower() not in stop_words) and (word.isalnum()))]
        words.append(c)

    return titles, words

# Index each document
def create_index():
    ix = index.create_in(index_path, schema)
    with ix.writer() as writer:
        for file_name in os.listdir(documentsPath):
            title, content = extract_title_and_content(documentsPath+"\\"+file_name)
            print(file_name)
            if title and content:
                for i in range(len(content)):
                    cnt = ' '.join(content[i])
                    writer.add_document(title=title[i], content=cnt)

# Searching the index
def search_index():
    ix = index.open_dir(index_path)
    with ix.searcher() as searcher:
        # Example query: search for documents containing the word "python"
        query = QueryParser("title", ix.schema).parse("1984")
        results = searcher.search(query)

        for result in results:
            print("Title:", result["title"])
        reader = searcher.reader()
        for docnum in range(reader.doc_count_all()):
            # Get the document
            doc = reader[docnum]

            # Access the "content" field
            content = doc.get("content", "")

            # Print the words from the "content" field
            words = content.split()  # Split the content into words
            print(f"Words in Document {docnum + 1}: {words}")

a = False
if(a):
    create_index()
else:
    search_index()