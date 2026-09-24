def astar(graph, h, start, goal):

    open = [(start, 0, [start])]

    while open:

        current, cost, path = min(
            open,
            key=lambda x: x[1] + h[x[0]]
        )

        open.remove((current, cost, path))

        if current == goal:
            return path, cost

        for next, d in graph[current]:

            if next not in path:
                open.append(
                    (next, cost + d, path + [next])
                )

    return None, None


if __name__ == "__main__":

    # Directed weighted graph
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('D', 2), ('E', 5)],
        'C': [('E', 1)],
        'D': [('G', 3)],
        'E': [('G', 2)],
        'G': []
    }

    # Heuristic estimates to goal G
    h = {
        'A': 6,
        'B': 5,
        'C': 3,
        'D': 3,
        'E': 2,
        'G': 0
    }

    start = input("Start: ").strip().upper()
    goal = input("Goal: ").strip().upper()

    path, cost = astar(graph, h, start, goal)

    if path:
        print("Path:", " -> ".join(path))
        print("Cost:", cost)
    else:
        print("No valid path exists between the given nodes.")