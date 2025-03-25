import random
import re
from enum import Enum
from pathlib import Path
from typing import Pattern, Union


class RegexPatterns(Enum):
    MIX_POLISH_ENGLISH = r"[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ'-]{4,}"


def shuffle_text(text: str, pattern: Union[str, Pattern[str]]) -> str:
    """
    Mixes words in text using given pattern.
    Function mixes middle letters of words but keeps the first and last letter.

    Note: This function operates only on words with a minimum length of 3 letters.
    """
    for match_word in re.finditer(pattern, text):
        start, end = match_word.span()
        first_letter, *middle, last_letter = match_word.group()
        random.shuffle(middle)
        new_words = first_letter + "".join(middle) + last_letter
        text = text[:start] + new_words + text[end:]
    return text


def open_file_by_line(file_path: Union[str, Path]) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line


def process_file(file_path: Union[str, Path], pattern: Union[str, Pattern[str]]) -> str:
    """
    Processes file with given pattern.
    Function loads file and calls shuffle_text for each line and add it to the list.
    """
    text_lines = [shuffle_text(line, pattern) for line in open_file_by_line(file_path)]
    return "".join(text_lines)
