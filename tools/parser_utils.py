
import json
import re
from typing import Any

def clean_and_parse_json(raw_text: str) -> Any:
    """
    Cleans markdown wrappers (like ```json ... ```) from LLM responses
    and safely extracts the nested JSON object.
    """
    # Remove whitespace from ends
    cleaned = raw_text.strip()
    
    # Use Regex to look for anything between the first '{' and the last '}'
    match = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if match:
        json_content = match.group(0)
    else:
        json_content = cleaned

    try:
        return json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse invalid JSON string. Raw response was:\n{raw_text}") from e