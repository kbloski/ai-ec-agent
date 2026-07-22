# OUTPUT RULES

## General Rules

- Follow the output format required by the task.
- Follow all task-specific instructions.
- Do not add unnecessary explanations, comments, or additional text.
- Keep the output consistent with the provided context.
- Do not copy the language of the input data.

## OUTPUT LANGUAGE

- Generate all text content in English.
- Keep technical terms, variable names, field names, and schema keys unchanged.
- Do not translate JSON keys or structured data fields.
- The output language is independent from the input language.

## JSON RULES

Apply these rules only when the required output format is JSON:

- Return only valid JSON.
- Do not add any text before or after the JSON object.
- Do not use markdown or code blocks.
- Follow the provided JSON schema exactly.
- Keep JSON keys unchanged.
- Do not rename, remove, or translate fields.
- Do not use null values.
- Do not leave required fields empty.
- All required fields must contain meaningful values.
- Arrays must always be returned as arrays.
- Objects must keep the structure defined by the schema.
- Do not replace objects with strings or arrays.
- Do not replace arrays with strings or objects.