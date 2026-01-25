# workflow/vision_flow.py
from langchain_core.prompts import ChatPromptTemplate




VISION_PROMPT = ChatPromptTemplate.from_template(
    """
You are a vision model analyzing a maritime-related chart.

Rules:
- ONLY extract information visible in the image
- Do NOT answer the user question
- Do NOT apply maritime domain reasoning
- Use approximate values if exact values are not visible
- If something is not visible, omit it

Return output STRICTLY as valid JSON.

JSON format:
{
  "axes": {
    "x": "...",
    "y": "...",
    "units": "..."
  },
  "time_range": {
    "start": "...",
    "end": "..."
  },
  "trend": "...",
  "events": [
    {
      "type": "peak | dip | change_point | anomaly",
      "x": "...",
      "y": "...",
      "description": "..."
    }
  ],
  "notes": "..."
}

User question (for context only):
{query}
"""
)


INTERPRET_PROMPT = ChatPromptTemplate.from_template(
    """
You are a maritime domain expert.

Based on the extracted chart analysis below, answer the user query clearly and concisely.

Chart analysis:
{vision_result}

User query:
{query}
"""
)


def vision_node(qwen_client):
    def _vision(state):
        prompt = VISION_PROMPT.invoke(
            {"query": state["query"]}
        ).to_string()

        result = qwen_client.analyze(
            image_path=state["image_path"],
            prompt=prompt,   # ONLY this
        )

        try:
        parsed = json.loads(raw)
        except Exception:
        parsed = {"raw_text": raw}
        
        return {"vision_result": result}

    return _vision


def vision_interpret_node(central_llm):
    chain = INTERPRET_PROMPT | central_llm

    def _interpret(state):
        response = chain.invoke(
            {
                "vision_result": state["vision_result"],
                "query": state["query"],
            }
        )
        return {"final_answer": response.content}

    return _interpret
