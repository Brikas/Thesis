import tiktoken
from typing import List, Dict
from openai import OpenAI
import os
import numpy as np
from numpy.linalg import norm

def count_tokens(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens

# find cosine similarity of every chunk to a given embedding
def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

# Prompt builder
def userMsg(*args) -> dict:
    return {"role": "user", "content": "\n".join(args)}
def assistantMsg(*args) -> dict:
    return {"role": "assistant", "content": "\n".join(args)}
def systemMsg(*args) -> dict:
    return {"role": "system", "content": "\n".join(args)}


BLACKLIST_CHAT_REGEX_FILTERS = [
    {
        "id": "link-filter",
        "pattern": r"https.*"
    },
    {
        "id": "react-filter",
        "pattern": r"Reacted\s.*\sto\syour\smessage"
    },
    {
        "id": "cookie-data-filter",
        "pattern": r"\b\w{101,}\b"
    }
]

BLACKLIST_ANSWER_SUBSTRINGS = [
    "\."
]

