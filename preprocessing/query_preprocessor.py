# preprocess/query_parser.py

import re

def parse_user_query(query: str) -> dict:
    """
    Converts natural language query into structured intent
    """

    query = query.lower()

    intent = "insight"
    analysis_type = []
    metrics = []
    time_filter = None

    # -------- INTENT DETECTION --------
    if any(word in query for word in ["compare", "difference", "vs"]):
        intent = "comparison"
    elif any(word in query for word in ["predict", "forecast", "future"]):
        intent = "prediction"
    elif any(word in query for word in ["why", "reason", "cause"]):
        intent = "explanation"

    # -------- ANALYSIS TYPE --------
    if any(word in query for word in ["trend", "increase", "decrease"]):
        analysis_type.append("trend")
    if any(word in query for word in ["outlier", "anomaly", "spike"]):
        analysis_type.append("anomaly")
    if any(word in query for word in ["max", "minimum", "highest", "lowest"]):
        analysis_type.append("extreme")
    if "distribution" in query:
        analysis_type.append("distribution")

    # -------- METRIC EXTRACTION (basic heuristic) --------
    common_metrics = ["sales", "revenue", "profit", "cost", "count", "price"]
    for metric in common_metrics:
        if metric in query:
            metrics.append(metric)

    # -------- TIME FILTER --------
    time_match = re.search(r"(last|past)\s(\d+)\s(days|months|years)", query)
    if time_match:
        time_filter = time_match.group(0)

    return {
        "intent": intent,
        "analysis_type": analysis_type,
        "metrics": metrics,
        "time_filter": time_filter,
        "raw_query": query
    }


def query_parse_lower(query: str):
    return query.lower()