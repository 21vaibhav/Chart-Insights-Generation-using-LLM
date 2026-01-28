# input/query_loader.py

from typing import Optional


def load_query(query: str) -> Optional[str]:

    if query is None:
        return None

    query = query.strip()

    if not query:
        return None

    return query
