# 8-Puzzle Solver (BFS) — Line-by-Line Code Walkthrough

## 1. Imports and Setup

```python
from collections import deque
```

- Imports `deque` (double-ended queue) from Python's `collections` module.
- BFS needs a **queue (FIFO — First In, First Out)**, and `deque` gives fast
  `O(1)` operations on both ends — `popleft()` (dequeue from the front) and
  `append()` (enqueue at the back) — unlike a plain list, where `pop(0)` is
  slow (`O(n)`).

```python
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
```

- Defines the target configuration as a flat tuple of 9 numbers (0 = blank
  tile), representing this grid:

```
1 2 3
4 5 6
7 8 _
```

- A **tuple** (not a list) is used because tuples are hashable — they can be
  stored inside a `set` (for `visited`) and used as dictionary/set keys,
  whereas lists cannot.

```python
OFFSETS = [(-3, "Up"), (3, "Down"), (-1, "Left"), (1, "Right")]
```

- Defines the four possible moves as `(index_shift, move_name)` pairs.
- **This is explained in full detail in Section 4 below — it's the part you
  asked about.**

## 2. Function Definition and Queue Initialization

```python
def solve_8_puzzle(start):
```

- Defines the solver function, taking the `start` board (a 9-element tuple)
  as input.

```python
    queue = deque([(start, [])])
```

- Initializes the BFS queue with one entry: `(start, [])`.
  - `start` — the starting board configuration.
  - `[]` — the empty list of moves taken so far (the path is empty because
    no move has been made yet).

```python
    visited = {start}
```

- Initializes a `set` containing the start board, to make sure we never
  revisit an already-explored configuration (prevents infinite loops and
  redundant work).

## 3. The Main BFS Loop

```python
    while queue:
```

- Keeps looping as long as there are unexplored boards left in the queue.
  If the queue empties without finding the goal, the loop ends and the
  function falls through to `return None`.

```python
        board, path = queue.popleft()
```

- Removes and returns the **oldest** entry in the queue (`popleft()` takes
  from the front — this is what makes it BFS, not DFS).
- Unpacks it into `board` (the current configuration) and `path` (the list
  of moves that led here).

```python
        if board == GOAL:
            return path
```

- Goal check: if the board we just pulled out of the queue matches `GOAL`,
  we're done — return the sequence of moves that produced it. Because BFS
  explores level-by-level (by number of moves), this path is guaranteed to
  be the **shortest possible** solution.

```python
        zero = board.index(0)
        r, c = zero // 3, zero % 3
```

- `board.index(0)` finds the flat index (0–8) of the blank tile in the
  9-element tuple.
- `zero // 3` (integer division) gives the **row** (0, 1, or 2).
- `zero % 3` (modulo/remainder) gives the **column** (0, 1, or 2).
- Example: if `zero = 5`, then `r = 5 // 3 = 1`, `c = 5 % 3 = 2` → row 1,
  column 2 (the rightmost tile of the middle row).

## 4. Generating Moves — and Answering Your Question

```python
        for shift, action in OFFSETS:
            new_zero = zero + shift
```

This loop tries all four moves by adding a `shift` value to the blank's flat
index. This is where your question comes in.

### ❓ Why does `OFFSETS` use `3` and `1`, specifically?

The board is a **3×3 grid**, but it's stored as a **flat 1D tuple of 9
elements** (indices `0` through `8`), like this:

```
Flat index:       0   1   2   3   4   5   6   7   8
Grid position:  (0,0)(0,1)(0,2)(1,0)(1,1)(1,2)(2,0)(2,1)(2,2)
                 └─────row 0─────┘└─────row 1─────┘└─────row 2─────┘
```

Because each **row has exactly 3 elements**, moving between rows means
jumping **3 flat-index positions**, and moving within a row (left/right)
means shifting by **1 flat-index position**:

| Move | What it does on the grid | Flat-index effect | Why |
|---|---|---|---|
| **Up** | Move to the row above | `index - 3` | Skip back one full row of 3 tiles |
| **Down** | Move to the row below | `index + 3` | Skip forward one full row of 3 tiles |
| **Left** | Move to the previous column | `index - 1` | Previous element in the flat array |
| **Right** | Move to the next column | `index + 1` | Next element in the flat array |

**Concrete example:** blank is at flat index `4` (row 1, col 1 — the exact
center tile).

```
0 1 2
3 4 5
6 7 8
```

- `Up` → `4 - 3 = 1` → row 0, col 1 (directly above). ✔
- `Down` → `4 + 3 = 7` → row 2, col 1 (directly below). ✔
- `Left` → `4 - 1 = 3` → row 1, col 0 (directly left). ✔
- `Right` → `4 + 1 = 5` → row 1, col 2 (directly right). ✔

**In short: `3` is the grid's width (row length), so `±3` moves you
vertically by one row; `1` is a single flat-array step, so `±1` moves you
horizontally by one column.** If this were a 4×4 puzzle (15-puzzle), the
vertical shift would need to be `±4` instead of `±3`, since each row would
then contain 4 elements.

## 5. Boundary Checks

```python
            if 0 <= new_zero < 9:
```

- First safety check: makes sure `new_zero` is a valid flat index
  (`0` to `8`). Without this, `Up` from row 0 (e.g., index `1 - 3 = -2`) or
  `Down` from row 2 (e.g., index `7 + 3 = 10`) would produce an out-of-range
  index and crash the program.

```python
                if action == "Left" and c == 0: continue
                if action == "Right" and c == 2: continue
```

- Second safety check, specifically for `Left`/`Right`. This catches a
  subtler bug the `0 <= new_zero < 9` check **cannot** catch: row-wrapping.
  - Example: blank at flat index `2` (row 0, col 2, the top-right tile).
    `Right` → `2 + 1 = 3`, which **is** within `0–8`, but flat index `3` is
    actually row 1, col 0 — the far-left tile of the *next* row, not a real
    right-neighbor!
  - `if action == "Left" and c == 0: continue` — skip `Left` if we're
    already in column 0 (leftmost column, nowhere further left to go).
  - `if action == "Right" and c == 2: continue` — skip `Right` if we're
    already in column 2 (rightmost column, nowhere further right to go).
  - `continue` skips the rest of this loop iteration and moves on to the
    next offset in `OFFSETS`.

## 6. Applying the Move

```python
                b = list(board)
```

- Converts the immutable `board` tuple into a mutable `list`, since tuples
  cannot have their elements reassigned directly.

```python
                b[zero], b[new_zero] = b[new_zero], b[zero]
```

- Swaps the blank tile (`0`) at position `zero` with the tile at
  `new_zero` — this is the actual "slide" move. Python's tuple-assignment
  syntax performs the swap in a single line without needing a temporary
  variable.

```python
                nxt = tuple(b)
```

- Converts the modified list back into a tuple (`nxt`), so it can be
  compared, hashed, and stored in the `visited` set again.

```python
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [action]))
```

- Only proceeds if this new configuration hasn't been seen before.
- Marks it visited immediately (important: marking it *here*, not later,
  prevents the same state from being queued multiple times before it's ever
  processed).
- Pushes `(nxt, path + [action])` onto the **back** of the queue —
  `path + [action]` creates a new list with the current move appended,
  without mutating the original `path` (so other branches of the search
  keep their own independent history).

## 7. No Solution Case

```python
    return None
```

- If the `while queue` loop exits because the queue became empty (every
  reachable configuration was explored and none matched `GOAL`), the
  function returns `None`, signaling no solution exists from this start
  state (this can genuinely happen — only exactly half of all possible
  8-puzzle configurations are solvable).

## 8. Driver Block

```python
if __name__ == "__main__":
    start_board = (1, 2, 3, 0, 4, 6, 7, 5, 8)

    moves = solve_8_puzzle(start_board)
    print("Solved in", len(moves), "moves!")
    print("Path:", " -> ".join(moves))
```

- `start_board` represents:
  ```
  1 2 3
  0 4 6
  7 5 8
  ```
- Calls `solve_8_puzzle` and stores the returned list of move-names in
  `moves`.
- `len(moves)` counts how many moves were needed — printed as the solution
  length.
- `" -> ".join(moves)` glues the move names together with arrows for a
  readable path, e.g.: `"Right -> Down -> Right"`.