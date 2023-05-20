import numpy as np

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

def generate_random_solution(num_cities):
    return np.random.permutation(num_cities)

def calculate_total_distance(solution, distance_matrix):
    total_distance = 0
    num_cities = len(solution)
    for i in range(num_cities - 1):
        city_a = solution[i]
        city_b = solution[i + 1]
        total_distance += distance_matrix[city_a, city_b]
    # Add distance from last city back to the starting city
    total_distance += distance_matrix[solution[-1], solution[0]]
    return total_distance

def generate_neighbor(solution):
    num_cities = len(solution)
    i = np.random.randint(num_cities)
    j = np.random.randint(num_cities)
    neighbor = np.copy(solution)
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def firefly_algorithm(distance_matrix, num_fireflies, num_iterations):
    num_cities = distance_matrix.shape[0]
    fireflies = [generate_random_solution(num_cities) for _ in range(num_fireflies)]
    best_solution = fireflies[0]
    best_distance = calculate_total_distance(best_solution, distance_matrix)

    for _ in range(num_iterations):
        for i in range(num_fireflies):
            current_solution = fireflies[i]
            current_distance = calculate_total_distance(current_solution, distance_matrix)
            for j in range(num_fireflies):
                if calculate_total_distance(fireflies[j], distance_matrix) < current_distance:
                    attractiveness = 1 / (1 + euclidean_distance(current_solution, fireflies[j]))
                    beta = 1  # Control parameter
                    movement_probability = attractiveness * np.exp(-beta * current_distance)
                    if np.random.rand() < movement_probability:
                        current_solution = generate_neighbor(fireflies[i])
            fireflies[i] = current_solution
            current_distance = calculate_total_distance(current_solution, distance_matrix)
            if current_distance < best_distance:
                best_solution = current_solution
                best_distance = current_distance

    return best_solution, best_distance


# Example usage
distance_matrix = np.array([
    [0, 2, 9, 10, 5],
    [1, 0, 6, 4, 7],
    [15, 7, 0, 8, 10],
    [6, 3, 12, 0, 3],
    [5, 8, 4, 3, 0]
])
num_fireflies = 50
num_iterations = 100

best_solution, best_distance = firefly_algorithm(distance_matrix, num_fireflies, num_iterations)
print("Best solution:", best_solution)
print("Best distance:", best_distance)