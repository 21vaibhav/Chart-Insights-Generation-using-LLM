# workflow/router.py
from langchain_core.prompts import ChatPromptTemplate




# from langchain_core.output_parsers import StrOutputParser


VISION_RULESETS_PROMPT = ChatPromptTemplate.from_template(
"""
You are a maritime analytics validation engine.

You are given:
1. Extracted chart information (from a vision model)
2. A set of domain-specific rules

Your task:
- Evaluate the extracted information against each rule
- Decide whether the rule PASSES, FAILS, or is NOT APPLICABLE
- Provide brief reasoning strictly based on the extracted data
- Do NOT reinterpret the image
- Do NOT invent missing values

Rules:
{ruleset}

Extracted chart data:
{vision_result}

Return output STRICTLY as JSON in the following format:

{
  "rule_evaluations": [
    {
      "rule_id": "<id>",
      "status": "PASS | FAIL | NOT_APPLICABLE",
      "reason": "short factual justification"
    }
  ],
  "overall_assessment": "PASS | FAIL | INCONCLUSIVE",
  "notes": "optional"
}




"""
)


VISION_ROUTER_PROMPT = ChatPromptTemplate.from_template(
"""
You are deciding whether a question requires analyzing an image.

Answer ONLY one of:
- answer_directly
- extract_from_graph

Rules:
- If answering requires reading values, trends, events, or comparisons visible in the graph → extract_from_graph
- If the question is conceptual, definitional, or can be answered without the graph → answer_directly

User question:
{query}
"""
)

SQL_ROUTER_PROMPT = ChatPromptTemplate.from_template(
"""
You are deciding whether a question requires querying tabular data.

Answer ONLY one of:
- answer_directly
- generate_sql

Rules:
- If answering requires filtering, aggregation, comparison, or computation on the data → generate_sql
- Otherwise → answer_directly

User question:
{query}
"""
)

SIMPLE_ANSWER_PROMPT = ChatPromptTemplate.from_template(
    """
You are a maritime domain expert.
Your are stricted to the maritime domain only.
dont generate the asnwer for the question out of the context.
if the question of out of the domain.
simply same sorry out of context/can't ans . 

As the question is conceptual,definitional, or can be answered without the image/data → answer_directly
Answer the user question using domain knowledge, clearly and concisely.

User question:
{query}

RELEVANT DOMAIN KNOWLEDGE:
{rag_context}
"""
)


def router_node(llm, router_prompt, valid_routes, retriever):
    def _route(state):

        print('hi i am here')
        prompt = router_prompt.format(query=state["query"])
        print(prompt)

        # llm.model.to('cuda')
        decision = llm.route(prompt)

        print(decision)

        if decision not in valid_routes:
            # llm.model.to("cpu")
            raise ValueError(
                f"Invalid routing decision: {decision}"
            )

        if decision == "answer_directly":
            
            rag_context = retriever.invoke(state['query']) 

            answer_prompt = SIMPLE_ANSWER_PROMPT.format(
                query=state["query"], 
                rag_context = rag_context
            )

            answer = llm.generate(
                prompt=answer_prompt
            )
            # llm.model.to("cpu")
            return {
                "decision": decision,
                "final_answer": answer,
            }

        # llm.model.to("cpu")  # "Park" it back on the CPU
        return {"decision": decision}

    return _route