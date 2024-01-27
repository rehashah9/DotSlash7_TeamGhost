import re

def is_sql_query(query):
    # Define a regex pattern to match common SQL keywords
    sql_keywords = ['SELECT', 'UPDATE', 'DELETE', 'INSERT', 'CREATE', 'ALTER', 'DROP', 'FROM', 'WHERE', 'JOIN', 'AND', 'OR']

    # Construct the regex pattern
    pattern = re.compile(r'\b(?:' + '|'.join(sql_keywords) + r')\b', re.IGNORECASE)

    # Check if any SQL keyword is present in the query
    return bool(re.search(pattern, query))