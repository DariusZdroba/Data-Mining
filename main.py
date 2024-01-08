import os
import re
from whoosh import index
from whoosh.fields import TEXT, Schema
from whoosh.qparser import QueryParser
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download("punkt")
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
# Set up the Whoosh index schema
schema = Schema(
    title=TEXT(stored=True),
    content=TEXT,
)

index_path = "wikipedia_index"

if not os.path.exists(index_path):
    os.makedirs(index_path)

# Open or create the Whoosh index
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

        c = [word for word in c if (word.lower() not in stop_words) or "==" in word]


    return titles, words

# Index each document
with ix.writer() as writer:
    #for file_name in os.listdir("enwiki-20140602-pages-articles.xml-0567.txt"):
        file_path = "enwiki-20140602-pages-articles.xml-0567.txt"

        title, content = extract_title_and_content(file_path)

        if title and content:
            # Add a document to the Whoosh index
            writer.add_document(title=title, content=content)

# Searching the index
with ix.searcher() as searcher:
    # Example query: search for documents containing the word "python"
    query = QueryParser("content", ix.schema).parse("python")
    results = searcher.search(query)

    for result in results:
        print("Title:", result["title"])
