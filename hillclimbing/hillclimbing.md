# Hill Climbing (Array Version) — Code Walkthrough Notes

## 1. Function Definition & Main Loop

```python
def hill_climbing(a, start):
```

- Defines the search function.
- `a`: A 1D list of numbers representing our landscape (heights at each index).
- `start`: The integer index where the search begins.

```python
    while True:
```

- Starts an infinite loop. Hill climbing keeps taking steps until it can no longer find any neighbor higher than the current position.

```python
        current = a[start]
```

- Reads the value (height) at the current index `start` and saves it in `current`.

## 2. Checking Neighbors with Boundary Guards

```python
        left = a[start - 1] if start > 0 else -1
```

- Looks at the neighbor to the left:
  - If `start > 0`: There is a valid element to the left, so it reads `a[start - 1]`.
  - If `start == 0`: We are already at the very beginning of the array, so it assigns `-1` as a placeholder indicating "no left neighbor".

```python
        right = a[start + 1] if start < len(a) - 1 else -1
```

- Looks at the neighbor to the right:
  - If `start < len(a) - 1`: There is a valid element to the right, so it reads `a[start + 1]`.
  - If `start` is the last index (`len(a) - 1`): Assigns `-1` indicating "no right neighbor".

## 3. Deciding Where to Move

```python
        if left > current and left >= right:
            start -= 1
```

- **Step Left Condition:**
  - If the left neighbor is strictly taller than where we are (`left > current`), and it is at least as tall as the right neighbor (`left >= right`), step to the left by decrementing the index (`start -= 1`).

```python
        elif right > current:
            start += 1
```

- **Step Right Condition:**
  - If the left check wasn't chosen, but the right neighbor is strictly taller than our current position (`right > current`), step to the right by incrementing the index (`start += 1`).

```python
        else:
            return start, current
```

- **Peak Found (Termination):**
  - If neither neighbor is strictly greater than `current`, we are standing on a local peak (or flat plateau).
  - Exits the function immediately and returns a tuple containing the winning index `start` and its height `current`.

## 4. User Input & Execution

```python
a = list(map(int, input("Enter values: ").split()))
```

- Takes numbers typed by the user, split by spaces (e.g., `1 3 7 5 2`):
  - `.split()` turns the string into `['1', '3', '7', '5', '2']`.
  - `map(int, ...)` converts each string element into an integer.
  - `list(...)` packs them into a Python list: `[1, 3, 7, 5, 2]`.

```python
start = int(input("Enter starting position: "))
```

- Asks the user which index to start climbing from, converts it to an integer, and stores it in `start`.

```python
pos, value = hill_climbing(a, start)
```

- Runs the climbing function with the user inputs and unpacks the returned tuple into `pos` (index) and `value` (height).

```python
print("Peak position:", pos)
print("Peak value:", value)
```

- Prints the final peak location index and the number found at that position.