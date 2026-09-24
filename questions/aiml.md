# AI Search Algorithms — Complete Study Notes
### Pass 1 of 4: Full Technical Detail (with code and diagrams)

> This document is being built in passes, as requested. This pass covers the
> full technical explanation of each algorithm/problem, the "what happens if"
> cross-analysis, and the NP-hard discussion. Later passes (simplified,
> combined, viva voce) can be requested as follow-ups and will reuse this same
> structure.

---

## PART A — The Five Algorithms / Problems

---

## 1. Depth First Search (DFS) for the Water Jug Problem

### Definition
The Water Jug Problem is a **state-space search problem**: given two jugs of
capacities $J_1$ and $J_2$ (no markings) and an infinite water source, find a
sequence of operations (fill, empty, pour) that produces an exact target
volume $T$ in either jug.

**DFS** solves it by exploring one path as deep as possible before
backtracking — implemented with a **stack (LIFO)** and a **visited set** to
avoid revisiting states.

### State Representation
A state is `(x, y)` = current water in Jug 1, Jug 2.

**Operations from state `(x, y)`:**
| Operation | Resulting state |
|---|---|
| Fill Jug 1 | `(J1, y)` |
| Fill Jug 2 | `(x, J2)` |
| Empty Jug 1 | `(0, y)` |
| Empty Jug 2 | `(x, 0)` |
| Pour Jug 1 → Jug 2 | `(x - min(x, J2-y), y + min(x, J2-y))` |
| Pour Jug 2 → Jug 1 | `(x + min(y, J1-x), y - min(y, J1-x))` |

### Code
```python
def dfs_water_jug(j1, j2, target):
    start = (0, 0)
    stack = [(start, [(start, "Initial State")])]
    visited = {start}

    while stack:
        (x, y), path = stack.pop()          # LIFO: pop last-pushed state
        if x == target or y == target:
            return path

        neighbors = [
            ((j1, y), "Fill Jug 1"),
            ((x, j2), "Fill Jug 2"),
            ((0, y), "Empty Jug 1"),
            ((x, 0), "Empty Jug 2"),
            ((x - min(x, j2 - y), y + min(x, j2 - y)), "Pour Jug1->Jug2"),
            ((x + min(y, j1 - x), y - min(y, j1 - x)), "Pour Jug2->Jug1"),
        ]
        for next_state, action in neighbors:
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, path + [(next_state, action)]))
    return None
```

### Worked Example
$J_1 = 4$, $J_2 = 3$, Target $T = 2$.

### Visualization — DFS Search Tree (depth-first path taken, left branch first)
```
(0,0)
  └─ Fill Jug1 → (4,0)
        └─ Pour 1→2 → (1,3)
              └─ Empty Jug2 → (1,0)
                    └─ Pour 1→2 → (0,1)
                          └─ Fill Jug1 → (4,1)
                                └─ Pour 1→2 → (2,3)  ✅ GOAL (Jug1 = 2)
```
DFS dives down one branch fully before trying siblings — note it never
backtracks here because the first branch happens to reach the goal; in
general DFS would explore dead-end branches (dashed below) before
backtracking.
```
(0,0)
 ├─ Fill Jug1 (explored fully first, found goal)
 ├─ Fill Jug2   ┄┄ (would only be tried if the first branch dead-ended)
 ├─ Empty Jug1  ┄┄
 └─ Empty Jug2  ┄┄
```
**Key property:** DFS is *not* guaranteed to find the shortest solution — it
finds *a* solution, possibly a long, winding one, because it commits to depth
over breadth.

---

## 2. Travelling Salesman Problem (TSP)

### Definition
Given $n$ cities and the cost between every pair, find the minimum-cost
closed tour that visits every city exactly once and returns to the start.
Brute force checks all $(n-1)!$ permutations of the non-start cities.

### Code
```python
from itertools import permutations

def solve_tsp(dist_matrix):
    n = len(dist_matrix)
    start = 0
    others = [c for c in range(n) if c != start]
    best_tour, min_cost = None, float("inf")

    for perm in permutations(others):
        tour = (start,) + perm + (start,)
        cost = sum(dist_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
        if cost < min_cost:
            min_cost, best_tour = cost, tour
    return best_tour, min_cost
```

### Worked Example — 4 cities
```
      10        15
  0 ------- 1 -------- 2
  |  \______           |
  |20      \25_35      |30
  |               \     |
  3 --------------------
```
Distance matrix:
```
      0   1   2   3
  0 [ 0, 10, 15, 20]
  1 [10,  0, 35, 25]
  2 [15, 35,  0, 30]
  3 [20, 25, 30,  0]
```

### Visualization — Best Tour Highlighted
```
Optimal tour: 0 -> 1 -> 3 -> 2 -> 0   (cost = 10+25+30+15 = 80)

   (0)===10===(1)
    |           |
   15          25
    |           |
   (2)===30===(3)
   ===  = chosen edges of the optimal tour
```
**Complexity:** Brute force is $O(n!)$ — exact but explodes fast; TSP is a
classic **NP-hard** problem, which is why heuristic/approximate methods
(nearest-neighbor, 2-opt, genetic algorithms, ant colony optimization) are
used for large $n$.

---

## 3. 8-Puzzle Problem Using Searching Algorithms

### Definition
A 3×3 grid with 8 numbered tiles and one blank. Slide tiles into the blank to
reach a goal configuration. State space size: $9!/2 = 181{,}440$ reachable
states. Can be solved with BFS, DFS, or (best) **A\*** using a heuristic like
**Manhattan distance** (sum of grid-distance each tile is from its goal
position) or **misplaced tiles count**.

### Code (A* with Manhattan distance)
```python
import heapq

def manhattan(state, goal):
    size = 3
    dist = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_i = goal.index(tile)
        dist += abs(i // size - goal_i // size) + abs(i % size - goal_i % size)
    return dist

def solve_8puzzle(start, goal):
    frontier = [(manhattan(start, goal), 0, start, [])]
    visited = {start}
    while frontier:
        f, g, state, path = heapq.heappop(frontier)
        if state == goal:
            return path + [state]
        blank = state.index(0)
        row, col = blank // 3, blank % 3
        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in moves:
            r, c = row+dr, col+dc
            if 0 <= r < 3 and 0 <= c < 3:
                new_blank = r*3+c
                new_state = list(state)
                new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
                new_state = tuple(new_state)
                if new_state not in visited:
                    visited.add(new_state)
                    heapq.heappush(frontier, (g+1+manhattan(new_state, goal), g+1, new_state, path+[state]))
    return None
```

### Worked Example
```
Start State:        Goal State:
 1  2  3              1  2  3
 4  _  6              4  5  6
 7  5  8              7  8  _
```

### Visualization — Move Sequence
```
 1 2 3      1 2 3      1 2 3
 4 _ 6  ->  4 5 6  ->  4 5 6
 7 5 8      7 _ 8      7 8 _
 (start)   (slide 5 up)  (slide 8 right)   GOAL ✅
```
Each arrow is one "move blank" action; A* picks the move sequence that
minimizes $f(n) = g(n) + h(n)$ at each step, so it reaches the goal in the
fewest necessary moves here (2 moves).

---

## 4. Hill Climbing Algorithm

### Definition
A **local search** technique: start at a random state, repeatedly move to the
**best neighboring state**, stop when no neighbor is better than the current
state. It never backtracks and keeps no memory of past states — fast and
memory-light, but prone to getting stuck.

### Code
```python
def hill_climbing(current, get_neighbors, value_fn):
    while True:
        neighbors = get_neighbors(current)
        best_neighbor = max(neighbors, key=value_fn, default=None)
        if best_neighbor is None or value_fn(best_neighbor) <= value_fn(current):
            return current                      # local (or global) optimum reached
        current = best_neighbor
```

### Worked Example — maximizing $f(x) = -(x-5)^2 + 25$ over integers
Start at $x = 1$; neighbors are $x-1, x+1$.

### Visualization — Landscape climbed
```
 f(x)
 25 |                    *  <- global maximum at x=5
    |                 *     *
    |              *           *
    |           *                 *
    |        *
  9 |     *  <- start (x=1)
    +--------------------------------- x
      1  2  3  4  5  6  7  8  9
Path: 1 -> 2 -> 3 -> 4 -> 5 (stop, no better neighbor)
```
**Failure modes (must know):**
- **Local maximum:** a peak lower than the global peak — climber stops early.
- **Plateau:** a flat region — climber can't tell which way is "up".
- **Ridge:** the true peak requires a path the simple neighbor-move can't see.

---

## 5. A* Search Algorithm for Shortest Path

### Definition
A* is a **best-first, informed search** using
$$f(n) = g(n) + h(n)$$
- $g(n)$ = actual cost from start to node $n$.
- $h(n)$ = heuristic estimate of cost from $n$ to goal (must be
  **admissible** — never overestimate — for A* to guarantee optimality).

It expands the node with the lowest $f(n)$ first, using a priority queue.

### Code
```python
import heapq

def a_star(graph, heuristic, start, goal):
    frontier = [(heuristic[start], 0, start, [start])]
    visited = set()
    while frontier:
        f, g, node, path = heapq.heappop(frontier)
        if node == goal:
            return path, g
        if node in visited:
            continue
        visited.add(node)
        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                new_g = g + cost
                heapq.heappush(frontier, (new_g + heuristic[neighbor], new_g, neighbor, path+[neighbor]))
    return None, float("inf")
```

### Worked Example
```
Graph (edges with cost):        Heuristic h(n) (straight-line estimate to G):
A --2-- B                        h(A)=6  h(B)=4
A --5-- C                        h(C)=2  h(D)=1
B --2-- D                        h(G)=0
C --1-- D
D --3-- G
```

### Visualization — Nodes Expanded and Final Path
```
        A
      /2  \5
     B      C
      \2   /1
        D
        |3
        G

f(A)=0+6=6
f(B via A)=2+4=6      f(C via A)=5+2=7
f(D via B)=4+1=5   <- chosen (lower f)
f(G via D)=7+0=7

Final path: A -> B -> D -> G   (cost = 2+2+3 = 7)
```
A* explores B before C because $f(B)=6 \le f(C)=7$ and $f(D)=5$ beats
exploring C further, so C is never expanded — this is the *efficiency* gained
from a good heuristic over blind search.

---

## PART B — "What Happens If…" Cross-Analysis

---

## Group 1 — A* Search Applied To:

**1. Water Jug** — A* works well if you define a heuristic, e.g.
$h = |x - T|$ combined with $|y - T|$ (distance from target volume in either
jug). It converges to the *shortest* sequence of operations, unlike DFS which
just finds *any* sequence. Requires building an explicit graph of jug states
first.

**2. 8-Puzzle** — This is A*'s classic use case. With Manhattan distance as
$h(n)$, A* finds the *optimal* (fewest-move) solution efficiently, pruning
far more of the $9!/2$ state space than BFS would.

**3. TSP** — A* can be adapted (e.g., held-karp-style with minimum spanning
tree as heuristic) but the state space (which cities visited so far) still
grows factorially/exponentially. A* helps prune but does not remove
NP-hardness — for large $n$ it remains impractical without further heuristics
or approximation.

**4. Hill Climbing** — This is a category mismatch: Hill Climbing is *not* a
graph-search algorithm with a frontier/open-list, so "applying A*" to it
doesn't quite parse. What you *can* say: A* subsumes hill climbing's
greediness but adds memory ($g(n)$) and backtracking via the priority queue,
so A* will never get stuck in a local optimum the way hill climbing does,
because it keeps all explored options open for reconsideration.

### Summary Table — Group 1
| Applied To | Feasible? | Result | Optimal? | Key Trade-off |
|---|---|---|---|---|
| Water Jug | Yes | Shortest operation sequence | Yes (with admissible h) | Needs a heuristic defined over jug states |
| 8-Puzzle | Yes (ideal case) | Fewest-move solution | Yes | Much faster than BFS/DFS with good h |
| TSP | Partially | Prunes search but still exponential worst case | Yes if run to completion | Doesn't beat NP-hardness for large n |
| Hill Climbing | Conceptual mismatch | N/A — different algorithm class | N/A | A* has memory + backtracking; Hill Climbing has neither |

---

## Group 2 — Heuristic Search Applied To:

**1. Water Jug** — Turns blind search into guided search; e.g., "distance to
target volume" heuristic focuses exploration and finds solutions faster than
plain DFS/BFS, though the heuristic must be crafted carefully since the state
space is small but non-obvious.

**2. 8-Puzzle** — Essential in practice — Manhattan distance or misplaced-tile
count heuristics turn an intractable blind search (181k+ states) into a
fast, near-instant solve.

**3. TSP** — Heuristic search (nearest-neighbor, greedy edge, 2-opt, genetic
algorithms) is the *standard real-world approach*, because exact solving is
infeasible for large n. Trades optimality for speed — gets a "good enough"
tour, not guaranteed the best.

**4. Hill Climbing** — Hill Climbing *is* a heuristic search method itself
(it directly uses an evaluation/heuristic function to pick the next move).
So "heuristic search applied to hill climbing" describes hill climbing's own
mechanism — the heuristic quality directly determines whether it finds a
good peak or gets stuck.

**5. A* Search** — A* *is* the premier heuristic search algorithm (heuristic
+ path cost). Applying "heuristic search" to A* just describes what A*
already is; the discussion becomes about *heuristic quality*: admissible +
consistent heuristics guarantee A* is optimal and efficient, a poor/
inadmissible heuristic can make it fast but suboptimal, or even slower than
blind search if it misleads the frontier ordering.

### Summary Table — Group 2
| Applied To | Role of Heuristic | Benefit | Risk |
|---|---|---|---|
| Water Jug | Distance to target volume | Faster convergence than blind DFS/BFS | Small state space so benefit is modest |
| 8-Puzzle | Manhattan distance / misplaced tiles | Makes huge state space tractable | Weak heuristic (e.g., misplaced tiles) explores more nodes than Manhattan |
| TSP | Nearest neighbor / MST-based estimates | Makes large instances solvable at all | Sacrifices guaranteed optimality |
| Hill Climbing | IS the search mechanism | Simple, fast, low memory | Highly sensitive to local optima |
| A* Search | Core of f(n) = g(n)+h(n) | Optimal + efficient (if admissible) | Bad heuristic breaks optimality or speed |

---

## Group 3 — DFS Applied To:

**1. Water Jug** — Natural fit; DFS with a stack + visited set finds *some*
valid operation sequence to the target, but not necessarily the shortest one
(as shown in Part A.1's search tree).

**2. 8-Puzzle** — Technically possible but poor in practice: the state
space is large and DFS can dive down very long, unproductive branches, and
without a depth limit, can even revisit unproductive regions or take far
longer than BFS/A* to find a (non-optimal) solution.

**3. TSP** — DFS naturally maps to permutation generation (i.e., depth-first
enumeration of partial tours), which is effectively what brute force does. It
guarantees finding the optimal tour eventually but with the same $O(n!)$
blow-up; it does not use cost pruning unless combined with **branch-and-
bound** (cutting a branch once its partial cost already exceeds the best
found tour).

**4. Hill Climbing** — Category mismatch again: DFS is a *complete* graph
traversal with backtracking; Hill Climbing is a *memoryless local* search.
They differ fundamentally — DFS can be seen as "the opposite philosophy":
DFS keeps exploring exhaustively (with memory of visited nodes) while Hill
Climbing commits greedily and forgets everything behind it.

**5. A\* Search** — Also a mismatch in the sense that DFS ignores cost/
heuristic information entirely (LIFO order only), whereas A* is driven
purely by $f(n)$. You could say DFS is "A* with the priority function
replaced by pure recency" — it loses all optimality guarantees in exchange
for very low memory use.

### Summary Table — Group 3
| Applied To | Works? | Finds Optimal? | Memory Use | Notable Risk |
|---|---|---|---|---|
| Water Jug | Yes | Not guaranteed | Low | May find a long, roundabout solution |
| 8-Puzzle | Yes, but weak | Rarely optimal | Can be high (deep paths) | May explore very deep before success |
| TSP | Yes (as enumeration) | Yes, eventually | Low (stack-based) | Still O(n!) without pruning |
| Hill Climbing | Conceptual mismatch | N/A | N/A | Different search philosophy entirely |
| A* Search | Conceptual mismatch | N/A | N/A | DFS ignores cost/heuristic info A* relies on |

---

## Group 4 — BFS Applied To:

**1. Water Jug** — Excellent fit: BFS explores level-by-level (queue, not
stack) and is **guaranteed to find the shortest sequence of operations**,
unlike DFS. Costs more memory since it holds an entire frontier level at
once.

**2. 8-Puzzle** — Guaranteed optimal (fewest moves) but memory-expensive:
the frontier can grow exponentially, so BFS becomes impractical for harder
scrambles compared to A* with a good heuristic.

**3. TSP** — Can be framed as BFS over partial tours, but since all edges
must eventually be explored to guarantee the optimal *complete* tour, BFS
provides no real advantage over DFS-style enumeration here — it still needs
to consider all $(n-1)!$ permutations (or all subsets in the Held-Karp DP
formulation) and uses far more memory than DFS enumeration for no benefit.

**4. Hill Climbing** — Category mismatch: BFS is exhaustive and complete;
Hill Climbing is greedy and incomplete. BFS would actually *fix* Hill
Climbing's local-optima problem by exploring everything, but doing so
defeats the entire purpose of hill climbing (speed/low memory).

**5. A\* Search** — BFS is a *special case* of A* where $h(n) = 0$ for all
nodes and all step costs are equal — A* then degenerates into plain BFS.
This illustrates directly why a heuristic matters: without it, A* is no
smarter than blind BFS.

### Summary Table — Group 4
| Applied To | Works? | Finds Optimal? | Memory Use | Notable Risk |
|---|---|---|---|---|
| Water Jug | Yes | Yes (shortest sequence) | Higher than DFS | Frontier can grow large |
| 8-Puzzle | Yes | Yes (fewest moves) | Very high | May run out of memory before A* would |
| TSP | Yes (as enumeration) | Yes | Very high | No real benefit over DFS enumeration |
| Hill Climbing | Conceptual mismatch | N/A | N/A | Defeats the purpose of hill climbing |
| A* Search | BFS = A* with h(n)=0 | Yes (unweighted case) | Higher than A* w/ good h | Loses efficiency A* would have |

---

## Group 5 — Hill Climbing Applied To:

**1. Water Jug** — Poor fit: define "closeness to target volume" as the
evaluation function; hill climbing will often get stuck because many jug
states are local optima (no single fill/empty/pour move improves closeness),
even though a solution exists a few moves away that temporarily looks
"worse."

**2. 8-Puzzle** — Also weak: using Manhattan distance as the evaluation
function, hill climbing frequently gets stuck in local optima or plateaus,
because solving a sliding puzzle often requires temporarily *increasing*
Manhattan distance before it can decrease (e.g., moving a correctly placed
tile out of the way).

**3. TSP** — This is actually a common and reasonably effective real-world
use: start from a random tour, and repeatedly swap two cities (or apply
2-opt) if it reduces total cost. Fast and simple, but can settle into a
locally short tour that isn't the globally shortest — often combined with
random restarts or simulated annealing to escape local minima.

**4. A\* Search** — Category mismatch: A* is a systematic, memory-based,
complete search; Hill Climbing cannot meaningfully be "applied to" A*, but
one framing is: Hill Climbing is what A* would degrade into if it discarded
its priority queue and visited-node memory and only ever kept the single
best current node — i.e., hill climbing is A* stripped of backtracking and
completeness.

### Summary Table — Group 5
| Applied To | Works Well? | Common Failure | Practical Use? |
|---|---|---|---|
| Water Jug | Poorly | Gets stuck at non-goal local optima | Rare — DFS/BFS preferred |
| 8-Puzzle | Poorly | Plateaus / local optima (needs temporary "worse" moves) | Rare — A* preferred |
| TSP | Reasonably well | Local minima (suboptimal tour) | Yes — with 2-opt / random restarts |
| A* Search | Conceptual mismatch | N/A | N/A — different algorithm class |

---

## PART C — Can an NP-hard Problem Be Converted Into a Heuristic Search Problem?

**Yes.** This is, in fact, the standard practical response to NP-hardness.

- An NP-hard problem (like TSP) has no known algorithm that solves it
  *exactly* in polynomial time for all instances. Exact methods (brute
  force, dynamic programming like Held-Karp, branch-and-bound) still take
  exponential time in the worst case.
- **Heuristic search reframes the goal**: instead of insisting on the
  provably optimal solution, it searches for a *good enough* solution in
  reasonable time, using domain knowledge (a heuristic function) to guide
  the search toward promising regions of the state space and prune
  unpromising ones.
- Concretely for TSP: nearest-neighbor construction, 2-opt/3-opt local
  search, simulated annealing, genetic algorithms, and ant colony
  optimization are all heuristic (and metaheuristic) methods that produce
  near-optimal tours in polynomial time, with no guarantee of exact
  optimality but often within a small, bounded percentage of it.
- The same idea generalizes to other NP-hard problems: graph coloring,
  knapsack, job-shop scheduling, and SAT all have well-known heuristic or
  approximation algorithms.
- **Trade-off being accepted:** completeness/optimality guarantees are
  exchanged for tractability — you move from "guaranteed best answer,
  possibly never finishes" to "very good answer, finishes quickly."

---

*End of Pass 1 (full technical detail). Ask for Pass 2 (simplified,
plain-language with analogies), Pass 3 (combined), or Pass 4 (viva voce
short spoken answers) whenever you're ready — they'll follow this exact
same structure.*