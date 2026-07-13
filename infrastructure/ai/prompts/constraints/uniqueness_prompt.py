def build_uniqueness_constraint_prompt(
    existing_data: str
) -> str:

    return f"""
When generating new data, take into account the existing information:

{existing_data}


Uniqueness rules:

- Do not generate duplicates or highly similar items to the existing data.
- If a new item has the same purpose, meaning, use case, or description as an existing item, do not create it again.
- Do not create a seemingly new item by only changing the name or slightly modifying the description.
- If a generated item overlaps with existing data, replace it with a different and unique item.
- Look for new perspectives, use cases, characteristics, segments, or opportunities that are not already covered.
- Every generated item must provide additional value and introduce new information.
"""