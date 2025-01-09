from langchain_core.prompts import PromptTemplate

SOURCE_ROUTING_PROMPT = """
You are an expert at routing a user question to the appropriate data source.
Based on the category the question is referring to, route it to the relevant data source.
Return "tourist_spots" if the query asks for recommendation of tourist spots.
Return "restaurants" if the query requests restaurant recommendations.
Returns "web" if it is not related to tourist attractions or restaurants, such as weather or transportation.
    """

# Template for SQL generation (initial attempt)
SQL_GENERATION_TEMPLATE = PromptTemplate(
    input_variables=["question", "datasource", "schema", "external_knowledge"],
    template="""
You are an expert in generating SQL queries. Your task is to create SQL queries based on the user's question and the provided schema.

You must follow these rules:
### Rules for SQL Generation:
1. Identify relevant columns in the schema that correspond to the conditions in the user's query.
2. If a part of the query has no directly corresponding column, do not add unnecessary filters. Instead, retrieve all data (e.g., `SELECT * FROM {data_source}`).
3. Only include columns in the `WHERE` clause if they are directly related to the query. Do not add assumptions or irrelevant filters.
4. Ensure each column matches the schema of the data source.
5. Answer the sql only between <SQL> </SQL> tag.

In a prior turn, you have predicted a SQL, which returned no results. Your job now is to generate a new SQL to try again.
In general, you should try to RELAX constraints.

Table schema: {schema}
External knowledge:{external_knowledge}
Prior sql : {previous_answer}

For your information, I'll provide examples of query-answer pairs.
{examples}

<QUESTION> {question} </QUESTION>
    """,
)

# Template for SQL generation (retry attempt)
SQL_RETRY_TEMPLATE = PromptTemplate(
    input_variables=[
        "question",
        "datasource",
        "schema",
        "external_knowledge",
        "previous_answer",
    ],
    template="""
You are an expert in generating SQL queries. Your task is to create SQL queries based on the user's question and the provided schema. You must follow these rules:

### Rules for SQL Generation:
1. Identify relevant columns in the schema that correspond to the conditions in the user's query.
2. If a part of the query has no directly corresponding column, do not add unnecessary filters. Instead, retrieve all data (e.g., `SELECT * FROM {data_source}`).
3. Only include columns in the `WHERE` clause if they are directly related to the query. Do not add assumptions or irrelevant filters.
4. Ensure each column matches the schema of the data source.
5. Answer the sql only between <SQL> </SQL> tag.

Table schema: {schema}
External knowledge:{external_knowledge}

For your information, I'll provide examples of query-answer pairs.
{examples}

<QUESTION> {question} </QUESTION>
    """,
)
