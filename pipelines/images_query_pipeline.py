from preprocessing.query_preprocessor import query_parse_lower
from input.image_loader import *

def image_query(img,query):
    query = query_parse_lower(query)
    return img,query 