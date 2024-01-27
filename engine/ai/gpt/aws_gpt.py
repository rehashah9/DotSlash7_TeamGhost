from ai.query_builder.aws_query_builder import aws_query_builder



class AWS_GPT:
    def __init__(self):
        self.aws_query_builder = aws_query_builder


    def query(self, query, service: str = None) -> str:
        sql_query = self.aws_query_builder[service].query(query)
        return sql_query
    



aws_gpt = AWS_GPT()