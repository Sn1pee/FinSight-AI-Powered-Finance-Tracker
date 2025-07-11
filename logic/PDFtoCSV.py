import os
from openai import OpenAI

_API_KEY = os.getenv("GITHUB_TOKEN") or os.getenv("FINSIGHT_API_KEY")
_ENDPOINT = "https://models.github.ai/inference"
_MODEL = "openai/gpt-4.1"

client = OpenAI(
    base_url=_ENDPOINT,
    api_key=_API_KEY,
)

def convert_pdf_to_csv(payload: dict) -> str:
    """
    Given a dict with 'text' key (raw PDF text), returns a clean CSV string
    with columns: Date, Description, Amount, Type.
    Type must be either Debit or Credit.
    """
    if "text" not in payload:
        raise ValueError("Missing 'text' in payload")

    raw_text = payload["text"]

    prompt = f"""
I have pasted below a raw bank statement or credit card transaction history extracted from a PDF:

-------------------------
{raw_text.strip()[:3000]}  # Truncated to keep it within token limits
-------------------------

Instructions:
• Extract and clean the data into a CSV format with columns: Date, Description, Amount, Type
• The Type should be either Debit or Credit
• Amounts should be pure numbers (no ₹ or commas)
• Return only the CSV. Do not explain anything. No Markdown. No extra text.
"""

    try:
        response = client.chat.completions.create(
            model=_MODEL,
            temperature=0.2,
            top_p=1.0,
            messages=[
                {"role": "system", "content": "You are a strict CSV parser bot. Output only CSV, no extra explanations."},
                {"role": "user", "content": prompt}
            ]
        )
        csv_output = response.choices[0].message.content.strip()
        return csv_output

    except Exception as e:
        raise RuntimeError(f"PDF to CSV conversion failed: {e}")
