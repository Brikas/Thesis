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

def describe_prompts(final_prompts: List[List[Dict]]) -> Dict:
    total_all_prompt_tokens = 0 #used elsewhere too
    prompt_tokens_min = 0
    prompt_tokens_max = 0
    for p in final_prompts:
        pt = 0 # Prompt tokens
        for msg in p:
            pt += count_tokens(msg["content"])
        if prompt_tokens_min == 0 or pt < prompt_tokens_min:
            prompt_tokens_min = pt
        if pt > prompt_tokens_max:
            prompt_tokens_max = pt

        total_all_prompt_tokens += pt

    return {
        "total_all_prompt_tokens": total_all_prompt_tokens,
        "prompt_tokens_min": prompt_tokens_min,
        "prompt_tokens_max": prompt_tokens_max
    }

def describe_prompts_and_print(final_prompts: List[List[Dict]]) -> Dict:
    info = describe_prompts(final_prompts)

    print(f"Created {len(final_prompts)} prompts.")
    print(f"Average prompt size: {round(info['total_all_prompt_tokens']/len(final_prompts))} tokens.")
    print(f"Min prompt size: {info['prompt_tokens_min']}, Max prompt size: {info['prompt_tokens_max']}")
    return info


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

