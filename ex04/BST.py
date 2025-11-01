import urllib.request


class Node:
    def __init__(self, word: str):
        self.word: str = word
        self.left: 'Node' = None
        self.right: 'Node' = None


class BST:
    def __init__(self, source: str, **kwargs):
        self.root: Node = None
        self.results: list[str] = []

        url_option = kwargs.get('url', False)
        file_option = kwargs.get('file', False)

        wordlist = []

        if url_option and file_option:
            raise ValueError("Both 'url' and 'file' options cannot be True.")

        if url_option:
            try:
                print(f"Fetching wordlist from URL: {source}...")
                with urllib.request.urlopen(source) as response:
                    data = response.read()
                content = data.decode('utf-8').strip()
                wordlist = content.split('\n')
                print("Wordlist fetched.")
            except Exception as e:
                print(f"Error fetching URL: {e}")
                wordlist = []

        elif file_option:
            try:
                print(f"Reading wordlist from file: {source}...")
                with open(source, 'r', encoding='utf-8') as f:
                    wordlist = [line.strip() for line in f if line.strip()]
                print("Wordlist read successfully.")
            except Exception as e:
                print(f"Error reading file: {e}")
                wordlist = []

        if wordlist:
            self.root = self._build_balanced_bst(wordlist, 0, len(wordlist) - 1)
            print("BST constructed.")

    def _build_balanced_bst(self, words: list[str], start: int, end: int) -> Node:
        if start > end:
            return None

        mid = (start + end) // 2
        node = Node(words[mid])

        node.left = self._build_balanced_bst(words, start, mid - 1)
        node.right = self._build_balanced_bst(words, mid + 1, end)

        return node

    def autocomplete(self, prefix: str) -> list[str]:
        self.results = []
        if self.root:
            self._collect(self.root, prefix.lower())
        return self.results

    def _collect(self, node: Node, prefix: str) -> None:
        if node is None:
            return

        word = node.word
        lower_word = word.lower()

        if prefix > lower_word and lower_word.startswith(prefix) is False:
            self._collect(node.right, prefix)
            return

        self._collect(node.left, prefix)

        if lower_word.startswith(prefix):
            self.results.append(word)

        if lower_word.startswith(prefix):
            self._collect(node.right, prefix)