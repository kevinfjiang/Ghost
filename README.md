# Optimal [Ghost](https://en.wikipedia.org/wiki/Ghost_(game))

## Solution:
Used a Trie to create a pseudo search dictionary of the words provided. Added each given word to the dictionary. Then we compute the winners of the game for each word using a Trie DFS. Following, we then find the optimal word using another DFS but only pursuing a path from the head node to end where Player.YOU is always the winner, meaning a forced win. 

## Methods:
`Trie.add_word()`: Adds a word to the Trie dictionary and if a word is shorter in length, trims all subsequent branches.

Time Complexity: O(m) where m is the length of the word

Space Complexity: O(m) 

Use case: Since we add n words to the Trie, we would expect the total time complexity to be O(mn)

`Trie.update_winners()`: Updates the winner of each level with a DFS by determining the optimal move for a given level and having the turn player make that move. 

Time Complexity: O(mn) or O(number of nodes)

Space Complexity: O(mn) as the data structure is O(mn). Arguably additional O(m) space for the stack frames due to recursion.

`Trie.find_a_winner()`: Follows a branch of which the nodes have winner Player.YOU to find a solution. This will be a forced win. 

Time Complexity: O(m) where m is the length of the winning word

Space Complexity: O(m) where m is the length of the winning word. From the string created and the stack frames from recursion

`Trie.find_prefix()`: Traverses down the prefix and find the Node where we start at the given prefix. Returns another Trie so we can start the traversal from that Trie and have all the above functions.

Time Complexity: O(m) where m is length of prefix

Space Complexity: O(m) as we may need to create new Trie nodes for the word. Nodes have a fixed size.
