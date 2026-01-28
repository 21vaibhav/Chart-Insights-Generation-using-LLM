# workflow/vision_flow.py
from langchain_core.prompts import ChatPromptTemplate


VISION_PROMPT = """
<|vision_start|><|image_pad|><|vision_end|>


You are a vision model analyzing a maritime-related chart.

Rules:
- ONLY extract information visible in the image
- Do NOT answer the user question
- Do NOT apply maritime domain reasoning
- Use approximate values if exact values are not visible
- If something is not visible, omit it

Return output STRICTLY as valid JSON.

JSON format:
{{
  "axes": {{
    "x": "...",
    "y": "...",
    "units": "..."
  }},
  "time_range": {{
    "start": "...",
    "end": "..."
  }},
  "trend": "...",
  "events": [
    {{
      "type": "peak | dip | change_point | anomaly",
      "x": "...",
      "y": "...",
      "description": "..."
    }}
  ],
  "notes": "..."
}}

User question (for context only):
{query}
"""



INTERPRET_PROMPT = ChatPromptTemplate.from_template(
    """
You are a maritime domain expert.

You are given structured data extracted from a chart.

STRICT RULES:
- Use domain knowledge ONLY to interpret the chart data
- Do NOT invent values not present in the chart
- Do NOT restate the question
- If the answer is not present in the chart data, reply: "Not visible in chart"

CHART DATA:
{vision_result}

RELEVANT DOMAIN KNOWLEDGE:
{rag_context}

QUESTION:
{query}

FINAL ANSWER (one sentence):
"""
)


def vision_node(llmv):
    def _vision(state):


        print('hi i am in vision node')
        prompt = VISION_PROMPT.format(query=state["query"])

        # qwen_client.model.to('cuda')
        result = llmv.analyze(
            image=state["image"],
            prompt=prompt,   # ONLY this
        )

        # try:
        #   parsed = json.loads(raw)
        # except Exception:
        #   parsed = {"raw_text": raw}

        # qwen_client.model.to("cpu")
        return {"vision_result": result}

    return _vision


def vision_interpret_node(llmc, retriever):
    def _interpret(state):
        print('hi i am in interpret node')

        rag_context = retriever.invoke(state['query'])

        prompt = INTERPRET_PROMPT.format(
            vision_result=state["vision_result"],
            query=state["query"],
            rag_context = rag_context
            )
        

        # mistral.model.to('cuda')
        response = llmc.generate(
            prompt=prompt
        )

        # mistral.model.to("cpu")
        return {"final_answer": response}

    return _interpret