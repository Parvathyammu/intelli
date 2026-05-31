from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from langchain_groq import ChatGroq

import os
import json

# 🔥 YOUR PIPELINE
from pipeline import run_pipeline

load_dotenv()

# ---------------- CONFIG ----------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL")

# ---------------- APP ----------------

app = Flask(__name__)
CORS(app, origins=[FRONTEND_URL] if FRONTEND_URL else "*")

# ---------------- LLM ----------------

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

# --------------------------------------------------
# ANSWER GENERATION (NEW CORE)
# --------------------------------------------------

def generate_final_answer(query, pipeline_data):

    context = json.dumps(pipeline_data, indent=2)

    prompt = f"""
You are an intelligent environmental AI assistant.

Use the given structured data to answer the user clearly.

User Query:
{query}

Data:
{context}

Instructions:
- Combine all relevant data (MOSDAC, scraped content, weather, ocean)
- Give a clear, human-readable answer
- Be precise and informative
- If some data is missing, still fill answer using what you know and Don't say no relevant data found say as limited data
- Be concise and factual
- Don't mention about unwanted links even if its provided.
- Prefer bullet points or short sentences
- If there is multiple values for same thing take the average and combine
- Maximum remove bold

Final Answer:
"""

    try:
        return llm.invoke(prompt).content.strip()
    except Exception as e:
        print("LLM error:", e)
        return "Error generating response."


# --------------------------------------------------
# API ROUTE
# --------------------------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Query required"}), 400

    # 🔥 STEP 1: RUN PIPELINE
    pipeline_result = run_pipeline(query)

    # 🔥 STEP 2: LLM FINAL ANSWER
    answer = generate_final_answer(query, pipeline_result)

    return jsonify({
        "answer": answer,
        "data": pipeline_result  # optional debug (remove in prod)
    })


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)