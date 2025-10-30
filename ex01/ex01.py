from collections import defaultdict
from typing import List

def group_anagrams(str: list[str]) -> list[list[str]]:
    anagram_group = defaultdict(list)

    for word in str:
        key = tuple(sorted(word))
        anagram_group[key].append(word)

    return list(anagram_group.values())