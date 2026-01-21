

import random
import math
import copy 
from typing import List, Tuple

default_problems = {
5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
10:[(470, 169), (602, 202), (754, 239), (476, 233), (468, 301), (522, 29), (597, 171), (487, 325), (746, 232), (558, 136)],
12:[(728, 67), (560, 160), (602, 312), (712, 148), (535, 340), (720, 354), (568, 300), (629, 260), (539, 46), (634, 343), (491, 135), (768, 161)],
15:[(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)]
}

def calculate_point_segment_distance(px, py, x1, y1, x2, y2):
    """
    Calculate the minimum distance between a point (px, py) and a line segment ((x1, y1), (x2, y2)).
    """
    dx = x2 - x1
    dy = y2 - y1
    
    if dx == 0 and dy == 0:
        return math.sqrt((px - x1)**2 + (py - y1)**2)

    # Project point onto line (parameter t)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx*dx + dy*dy)

    # Clamp t to segment [0, 1]
    t = max(0, min(1, t))

    # Closest point on segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return math.sqrt((px - closest_x)**2 + (py - closest_y)**2)


def generate_distance_matrix(cities_location: List[Tuple[float, float]]) -> List[List[float]]:
    """
    Generate a distance matrix for the given cities.
    Includes a heavy penalty if the path between two cities passes too close to a third city.
    """
    n = len(cities_location)
    matrix = [[0.0] * n for _ in range(n)]
    
    # Removed intersection penalty for CVRP correct distance calculation
    # INTERSECTION_PENALTY = 10000.0
    # SAFETY_RADIUS = 15.0 
    
    for i in range(n):
        for j in range(n):
            if i != j:
                # Basic Euclidean distance
                dist = math.sqrt((cities_location[i][0] - cities_location[j][0]) ** 2 + 
                                 (cities_location[i][1] - cities_location[j][1]) ** 2)
                
                # Check for intersection with any other city k - REMOVED for VRP
                penalty = 0
                # for k in range(n):
                #     if k == i or k == j:
                #         continue
                #     
                #     px, py = cities_location[k]
                #     x1, y1 = cities_location[i]
                #     x2, y2 = cities_location[j]
                #     
                #     distance_to_segment = calculate_point_segment_distance(px, py, x1, y1, x2, y2)
                #     
                #     if distance_to_segment < SAFETY_RADIUS:
                #         penalty += INTERSECTION_PENALTY
                
                matrix[i][j] = dist + penalty
                
    return matrix


def generate_random_population(n_cities: int, population_size: int) -> List[List[int]]:
    """
    Generate a random population of routes (indices) for a given number of cities.

    Parameters:
    - n_cities (int): The number of cities.
    - population_size (int): The size of the population.

    Returns:
    List[List[int]]: A list of routes, where each route is a list of city indices.
    """
    return [random.sample(range(n_cities), n_cities) for _ in range(population_size)]


def calculate_fitness(path: List[int], distance_matrix: List[List[float]], weights: List[int] = None, capacity: int = None, priorities: List[str] = None, priority_penalty: float = 0) -> float:
    """
    Calculate the fitness of a given path based on the distance matrix.
    If weights and capacity are provided, calculates the CVRP distance (sum of split trips).
    If priorities and penalty are provided, penalizes visiting Normal cities before Critical ones.
    """
    if weights is None or capacity is None:
        # Standard TSP Fitness (Single Loop)
        distance = 0
        n = len(path)
        for i in range(n):
            u = path[i]
            v = path[(i + 1) % n]
            distance += distance_matrix[u][v]
        return distance

    # CVRP Fitness (Split Routes)
    # 1. Rotate to start at Depot (0)
    if 0 in path:
        zero_idx = path.index(0)
        rotated_path = path[zero_idx:] + path[:zero_idx]
    else:
        rotated_path = path
        
    total_distance = 0
    current_load = 0
    last_node = rotated_path[0] # Should be 0
    
    # Priority Logic Setup
    pending_critical = 0
    if priorities is not None and priority_penalty > 0:
        pending_critical = sum(1 for p in priorities if p == 'Critical')
    
    # Iterate through cities excluding the depot itself at the start
    for city_idx in rotated_path[1:]:
        # Priority Check
        if priorities is not None and priority_penalty > 0:
            is_critical = priorities[city_idx] == 'Critical'
            if is_critical:
                pending_critical -= 1
            elif pending_critical > 0:
                # Penalty for visiting Normal while Critical still exists
                total_distance += priority_penalty

        w = weights[city_idx]
        if current_load + w > capacity:
            # Trip complete: Return to Depot (0)
            total_distance += distance_matrix[last_node][0]
            
            # Start new trip: Depot (0) -> current city
            total_distance += distance_matrix[0][city_idx]
            
            current_load = w
            last_node = city_idx
        else:
            # Continue trip
            total_distance += distance_matrix[last_node][city_idx]
            current_load += w
            last_node = city_idx
            
    # Final return to Depot (0)
    total_distance += distance_matrix[last_node][0]

    return total_distance

    
def calculate_fitness_path(path, distance_matrix, info_locais):
    total_distance = 0
    penalty = 0
    
    # 1. Calcular Distância
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i+1]]
    
    # 2. Aplicar Restrição de Prioridade (Exemplo Simplificado)
    # Se encontrar um item regular antes de um crítico na lista, pune.
    tem_critico_pendente = sum(1 for p in path if info_locais[p]['tipo'] == 'critico')
    for cidade in path:
        if info_locais[cidade]['tipo'] == 'critico':
            tem_critico_pendente -= 1
        elif info_locais[cidade]['tipo'] == 'regular' and tem_critico_pendente > 0:
            penalty += 1000 # Penalidade pesada
            
    # 3. Restrição de Autonomia
    MAX_AUTONOMIA = 20000 # Defina seu limite
    if total_distance > MAX_AUTONOMIA:
        penalty += 50000
        
    return total_distance + penalty
    


def order_crossover(parent1: List[Tuple[float, float]], parent2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Perform order crossover (OX) between two parent sequences to create a child sequence.

    Parameters:
    - parent1 (List[Tuple[float, float]]): The first parent sequence.
    - parent2 (List[Tuple[float, float]]): The second parent sequence.

    Returns:
    List[Tuple[float, float]]: The child sequence resulting from the order crossover.
    """
    length = len(parent1)

    # Choose two random indices for the crossover
    start_index = random.randint(0, length - 1)
    end_index = random.randint(start_index + 1, length)

    # Initialize the child with a copy of the substring from parent1
    child = parent1[start_index:end_index]

    # Fill in the remaining positions with genes from parent2
    remaining_positions = [i for i in range(length) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in parent2 if gene not in child]

    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)

    return child

### demonstration: crossover test code
# Example usage:
# parent1 = [(1, 1), (2, 2), (3, 3), (4,4), (5,5), (6, 6)]
# parent2 = [(6, 6), (5, 5), (4, 4), (3, 3),  (2, 2), (1, 1)]

# # parent1 = [1, 2, 3, 4, 5, 6]
# # parent2 = [6, 5, 4, 3, 2, 1]


# child = order_crossover(parent1, parent2)
# print("Parent 1:", [0, 1, 2, 3, 4, 5, 6, 7, 8])
# print("Parent 1:", parent1)
# print("Parent 2:", parent2)
# print("Child   :", child)


# # Example usage:
# population = generate_random_population(5, 10)

# print(calculate_fitness(population[0]))


# population = [(random.randint(0, 100), random.randint(0, 100))
#           for _ in range(3)]



# TODO: implement a mutation_intensity and invert pieces of code instead of just swamping two. 
def mutate(solution:  List[Tuple[float, float]], mutation_probability: float) ->  List[Tuple[float, float]]:
    """
    Mutate a solution by inverting a segment of the sequence with a given mutation probability.

    Parameters:
    - solution (List[int]): The solution sequence to be mutated.
    - mutation_probability (float): The probability of mutation for each individual in the solution.

    Returns:
    List[int]: The mutated solution sequence.
    """
    mutated_solution = copy.deepcopy(solution)

    # Check if mutation should occur    
    if random.random() < mutation_probability:
        
        # Ensure there are at least two cities to perform a swap
        if len(solution) < 2:
            return solution
    
        # Select a random index (excluding the last index) for swapping
        index = random.randint(0, len(solution) - 2)
        
        # Swap the cities at the selected index and the next index
        mutated_solution[index], mutated_solution[index + 1] = solution[index + 1], solution[index]   
        
    return mutated_solution

### Demonstration: mutation test code    
# # Example usage:
# original_solution = [(1, 1), (2, 2), (3, 3), (4, 4)]
# mutation_probability = 1

# mutated_solution = mutate(original_solution, mutation_probability)
# print("Original Solution:", original_solution)
# print("Mutated Solution:", mutated_solution)


def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    """
    Sort a population based on fitness values.

    Parameters:
    - population (List[List[Tuple[float, float]]]): The population of solutions, where each solution is represented as a list.
    - fitness (List[float]): The corresponding fitness values for each solution in the population.

    Returns:
    Tuple[List[List[Tuple[float, float]]], List[float]]: A tuple containing the sorted population and corresponding sorted fitness values.
    """
    # Combine lists into pairs
    combined_lists = list(zip(population, fitness))

    # Sort based on the values of the fitness list
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])

    # Separate the sorted pairs back into individual lists
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return sorted_population, sorted_fitness


if __name__ == '__main__':
    N_CITIES = 10
    
    POPULATION_SIZE = 100
    N_GENERATIONS = 100
    MUTATION_PROBABILITY = 0.3
    cities_locations = [(random.randint(0, 100), random.randint(0, 100))
              for _ in range(N_CITIES)]
    
    # CREATE INITIAL POPULATION
    population = generate_random_population(cities_locations, POPULATION_SIZE)

    # Lists to store best fitness and generation for plotting
    best_fitness_values = []
    best_solutions = []
    
    for generation in range(N_GENERATIONS):
  
        
        population_fitness = [calculate_fitness(individual) for individual in population]    
        
        population, population_fitness = sort_population(population,  population_fitness)
        
        best_fitness = calculate_fitness(population[0])
        best_solution = population[0]
           
        best_fitness_values.append(best_fitness)
        best_solutions.append(best_solution)    

        print(f"Generation {generation}: Best fitness = {best_fitness}")

        new_population = [population[0]]  # Keep the best individual: ELITISM
        
        while len(new_population) < POPULATION_SIZE:
            
            # SELECTION
            parent1, parent2 = random.choices(population[:10], k=2)  # Select parents from the top 10 individuals
            
            # CROSSOVER
            child1 = order_crossover(parent1, parent2)
            
            ## MUTATION
            child1 = mutate(child1, MUTATION_PROBABILITY)
            
            new_population.append(child1)
            
    
        print('generation: ', generation)
        population = new_population
    


