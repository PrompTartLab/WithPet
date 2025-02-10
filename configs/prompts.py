from langchain_core.prompts import PromptTemplate
from configs.schemas import SCHEMAS

SOURCE_ROUTING_PROMPT = f"""
You are an expert at routing a user question to the appropriate data source. The data sources are described below:

Return "pet_places" if the query is about finding or asking for facilities such as hospitals, museums, cafes, restaurants, hotels, or any other physical locations where services or activities are provided.

Return "not_relevant" if the query is not related to finding facilities, such as general knowledge questions or general chat.
"""


# Template for SQL generation (retry attempt)
SQL_RETRY_TEMPLATE = PromptTemplate(
    input_variables=[
        "question",
        "data_source",
        "examples",
        "schema",
        "external_knowledge",
        "previous_answer",
    ],
    template="""
You are an expert in generating SQL queries. Your task is to create SQL queries based on the user's question and the provided schema.

You must follow these rules:
### Rules for SQL Generation:
1. **Match Columns to Conditions**: Identify relevant columns in the schema that correspond to the conditions in the user's query. Use only columns specified in the schema.
2. **Avoid Unnecessary Filters**: If part of the query has no directly corresponding column, do not add assumptions or irrelevant filters. Instead, retrieve all data using `SELECT * FROM {data_source}`.
3. **Include Only Relevant Columns in WHERE Clause**: Only include columns in the `WHERE` clause that are directly related to the query. Do not infer conditions beyond what is explicitly asked in the query.
4. **Filter Days with Specific Rules**: 
   - For filtering days, use LIKE operation on the relevant column to match specific days:
     - Saturday: `DAYTIME_COLUMN LIKE "%토%"`
     - Sunday: `DAYTIME_COLUMN LIKE "%일요일%"`
5. **Ensure Schema Accuracy**: Always ensure the column names in the query match those defined in the schema exactly.
6. **SQL Tagging**: Wrap the generated SQL query between `<SQL>` and `</SQL>` tags to clearly separate it from other content.

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

# Template for SQL generation (initial attempt)
SQL_GENERATION_TEMPLATE = PromptTemplate(
    input_variables=[
        "question",
        "data_source",
        "examples",
        "schema",
        "external_knowledge",
    ],
    template="""
You are an expert in generating SQL queries. Your task is to create SQL queries based on the user's question and the provided schema. You must follow these rules:

### Rules for SQL Generation:
1. **Match Columns to Conditions**: Identify relevant columns in the schema that correspond to the conditions in the user's query. Use only columns specified in the schema.
2. **Avoid Unnecessary Filters**: If part of the query has no directly corresponding column, do not add assumptions or irrelevant filters. Instead, retrieve all data using `SELECT * FROM {data_source}`.
3. **Include Only Relevant Columns in WHERE Clause**: Only include columns in the `WHERE` clause that are directly related to the query. Do not infer conditions beyond what is explicitly asked in the query.
4. **Filter Days with Specific Rules**: 
   - For filtering days, use LIKE operation on the relevant column to match specific days:
     - Saturday: `DAYTIME_COLUMN LIKE "%토%"`
     - Sunday: `DAYTIME_COLUMN LIKE "%일요일%"`
5. **Ensure Schema Accuracy**: Always ensure the column names in the query match those defined in the schema exactly.
6. **SQL Tagging**: Wrap the generated SQL query between `<SQL>` and `</SQL>` tags to clearly separate it from other content.


Table schema: {schema}
External knowledge:{external_knowledge}

For your information, I'll provide examples of query-answer pairs.
{examples}

<QUESTION> {question} </QUESTION>
    """,
)

ANSWER_GENERATION_TEMPLATE = PromptTemplate(
    input_variables=[
        "question",
        "schema",
        "data",
    ],
    template="""
Based on the user's question: {question}
From the table with schema:
{schema}
Retrieved information is:
{data}
Please provide a detailed and concise answer in Korean.
Please include useful information like telephone number, homepage url, and full address.
Format the number with dashes for readability (e.g., 02-1234-5678).
If the data does not match the question completely, please explain the content of the retrieved data, but notify that it may not match the question.
Only explain the data included in your answer.
    """,
)
