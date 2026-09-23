def condition(state, j1, j2):
    x, y = state
    moves = []

    moves.append(((j1, y), "fill a jug 1"))
    moves.append(((x, j2), "fill a jug 2"))
    moves.append(((0, y), "empty a jug 1"))
    moves.append(((x, 0), "empty a jug 2"))

    # Pour jug 1 -> jug 2
    pour_to_2 = min(x, j2 - y)
    moves.append(((x - pour_to_2, y + pour_to_2), "transfer water from jug 1 to jug 2"))

    # Pour jug 2 -> jug 1
    pour_to_1 = min(y, j1 - x)
    moves.append(((x + pour_to_1, y - pour_to_1), "transfer water from jug 2 to jug 1"))

    return moves


def dfs_water_jug(j1, j2, target):
    initial_state = (0, 0)
    initial_path = [(initial_state, "initial state")]

    stack = [(initial_state, initial_path)]
    visited = set()

    while stack:
        current_state, path = stack.pop()

        if current_state[0] == target or current_state[1] == target:
            return path

        if current_state in visited:
            continue
        visited.add(current_state)

        for next_state, action in condition(current_state, j1, j2):
            if next_state not in visited:
                new_path = path + [(next_state, action)]
                stack.append((next_state, new_path))

    return None


if __name__ == "__main__":
    j1 = 4
    j2 = 3
    target = 2

    print(f"Searching for {target}L using Jug 1 ({j1}L) and Jug 2 ({j2}L)...")
    solution = dfs_water_jug(j1, j2, target)

    if solution:
        print(f"\nGoal Reached in {len(solution) - 1} steps:\n")
        for step_num, (state, action) in enumerate(solution):
            print(f"Step {step_num:2d}: {action:<38} -> State (J1, J2): {state}")
    else:
        print("\nNo solution exists for the given inputs.")       
                


   

      