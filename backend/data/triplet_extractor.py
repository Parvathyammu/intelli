from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def extract_triplets(text):
    
    prompt = f"""
Extract triplets (subject, predicate, object) from the text.

Return ONLY JSON like this:
[
 {{"subject":"...","predicate":"...","object":"..."}}
]

Text:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    content = response.choices[0].message.content

    try:
        triplets = json.loads(content)
        return triplets
    except:
        print("JSON parsing failed")
        print(content)
        return []


# Example text
text = """
Space Applications Centre (SAC) is an ISRO Centre located in Ahmedabad.
MOSDAC is a data centre of SAC.
MOSDAC provides satellite data for meteorology and oceanography research.
"""

triplets = extract_triplets(text)

for t in triplets:
    print(f"{t['subject']} -- {t['predicate']} --> {t['object']}")