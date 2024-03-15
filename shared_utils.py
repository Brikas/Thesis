import tiktoken
from typing import List, Dict
from openai import OpenAI
import os

def count_tokens(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def gpt(messages: list[Dict], model: str = "gpt-3.5-turbo", kwargs: dict = {}) -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    r = client.chat.completions.create(
        messages=messages,
        **kwargs,
        model=model,
    )
    return r.choices[0].message.content


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