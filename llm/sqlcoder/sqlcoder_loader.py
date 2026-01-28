import requests
import os 
from dotenv import load_dotenv

load_dotenv()

# def generate_sql(prompt_text):
#     """Sends the final prompt to Cloudflare's SQLCoder API."""
#     AUTH_TOKEN = "HtlGgpDflWPRZdSiwrfIpBYo2B27shv19M0sr9j5"
#     ACCOUNT_ID = "a78392e2b98400de78230f1cc264d815"
#     MODEL_ID = "@cf/defog/sqlcoder-7b-2"
    
#     url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL_ID}"
#     headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    
#     try:
#         response = requests.post(url, headers=headers, json={"prompt": prompt_text})
#         result = response.json()
#         if result['success']:
#             return result['result']['response']
#         else:
#             return f"API Error: {result['errors']}"
#     except Exception as e:
#         return f"Request failed: {str(e)}"

from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables!")

client = Groq(api_key=GROQ_API_KEY)

def generate_sql(prompt):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile", # High performance SQL model
    )
    sql = chat_completion.choices[0].message.content
    sql = sql.strip().strip("```sql").strip("```")
    return sql