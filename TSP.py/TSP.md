# Traveling Salesman Problem (TSP) — Brute Force Solution Notes

## 1. Problem Overview

The Traveling Salesman Problem (TSP) asks: given a set of cities and the travel cost between every pair of them, what is the cheapest possible route that visits every city exactly once and returns to the starting city?

This brute-force approach solves it by generating **every possible route**, calculating the cost of each, and keeping track of the cheapest one found.

## 2. Imports and Function Definition

```python
from itertools import permutations
```

Imports the `permutations` tool from Python's standard `itertools` library. It automatically generates all possible orderings of a collection without needing to write nested loops.

```python
def solve_tsp(dist_matrix):
```

Defines the main TSP solving function.

- `dist_matrix`: A 2D list (matrix) where `dist_matrix[i][j]` is the travel cost from city `i` to city `j`.

```python
    num_cities = len(dist_matrix)
```

Counts the total number of cities in the graph. For a $4 \times 4$ matrix, `len(dist_matrix)` gives `4`.

```python
    start_city = 0
```

Fixes city `0` as the designated starting and ending point of the entire round trip.

## 3. Preparing Candidates and Tracking Variables

```python
    cities_to_visit = [city for city in range(num_cities) if city != start_city]
```

Uses a list comprehension to create a list of intermediate cities to visit.

- `range(4)` generates numbers `0, 1, 2, 3`.
- The condition `if city != start_city` filters out city `0`.
- **Result:** `cities_to_visit = [1, 2, 3]`.

```python
    min_cost = float("inf")
```

Initializes the tracker for the smallest cost seen so far. Setting it to positive infinity (`float("inf")`) ensures that the very first tour evaluated will always be smaller than this value and take its place.

```python
    best_tour = None
```

Initializes a placeholder variable to store the sequence of cities that produces the lowest cost.

## 4. Evaluating Every Route

```python
    for perm in permutations(cities_to_visit):
```

Loops through every possible permutation of the intermediate cities `[1, 2, 3]`. Generates tuples in order: `(1, 2, 3)`, `(1, 3, 2)`, `(2, 1, 3)`, etc.

```python
        current_tour = (start_city,) + perm + (start_city,)
```

Constructs the complete closed-loop cycle.

- `(start_city,)` creates a single-element tuple: `(0,)`.
- The `+` operator glues tuples together.
- **Example:** If `perm` is `(1, 3, 2)`, then:
  `current_tour = (0,) + (1, 3, 2) + (0,)` → `(0, 1, 3, 2, 0)`.

```python
        current_cost = 0
```

Resets the cost counter to zero before measuring the total distance of this specific tour.

```python
        for i in range(len(current_tour) - 1):
```

Loops through each leg of the journey. If `current_tour` has length 5 (`0 -> 1 -> 3 -> 2 -> 0`), there are $5 - 1 = 4$ road segments to sum up:

- Segment 1: index 0 to index 1 ($0 \rightarrow 1$)
- Segment 2: index 1 to index 2 ($1 \rightarrow 3$)
- Segment 3: index 2 to index 3 ($3 \rightarrow 2$)
- Segment 4: index 3 to index 4 ($2 \rightarrow 0$)

```python
            from_city = current_tour[i]
            to_city = current_tour[i + 1]
            current_cost += dist_matrix[from_city][to_city]
```

- `from_city`: The departure city on this leg.
- `to_city`: The arrival city on this leg.
- `dist_matrix[from_city][to_city]`: Looks up the road cost in the distance table and adds it to `current_cost`.

```python
        if current_cost < min_cost:
            min_cost = current_cost
            best_tour = current_tour
```

**Best Route Check:** If the cost of the route just checked is smaller than `min_cost`:

- Updates `min_cost` with the new lower number.
- Overwrites `best_tour` with the winning sequence `current_tour`.

```python
    return best_tour, min_cost
```

Once all permutations have been checked, returns a tuple containing the optimal path and its minimum cost.

## 5. Driver Execution Block

```python
if __name__ == "__main__":
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
```

Defines the 4-city cost table:

- Row 0 shows costs from City 0: to 0 is 0, to 1 is 10, to 2 is 15, to 3 is 20.
- Row 1 shows costs from City 1: to 0 is 10, to 1 is 0, to 2 is 35, to 3 is 25.
- And so on.

## 6. Understanding the Final 4 Lines (Line-by-Line, in Plain English)

This is the part that trips people up, so let's slow down and treat it like a recipe: each line takes the output of the line before it and transforms it into something more useful.

```python
best_path, lowest_cost = solve_tsp(graph)
path_display = "->".join(str(city) for city in best_path)
print("optimal path", path_display)
print("lowest cost", lowest_cost)
```

### 6.1 `best_path, lowest_cost = solve_tsp(graph)`

**Think of `solve_tsp(graph)` like a vending machine with two delivery slots.**

You put in a coin (`graph`, the distance table), and the machine returns **two items at once** because the function ends with:

```python
return best_tour, min_cost
```

That `return` statement is really returning a single tuple that looks like `(best_tour, min_cost)` — for example `((0, 1, 3, 2, 0), 80)`.

The line

```python
best_path, lowest_cost = solve_tsp(graph)
```

**unpacks** that tuple into two separate variables in one step:

| Variable | Gets the value of |
|---|---|
| `best_path` | `best_tour` → e.g. `(0, 1, 3, 2, 0)` |
| `lowest_cost` | `min_cost` → e.g. `80` |

It's exactly the same idea as:

```python
result = solve_tsp(graph)   # result = ((0, 1, 3, 2, 0), 80)
best_path = result[0]       # (0, 1, 3, 2, 0)
lowest_cost = result[1]     # 80
```

Python just lets you skip the middle step and split the tuple directly into named variables.

### 6.2 `path_display = "->".join(str(city) for city in best_path)`

This line turns a tuple of numbers into a single readable string. It happens in two stages — read it from the **inside out**.

**Stage A — the generator: `str(city) for city in best_path`**

This walks through every number in `best_path` (e.g. `(0, 1, 3, 2, 0)`) and converts each one from a number to text:

```python
0 -> "0"
1 -> "1"
3 -> "3"
2 -> "2"
0 -> "0"
```

This step is required because `.join()` only works on strings — you cannot glue numbers together directly.

**Stage B — the glue: `"->".join(...)`**

`.join()` takes a collection of strings and stitches them together, placing its own string (`"->"`) in between each pair.

```python
"->".join(["0", "1", "3", "2", "0"])
# "0->1->3->2->0"
```

**Mini analogy:** imagine you have beads labeled `0, 1, 3, 2, 0` and a piece of string that says `"->"`. `.join()` threads that `"->"` string between every bead, giving you one long readable line instead of a loose pile of beads.

**Result:** `path_display = "0->1->3->2->0"`

### 6.3 `print("optimal path", path_display)`

`print()` can take multiple arguments separated by commas, and it automatically prints them one after another with a single space in between.

So this prints:

```
optimal path 0->1->3->2->0
```

It is equivalent to writing:

```python
print("optimal path" + " " + path_display)
```

but `print(a, b)` does the space-joining for you automatically.

### 6.4 `print("lowest cost", lowest_cost)`

Same idea as above, just with the numeric value:

```
lowest cost 80
```

Note that `lowest_cost` is already a plain number (an `int`), so it doesn't need any `str()` conversion — `print()` converts it to text automatically when displaying it.

### 6.5 Putting It All Together

| Step | Code | What it does | Example result |
|---|---|---|---|
| 1 | `best_path, lowest_cost = solve_tsp(graph)` | Runs the solver and splits its 2-item answer into 2 variables | `best_path = (0,1,3,2,0)`, `lowest_cost = 80` |
| 2 | `path_display = "->".join(str(city) for city in best_path)` | Converts the tuple of numbers into one readable string | `"0->1->3->2->0"` |
| 3 | `print("optimal path", path_display)` | Displays the route | `optimal path 0->1->3->2->0` |
| 4 | `print("lowest cost", lowest_cost)` | Displays the cost | `lowest cost 80` |