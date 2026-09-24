# A* Search Algorithm — Line-by-Line Code Walkthrough

## 1. Function Definition

```python
def astar(graph, h, start, goal):
```

- Defines the A* search function.
- `graph`: a dictionary representing a **directed, weighted graph** — each
  key is a node, and its value is a list of `(neighbor, edge_cost)` pairs.
- `h`: a dictionary of **heuristic estimates** — `h[node]` is the estimated
  cost from that node to the goal (must be admissible, i.e. never an
  overestimate, for A* to guarantee the optimal path).
- `start`: the node to begin searching from.
- `goal`: the node we're trying to reach.

## 2. Initializing the Open List

```python
    open = [(start, 0, [start])]
```

- `open` is the **frontier** — the list of nodes discovered but not yet
  fully processed. (Note: `open` shadows Python's built-in `open()`
  function; it works here but isn't best practice — `open_list` would be
  safer.)
- It starts with a single entry: `(start, 0, [start])`.
  - `start` — the current node.
  - `0` — the cost `g(n)` accumulated so far to reach this node (zero,
    since we haven't moved yet).
  - `[start]` — the path taken so far, as a list (just the start node
    itself right now).

## 3. Main Search Loop

```python
    while open:
```

- Keeps looping as long as there are unexplored entries in `open`. If
  `open` becomes empty before the goal is found, the loop ends and the
  function falls through to `return None, None`.

```python
        current, cost, path = min(
            open,
            key=lambda x: x[1] + h[x[0]]
        )
```

- This is the **heart of A\***: pick the entry in `open` with the smallest
  $f(n) = g(n) + h(n)$.
- `min(open, key=...)` scans every tuple in `open` and returns the one that
  minimizes the `key` function.
- `key=lambda x: x[1] + h[x[0]]` computes, for each tuple `x`:
  - `x[1]` → the tuple's second element, `cost`, which is $g(n)$.
  - `h[x[0]]` → look up the heuristic for the tuple's first element (the
    node), which is $h(n)$.
  - Their sum is $f(n) = g(n) + h(n)$ — exactly A*'s priority formula.
- The winning tuple is unpacked into `current` (the node), `cost` (its
  $g(n)$), and `path` (the route taken to reach it).
- **Note on efficiency:** using `min()` over a plain list re-scans the
  entire `open` list every iteration — `O(n)` per pick. A production
  implementation would use a **priority queue / heap** (`heapq`) for
  `O(log n)` picks instead, but this simpler version is easier to read and
  trace by hand.

```python
        open.remove((current, cost, path))
```

- Removes the chosen tuple from `open`, since it's now being processed
  (it moves conceptually from the "frontier" into the "explored" set).

## 4. Goal Check

```python
        if current == goal:
            return path, cost
```

- If the node just popped is the goal, we're done. Because A* always
  expands the lowest-$f(n)$ node next (and the heuristic is admissible),
  the first time we pop the goal, the `path` found is guaranteed to be the
  **optimal (lowest-cost)** path. Returns the path (list of nodes) and its
  total cost.

## 5. Expanding Neighbors

```python
        for next, d in graph[current]:
```

- Looks up all outgoing edges from `current` in the graph dictionary.
- Each edge is unpacked into `next` (the neighboring node) and `d` (the
  cost/distance of that edge).
- Example: if `current = 'A'`, `graph['A']` is `[('B', 1), ('C', 4)]`, so
  this loop runs twice: once with `next='B', d=1`, once with
  `next='C', d=4`.

```python
            if next not in path:
```

- A simple **cycle-prevention check**: only consider this neighbor if it
  isn't already part of the current path (i.e., we haven't already visited
  it *on this specific route*). This stops the search from looping back on
  itself infinitely.
- Note: this checks membership in `path` (the route so far), not a global
  `visited` set — so the *same* node can still be explored again later via
  a *different* path with different cost, which is safe but a bit less
  efficient than a global visited-set + re-open-if-cheaper strategy used in
  more optimized A* implementations.

```python
                open.append(
                    (next, cost + d, path + [next])
                )
```

- Adds a new frontier entry for this neighbor:
  - `next` — the neighboring node.
  - `cost + d` — the new $g(n)$: the cost to reach `current`, plus the
    edge cost to get to `next`.
  - `path + [next]` — a **new** list (the `+` operator creates a fresh
    list rather than mutating `path`), containing the route so far with
    `next` appended. This ensures other branches keep their own
    independent path history.

## 6. No Path Found

```python
    return None, None
```

- If the `while open:` loop exits because `open` became empty (every
  reachable node was explored and the goal was never popped), the function
  returns `(None, None)`, signaling that no path exists from `start` to
  `goal`.

## 7. Driver Block — Setting Up the Graph and Heuristics

```python
if __name__ == "__main__":

    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('D', 2), ('E', 5)],
        'C': [('E', 1)],
        'D': [('G', 3)],
        'E': [('G', 2)],
        'G': []
    }
```

- Defines a directed, weighted graph as an **adjacency list**. For example,
  `'A': [('B', 1), ('C', 4)]` means: from `A`, you can go to `B` at cost 1,
  or to `C` at cost 4. `'G': []` means `G` has no outgoing edges (it's the
  goal / a dead end going forward).

Visualized:
```
        A
      /1  \4
     B      C
   /2  \5   |1
  D      E--
  |3      |2
   \      /
    \    /
     \  /
      G
```

```python
    h = {
        'A': 6,
        'B': 5,
        'C': 3,
        'D': 3,
        'E': 2,
        'G': 0
    }
```

- Defines the heuristic estimate from each node to the goal `G`. Note
  `h['G'] = 0`, which must always be true — the estimated distance from the
  goal to itself is zero.

```python
    start = input("Start: ").strip().upper()
    goal = input("Goal: ").strip().upper()
```

- Prompts the user to type a start node and a goal node.
- `.strip()` removes any accidental leading/trailing whitespace (e.g., if
  the user typed `" a "` with spaces).
- `.upper()` converts the input to uppercase, so typing `a` still correctly
  matches the graph's `'A'` key (the dictionaries use uppercase letters).

```python
    path, cost = astar(graph, h, start, goal)
```

- Calls `astar()` with the graph, heuristics, and the user's chosen start
  and goal nodes, then unpacks the returned tuple into `path` and `cost`.

```python
    if path:
        print("Path:", " -> ".join(path))
        print("Cost:", cost)
    else:
        print("No valid path exists between the given nodes.")
```

- `if path:` checks whether a path was actually found. If `astar()`
  returned `None` (no path), this condition is `False` since `None` is
  "falsy" in Python.
- If a path exists: `" -> ".join(path)` glues the list of node names
  together with arrows (e.g., `"A -> B -> D -> G"`), and prints it along
  with the total cost.
- If no path exists: prints a friendly failure message instead of crashing
  on `None`.

## 8. Worked Trace (Start = A, Goal = G)

| Step | Popped (lowest f) | g(n) | h(n) | f(n) | Path so far |
|---|---|---|---|---|---|
| 1 | A | 0 | 6 | 6 | [A] |
| 2 | B (via A) | 1 | 5 | 6 | [A, B] |
| 3 | D (via A→B) | 3 | 3 | 6 | [A, B, D] |
| 4 | G (via A→B→D) | 6 | 0 | 6 | [A, B, D, G] ✅ |

**Result:** `Path: A -> B -> D -> G`, `Cost: 6`

(Note: `E` and `C` branches also get added to `open` along the way, e.g.
`A→C` at cost 4 and `A→B→E` at cost 6, but they're never popped because a
path reaching `G` with equal-or-lower `f(n)` is found first.)