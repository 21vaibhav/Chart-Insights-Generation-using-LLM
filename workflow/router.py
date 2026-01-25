# workflow/router.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


ROUTER_PROMPT = ChatPromptTemplate.from_template(

    # change the below prompts 
    """
You are a routing agent for a maritime analytics system.

Decide how the user query should be handled.

Return ONLY ONE of:
- simple   (answerable directly using maritime domain knowledge)
- vision   (requires understanding a chart, graph, or image)
- sql      (requires querying or aggregating tabular data)

User query:
{query}

Decision:
"""
)


def router_node(llm):
    """
    llm: central Mistral model
    """

    chain = ROUTER_PROMPT | llm | StrOutputParser()

    def _route(state):
        decision = chain.invoke({"query": state["query"]}).strip().lower()
        return {"decision": decision}

    return _route
