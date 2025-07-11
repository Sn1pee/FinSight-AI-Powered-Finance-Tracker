import os
from openai import OpenAI
import pandas as pd

_GH_TOKEN = os.getenv("GITHUB_TOKEN")  # throws KeyError if missing
_ENDPOINT = "https://models.github.ai/inference"
_MODEL_ID = "openai/gpt-4.1"

_client = OpenAI(
    base_url=_ENDPOINT,
    api_key=_GH_TOKEN,
)


def _build_prompt(summary: dict[str, any]) -> str:
    """
    Turn the numeric summary returned by analyzer.py into a prompt
    the model can understand.
    """
    income   = summary["income"]
    expense  = summary["expense"]
    savings  = summary["savings"]
    cat_tbl: pd.Series = summary["category_summary"]   # pandas Series

    return f"""
You are FinSight, an upbeat bilingual English personal-finance coach for Indian users.
Given the month's money summary below, respond in ~6-8 lines:
• 2-line high-level recap (English)
• bullet list (max 3) of biggest expense drains  
• 2 personalised saving tips  
• end with one motivational one-liner

Generate detailed insights for the user based on the summary below:
be more professional like talking to an acutal trader/inverstor

💰  Summary
Income  : ₹{income:,.2f}
Expense : ₹{expense:,.2f}
Savings : ₹{savings:,.2f}

- while giving summary add some funny lines/tips to make it engaging.
- speak like you are talking to a friend, no formal tone.

Category-wise debit:
{cat_tbl.to_string()}

Remember: be friendly, no lecture vibes, sprinkle one emoji.
"""

def generate_insights(summary: dict[str, any]) -> str:
    """
    Returns a string containing AI-generated insights for the
    dashboard.  Raises RuntimeError on API issues so the UI can
    handle errors gracefully.
    """
    try:
        chat = _client.chat.completions.create(
            model=_MODEL_ID,
            temperature=0.9,
            top_p=1.0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are FinSight, a friendly bilingual personal-finance coach. "
                        "Keep responses concise, actionable, and engaging."
                    ),
                },
                {
                    "role": "user",
                    "content": _build_prompt(summary),
                },
            ],
        )
        return chat.choices[0].message.content.strip()
    except Exception as exc:

        raise RuntimeError("AI insight generation failed") from exc
