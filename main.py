import os
import re
from whoosh import index
from whoosh.fields import TEXT, Schema, ID
from whoosh.qparser import QueryParser
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from whoosh.query import And, Or

nltk.download("punkt")
nltk.download("stopwords")


ps = PorterStemmer()
stop_words = set(stopwords.words("english"))
# Set up the Whoosh index schema
schema = Schema(
    title=TEXT(stored=True),
    content=TEXT(stored = True),
)
index_path = "wikipedia_index"
if not os.path.exists(index_path):
    os.makedirs(index_path)
documentsPath = "C:\\Users\\Darius\\Downloads\\Wiki\\wiki-subset-20140602.tar"


# Function to extracst title and content from each document
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
    ix.close()

# Searching the index
def search_index(withCategory = False):
    categories, clues, titles = questions()
    ix = index.open_dir(index_path)
    query_parser = QueryParser("content", ix.schema)
    matches = 0
    for i in range(len(clues)):
        c = nltk.word_tokenize(clues[i])
        c = [ps.stem(word) for word in c if ((word.lower() not in stop_words) and (word.isalnum()))]
        word_queries = [query_parser.parse(word) for word in c]
        if(withCategory):
            cat = nltk.word_tokenize(categories[i])
            cat = [ps.stem(word) for word in cat if ((word.lower() not in stop_words) and (word.isalnum()))]
            w_queries = [query_parser.parse(word) for word in cat]
            word_queries += w_queries
        combined_query = Or(word_queries)
        with ix.searcher() as searcher:
            results = searcher.search(combined_query)
            if len(results) > 0 and results[0]["title"] == titles[i]:
                matches = matches + 1
    print(matches / len(clues))
def questions():
    with open("questions.txt", "r", encoding="utf-8") as file:
        content = file.read()
    text = content.splitlines()
    categories = text[::4]
    clues = text[1::4]
    answers = text[2::4]
    return categories, clues, answers

a = False
if(a):
    create_index()
else:
    search_index(True)
