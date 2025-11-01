import sys
import os

def get_char() -> str:
    """
    Read one character from stdin without pressing Enter.
    Returns:
        str: The character read from stdin.
    """
    ch = ""
    try:
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except ImportError:
        import msvcrt
        raw_ch = msvcrt.getch()
        if raw_ch == b'\x1b':
            ch = '\x1b'
        elif raw_ch in (b'\x00', b'\xe0'):
            msvcrt.getch()
            ch = ""
        else:
            ch = raw_ch.decode("utf-8")
    return ch


def search_loop(bst: 'BST') -> None:
    """
    Prompts the user to type a word, and it will display the first 7 autocomplete suggestions
    from a given knowledge base dictionary. The loop runs until the user is pressing ESC to quit.
    Args:
        bst (BST): The binary search tree containing the dictionary words.
    Returns:
        None
    """
    prefix = ""
    while True:
        ch = get_char()

        if not ch:
            continue

        if ord(ch) == 27:
            print("\nExiting...")
            break

        if ch in ("\b", "\x7f"):
            prefix = prefix[:-1]
        elif ch == "\r":
            continue
        else:
            prefix += ch.lower()

        os.system("cls" if os.name == "nt" else "clear")
        print(f"Search for >> {prefix}")
        suggestions = bst.autocomplete(prefix)
        if suggestions:
            for s in suggestions[:7]:
                print(s)
        else:
            print("No matches found.")
        print("\n(Press ESC to quit)")
