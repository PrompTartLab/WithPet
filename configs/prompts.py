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
    You are an expert in generating SQL queries. Based on the user's question, external knowledge and the specified data source, generate an SQL query. 

    Data source: {datasource}
    Table schema: {schema}
    External knowledge:{external_knowledge}

    Ensure the query matches the schema of the data source and retrieves the most relevant information. Do not filter with extra columns that are not explicitly requested in the query.
    Use the 'LIKE' operator instead of equal(=) to filter text-type columns such as MENU_NAME or reviews and utilize the 'IN' operator for multiple possible options.
    Note that all columns other than those ending in English are Korean characters, and make sure that categorical columns are selected only in Possible values.
    Let's think step by step; first divide the user query into several conditions, tailor each condition to a possible value in the schema, and then convert each condition into a SQL statement.
    After the thoughts, provide the final SQL query in the <SQL> </SQL> tag.

    For your information, I'll provide examples of query-answer pairs.

    <QUERY> 부산역 근처 돼지국밥 맛집 알려주세요.
    <ANSWER> "부산역 근처" indicates proximity to Busan Station. 부산역 is located in 동구. This can be addressed using the DISTRICT_NAME column.
            "돼지국밥" specifies the type of food, which can be matched with the MENU_NAME column.
            맛집" implies that the restaurant should have a high rating, likely using the RATING column.
            <SQL> SELECT RESTAURANT_NAME_KOREAN, ADDRESS_KOREAN FROM restaurants WHERE DISTRICT_NAME = '동구' AND MENU_NAME LIKE '%돼지국밥%' ORDER BY RATING DESC LIMIT 5; </SQL>

    <QUERY> 광안리 근처에서 아이들이랑 가기 좋은 식당 추천해주세요.
    <ANSWER> "광안리 근처" indicates proximity to 광안리. 광안리 is in 수영구. This can be addressed using the DISTRICT_NAME column.
            Childeren might needs menu for childeren, which can be matched with MENU_FOR_CHILDREN_YN column. This column has Boolean type.
            <SQL> SELECT RESTAURANT_NAME_KOREAN, MENU_NAME FROM restaurants WHERE DISTRICT_NAME = '수영구' AND MENU_FOR_CHILDREN_YN = True ORDER BY RATING DESC LIMIT 5; </SQL>

    <QUERY> 외국인 친구랑 갈만한 관광지 알려주세요.
    <ANSWER> Foreign friends may like historical experience, which can be matched with the Major_Category column with '역사관광지'.
            <SQL> SELECT Tourist_Spot_Name_Korean FROM foreign_tourist_spots WHERE Major_Category = '역사관광지' ORDER BY Number_of_Visit DESC LIMIT 5; </SQL>

    <QUERY> 서구 근처에서 할 만한 액티비티 알려주세요.
    <ANSWER> 서구 근처" indicates proximity to 서구. 서구 is connected to 사하구, 사상구, 동구, and 중구. This can be addressed using the District column.
            "액티비티" specifies the type of tour, which can be matched with the Major_Category column with '육상 레포츠' '수상 레포츠' and '레포츠소개'.
            <SQL> SELECT Tourist_Spot_Name_Korean FROM local_tourist_spots WHERE District IN ('사하구', '사상구', '동구', '중구') AND Major_Category IN ('육상 레포츠', '수상 레포츠', '레포츠소개') ORDER BY Number_of_Visit DESC LIMIT 5; </SQL>

    <QUERY> {question}
    <ANSWER>
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
    You are an expert in generating SQL queries. Based on the user's question, external knowledge, and the specified data source, generate an SQL query.

    In a prior attempt, you generated a SQL query that returned no results. Relax constraints to retrieve relevant data.

    Data source: {datasource}
    Table schema: {schema}
    External knowledge:{external_knowledge}
    Prior SQL: {previous_answer}
    User query: {question}

    Provide the final SQL query in the <SQL> </SQL> tag.
    """,
)
