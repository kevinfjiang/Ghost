from enum import Enum, auto
from typing import List, Optional, Self


class Player(Enum):
    YOU = auto()
    OTHER = auto()
    UNKNOWN = auto()

    def change_turn(self) -> Self:
        if self == Player.UNKNOWN:
            raise NotImplementedError(f"{Player.UNKNOWN} is for unitialized states")
        return Player.OTHER if self == Player.YOU else Player.YOU


class Trie:
    """Trie with additional methods to solve the game Ghost optimally"""

    class Node:
        """Node of Trie, with rbase leaves"""

        def __init__(self, rbase: int = 26):
            self.letters: List[Optional[Trie.Node]] = [None for _ in range(rbase)]
            self.winner: Player = Player.UNKNOWN  # Winner of current level
            self.ender = False  # If current level is an ending word

    def __init__(
        self,
        first_move: bool = True,
        rbase: int = 26,
        refchar: str = "a",
        pref: str = "",
        head: Optional[Node] = None,
    ):
        self.rbase = rbase
        self.first_move = first_move
        self.refchar = refchar
        self.pref = pref

        self.head = Trie.Node(rbase) if head is None else head

    def _pos(self, char: str) -> int:
        return ord(char) - ord(self.refchar)

    def _char(self, pos: int) -> str:
        return chr(pos + ord(self.refchar))

    def find_prefix(self, prefix: str) -> Self:
        """Traverses trie according to prefix and returns a wrapper around current node

        :param str prefix: Specified prefix of starting word
        :return Trie: Trie to traverse and find next best word
        """
        curr = self.head

        for letter in prefix:
            if curr.ender or curr.letters[self._pos(letter)] is None:
                raise Exception("No word with prefix found")

            # Traverses and adds word to Trie, mypy error with guard clause
            curr = curr.letters[self._pos(letter)] # type: ignore

        # Wraps remaining nodes in a new Trie
        return Trie(
            self.first_move != len(prefix) % 2,
            self.rbase,
            self.refchar,
            self.pref + prefix,
            curr,
        )

    def add_word(self, word: str) -> None:
        """Adds a word to the search dictionary. Labels the end of the word
        if at the end, there's words that use the base, the following leaves
        are pruned because game ends at any end of word. O(n) time where n
        is length of word. O(n) space added, as for every new letter,
        we create another constant size dictionary per letter.

        :param str word: Any lowercase word
        """
        curr = self.head

        for letter in word:
            if curr.ender:
                break

            if curr.letters[self._pos(letter)] is None:
                curr.letters[self._pos(letter)] = Trie.Node(self.rbase)

            # Traverses and adds word to Trie, mypy error with guard clause
            curr = curr.letters[self._pos(letter)]  # type: ignore

        curr.ender = True
        # Cleans out leaves of finishing letter
        curr.letters = [None for _ in range(len(curr.letters))]
        return

    def update_winners(self) -> None:
        """Depth first search with alternating winners. Labels each node with what move
        an optimal turn player would make. O(n) time DFS where n is number of nodes.

        :param bool odd_winner: Determines if you're starting on odd letter or even,
        defaults to True
        """

        def recurse_update(curr_node: Trie.Node, turn_player: Player) -> None:
            """Recursive update of Trie DFS. Will traverse to lowest word and determine
            the winner. At parents, determines the winner for optimal turn player

            :param Trie.Node curr_dict: Current word level
            :param Player turn_player: Current player, either Player.YOU or Player.OTHER
            """
            if curr_node.ender:
                curr_node.winner = turn_player

            for letter in curr_node.letters:  # DFS
                if letter is None:
                    continue
                recurse_update(letter, turn_player.change_turn())
                # Checks if there's a move where turn_player forces a win
                curr_node.winner = (
                    turn_player if letter.winner == turn_player else curr_node.winner
                )

            if curr_node.winner == Player.UNKNOWN:
                # If determined that there's no forcing winning move, meaning
                # Only forcing winning moves for non-turn player
                curr_node.winner = turn_player.change_turn()

            return

        recurse_update(self.head, Player.YOU if self.first_move else Player.OTHER)

    def find_a_winner(self) -> str:
        """Finds optimal move for Player.YOU through a DFS of the Trie.
        This is an O(m) time and space where m is length of optimal word.

        :return str: Forced winning word for Player.YOU. Returns "No valid winner" if no
        valid words
        """

        def recurse_search(curr: Trie.Node) -> str:
            leaf_index = -1  # Determines if we're at a forced win/ender point
            for i, letter in enumerate(curr.letters):
                if letter is None or letter.winner == Player.OTHER:
                    continue

                # Must be on level with only ender word choices to return a char
                leaf_index = i if letter.ender and leaf_index >= -1 else -2

                # DFS, searches for a forced winning word, if it exists,
                # Adds current character to recreate the word bottom up
                return f"{self._char(i)}{recurse_search(letter)}"

            # We've hit a forced win point, and the index gets char of win
            if leaf_index >= 0:
                return self._char(leaf_index)
            # Nothing of use found, most likely a deadend leading to Player.OTHER victory
            return ""

        return (
            f"Winning word: {self.pref}{recurse_search(self.head)}"
            if self.head.winner == Player.YOU
            else "No valid winning word"
        )


def test(prefix: str, words: List[str]) -> str:
    d = Trie(True)

    for word in words:
        d.add_word(word)

    d = d.find_prefix(prefix)
    d.update_winners()

    return d.find_a_winner()


if __name__ == "__main__":
    print(test(prefix="h", words=["hote", "lone", "bone", "horsewewew", "horseew"]))
