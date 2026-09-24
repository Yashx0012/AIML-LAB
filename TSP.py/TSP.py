from itertools import permutations
def tsp(dist_matrix):
    num_cities=len(dist_matrix)
    startcity=0
    cities_to_visit=[city for city in range(num_cities) if city != startcity]

    min_cost=float("inf")
    best_tour=None
    for perm in permutations(cities_to_visit):
        current_tour=(startcity,)+perm+(startcity,)
        current_cost=0

        for i in range(len(current_tour)-1):
            from_city=current_tour[i]
            end_city=current_tour[i+1]
            current_cost+=dist_matrix[from_city][end_city]

        if current_cost<min_cost:
            min_cost=current_cost
            best_tour=current_tour

    return best_tour, min_cost

if __name__ == "__main__":
    # Cost adjacency matrix for 4 cities (0, 1, 2, 3)
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    best_path, lowest_cost= tsp(graph)
    path_display="->".join(str(city) for city in best_path)
    print("optimal path", path_display)
    print("lowest cost", lowest_cost)


