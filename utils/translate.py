from langchain_core.prompts import PromptTemplate


def ko_to_eng(template: str, query: str, llm) -> str:

    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
    )

    llm_chain = prompt | llm

    output = llm_chain.invoke(query)
    return output
