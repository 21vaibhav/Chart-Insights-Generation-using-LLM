# llm/models/sqlcoder_client.py
import sqlite3
import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import re 


class SQLCoderClient:
    """
    SQLCoder client:
    - Generates SQL from schema + NL query
    - Executes SQL on SQLite (in-memory by default)
    """

    def __init__(
        self,
        model_name: str = "defog/sqlcoder-7b-2",
        device: str = "cuda",
        dtype=torch.float16,
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype,
            device_map="auto",
        )

    # ------------------------------------------------
    # 1. SQL GENERATION
    # ------------------------------------------------
    def generate_sql(self, prompt: str) -> str:

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.0,
                do_sample=False,
            )

        decoded = self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
        )

        # Extract SQL safely
        match = re.search(r"### SQL\s*(.*)", decoded, re.S)
        if not match:
            raise ValueError("No SQL found in model output")

        sql = match.group(1).strip()
        sql = sql.split("```")[0].strip()
        return sql.rstrip(";") + ";"

    # ------------------------------------------------
    # 2. SQLITE EXECUTION
    # ------------------------------------------------
    def execute_sql(
        self,
        df: pd.DataFrame,
        sql_query: str,
        db_path: str = ":memory:",
        table_name: str = "data",
    ) -> pd.DataFrame:
        """
        Executes SQL on SQLite.
        df is loaded as table `data` by default.
        """

        conn = sqlite3.connect(db_path)

        try:
            df.to_sql(
                table_name,
                conn,
                if_exists="replace",
                index=False,
            )

            result = pd.read_sql_query(sql_query, conn)
        finally:
            conn.close()

        return result
