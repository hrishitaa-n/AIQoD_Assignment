import json
import re

from langchain_core.prompts import PromptTemplate

from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings
)

from llama_index.llms.ollama import Ollama as LlamaOllama
from llama_index.embeddings.huggingface import (
    HuggingFaceEmbedding
)

from config import OLLAMA_MODEL, log
# LlamaIndex 
def build_llama_index(df):
    log.info("Building LlamaIndex over CSV data...")
    documents = [
        Document(text=", ".join(f"{k}: {v}" for k, v in row.items()))
        for row in df.to_dict("records")
    ]
    Settings.llm         = LlamaOllama(model=OLLAMA_MODEL, request_timeout=120)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    index = VectorStoreIndex.from_documents(documents)
    log.info("LlamaIndex ready.")
    return index.as_query_engine()


# 3. LangChain 
PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are a MongoDB query generator.

STRICT RULES:
- Output ONLY a JSON object, nothing else
- ALL keys must be in double quotes
- Use ONLY these exact field names: "ProductID", "ProductName", "Category",
  "Price", "Rating", "ReviewCount", "Stock", "Discount", "Brand", "LaunchDate"
- Use MongoDB operators: $gt, $lt, $gte, $lte, $in, $and, $or
- Numbers must NOT be quoted (e.g. 50, not "50")
- For dates use: {{"$date": "YYYY-MM-DD"}}
- Output format: {{"filter": {{...}}, "sort": [[field, 1 or -1]] or null}}

EXAMPLES:
Q: products with price greater than 50
A: {{"filter": {{"Price": {{"$gt": 50}}}}, "sort": null}}

Q: Electronics with rating above 4
A: {{"filter": {{"Category": "Electronics", "Rating": {{"$gt": 4}}}}, "sort": null}}

Q: products sorted by price descending
A: {{"filter": {{}}, "sort": [["Price", -1]]}}

Now answer this:
Q: {question}
A:"""
)

def fix_unquoted_keys(raw):
    fixed = re.sub(r'(?<!["\w])(\$?\w+)\s*:', r'"\1":', raw)
    fixed = re.sub(r'""(\$?\w+)""', r'"\1"', fixed)
    return fixed
def convert_numeric_values(obj):
    numeric_fields = {
        "ProductID",
        "Price",
        "Rating",
        "ReviewCount",
        "Stock",
        "Discount"
    }

    if isinstance(obj, dict):
        fixed = {}

        for k, v in obj.items():

            if isinstance(v, dict):
                fixed[k] = convert_numeric_values(v)

                for op, op_val in fixed[k].items():
                    if (
                        isinstance(op_val, str)
                        and op_val.replace(".", "", 1).isdigit()
                    ):
                        fixed[k][op] = (
                            float(op_val)
                            if "." in op_val
                            else int(op_val)
                        )

            elif (
                k in numeric_fields
                and isinstance(v, str)
                and v.replace(".", "", 1).isdigit()
            ):
                fixed[k] = float(v) if "." in v else int(v)

            else:
                fixed[k] = v

        return fixed

    return obj
def ask_llm(llm, question):
    try:
        prompt = PROMPT.format(question=question)
        raw    = llm.invoke(prompt).strip()
        raw    = re.sub(r"```(?:json)?|```", "", raw).strip()
        match  = re.search(r'\{.*\}', raw, re.DOTALL)
        raw    = match.group() if match else raw

        try:
            query = json.loads(raw)
        except json.JSONDecodeError:
            raw   = fix_unquoted_keys(raw)
            query = json.loads(raw)

        query["filter"] = convert_numeric_values(
            query.get("filter", {})
        )

        log.info("Generated query: %s", json.dumps(query))
        return query

    except json.JSONDecodeError:
        log.warning("Could not parse LLM response — using empty filter.")
        return {"filter": {}, "sort": None}
    except Exception as e:
        log.error("LLM error: %s", e)
        return {"filter": {}, "sort": None}
