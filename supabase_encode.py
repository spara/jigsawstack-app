import os
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
from supabase import create_client, Client
import vecs
from dotenv import load_dotenv

load_dotenv()

supabase_password = os.getenv('SUPABASE_PASSWORD')

DB_CONNECTION = "postgresql://postgres.wdatpzdaobgyomvjwpmg:" + supabase_password +"@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
vx = vecs.create_client(DB_CONNECTION)

embedding_model = SentenceTransformer("thenlper/gte-large")
MODEL = "text-embedding-3-small"


def create_vectors(prompt):
    result = embedding_model.encode(prompt)

    return result.tolist()

def tiktoken_length(text):
    encoding = tiktoken.encoding_for_model(MODEL)
    num_tokens = len(encoding.encode(text))

    return num_tokens

def recursive_chracter_splitter_chunking(text):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=5,
        length_function=tiktoken_length,
        is_separator_regex=False,
    )

    data = text_splitter.create_documents([text])
    
    # text splitter returns langchain Document class
    # reformat into an array of strings
    doc =[]
    for d in data:
        d = d.page_content
        doc.append(d)

    return doc

def create_embeddings(text):
    records = []
    id_num = 0
    chunks = recursive_chracter_splitter_chunking(text)
    for chunk in chunks:
        id = str(id_num)
        embedding = create_vectors(chunk)
        record = ("vec" + id, embedding, {"text": chunk})
        records.append(record)
        id_num += 1

    return records


def supabase_upsert(text):
    records = create_embeddings(text)
    docs = vx.get_or_create_collection(name="docs", dimension=1024)
    docs.upsert(records)

    docs.create_index(measure=vecs.IndexMeasure.cosine_distance)

def supabase_query(query):
    query_vector = create_vectors(query)
    docs = vx.get_or_create_collection(name="docs", dimension=1024)

    context_data = docs.query(
        data=query_vector,
        limit=5,
        filters={},
        measure="cosine_distance",
        include_value=False,
        include_metadata=True,
)

    return context_data


