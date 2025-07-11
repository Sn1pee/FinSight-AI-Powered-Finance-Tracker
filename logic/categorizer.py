def categorize(description: str) -> str:
    description = description.lower()
    if "swiggy" in description or "zomato" in description or "cafe" in description:
        return "Food"
    elif "uber" in description or "ola" in description:
        return "Transport"
    elif "amazon" in description:
        return "Shopping"
    elif "netflix" in description or "prime" in description:
        return "Entertainment"
    elif "electricity" in description or "bill" in description:
        return "Utilities"
    elif "salary" in description or "freelance" in description:
        return "Income"
    else:
        return "Others"
