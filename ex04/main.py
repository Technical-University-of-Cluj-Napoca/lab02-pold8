import sys
from BST import BST
from search_engine import search_loop


def main():
    WORDLIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt"

    search_tree = BST(WORDLIST_URL, url=True)

    search_loop(search_tree)


if __name__ == "__main__":
    main()