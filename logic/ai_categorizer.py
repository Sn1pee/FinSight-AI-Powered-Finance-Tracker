import os
import pandas as pd
from openai import OpenAI

_API_KEY  = os.getenv("GITHUB_TOKEN") or os.getenv("FINSIGHT_API_KEY")
_ENDPOINT = "https://models.github.ai/inference"
_MODEL    = "openai/gpt-4.1"

client = OpenAI(base_url=_ENDPOINT, api_key=_API_KEY)

SYSTEM_MSG = (
    "You are a finance‑savvy assistant. "
    "Given a CSV of transactions, add an intelligent Category column "
    "using common spending classes like Food, Transport, Shopping, Utilities, Entertainment, Income, Others. "
    "Return ONLY the CSV."
)

def categorize_with_ai(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the DataFrame (without index) to CSV text for the prompt
    csv_no_header = df.to_csv(index=False)
    prompt = (
        "Categorise each row. "
        "Return the same CSV with an extra column named Category.\n\n"
        + csv_no_header[:4500]        # truncate for token safety
    )

    resp = client.chat.completions.create(
        model=_MODEL,
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": prompt},
        ],
    )

    new_csv = resp.choices[0].message.content.strip()
    new_df  = pd.read_csv(pd.io.common.StringIO(new_csv))
    return new_df
import os
import pandas as pd
from openai import OpenAI

_API_KEY  = os.getenv("GITHUB_TOKEN") or os.getenv("FINSIGHT_API_KEY")
_ENDPOINT = "https://models.github.ai/inference"
_MODEL    = "openai/gpt-4.1"

client = OpenAI(base_url=_ENDPOINT, api_key=_API_KEY)

SYSTEM_MSG = (
    "You are a finance‑savvy assistant. "
    "Given a CSV of transactions, add an intelligent Category column "
    "using common spending classes like Food, Transport, Shopping, Utilities, Entertainment, Income, Others. "
    "Return ONLY the CSV."
)

def categorize_with_ai(df: pd.DataFrame) -> pd.DataFrame:
    # Convert the DataFrame (without index) to CSV text for the prompt
    csv_no_header = df.to_csv(index=False)
    prompt = (
        "Categorise each row. "
        "Return the same CSV with an extra column named Category.\n\n"
        + csv_no_header[:4500]        # truncate for token safety
    )

    resp = client.chat.completions.create(
        model=_MODEL,
        temperature=0.0,
        messages=[
            {"role": "system", "content": SYSTEM_MSG},
            {"role": "user", "content": prompt},
        ],
    )

    new_csv = resp.choices[0].message.content.strip()
    new_df  = pd.read_csv(pd.io.common.StringIO(new_csv))
    return new_df
