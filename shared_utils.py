import tiktoken
from typing import List, Dict
from openai import OpenAI
import os

def count_tokens(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


BLACKLIST_CHAT_REGEX_FILTERS = [
    {
        "id": "link-filter",
        "pattern": r"https.*"
    },
    {
        "id": "react-filter",
        "pattern": r"Reacted\s.*\sto\syour\smessage"
    }
]

BLACKLIST_ANSWER_SUBSTRINGS = [
    "\."
]