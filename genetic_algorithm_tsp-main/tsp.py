import pygame
from pygame.locals import *
import random
import itertools
from genetic_algorithm import mutate, order_crossover, generate_random_population, calculate_fitness, sort_population, default_problems, generate_distance_matrix
from draw_functions import draw_paths, draw_plot, draw_cities, draw_text
import sys
import numpy as np
import pygame
from benchmark_att48 import *


# Define constant values
# pygame
WIDTH, HEIGHT = 800, 400
NODE_RADIUS = 10
FPS = 30
PLOT_X_OFFSET = 450

# GA
# Default values used if run directly
DEFAULT_N_CITIES = 15
DEFAULT_POPULATION_SIZE = 100
DEFAULT_N_GENERATIONS = 5000
DEFAULT_MUTATION_PROBABILITY = 0.5
DEFAULT_TRUCK_CAPACITY = 80

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ROUTE_COLORS = [BLUE, RED, PURPLE, ORANGE, CYAN, MAGENTA, YELLOW]

def get_routes_with_capacity(solution_indices, weights, capacity):
    routes = []
    current_route = []
    current_load = 0
    
    if not solution_indices:
        return []

    # Enforce Fixed Depot = 0
    # Find where 0 is in the solution
    try:
        zero_index = solution_indices.index(0)
    except ValueError:
        zero_index = 0
        
    # Rotate solution so 0 is at index 0
    rotated_solution = solution_indices[zero_index:] + solution_indices[:zero_index]
    
    depot_index = rotated_solution[0] # Should be 0
    
    # Start first route from depot
    current_route = [depot_index]
    
    # Iterate through the rest
    for city_idx in rotated_solution[1:]:
        weight = weights[city_idx]
        if current_load + weight > capacity:
            # Close current route
            routes.append(current_route)
            
            # Start new route
            current_route = [depot_index, city_idx]
            current_load = weight
        else:
            current_route.append(city_idx)
            current_load += weight
    
    # Add the last route
    if len(current_route) > 1:
        routes.append(current_route)
        
    return routes

def run_tsp_simulation(truck_capacity=DEFAULT_TRUCK_CAPACITY, 
                       population_size=DEFAULT_POPULATION_SIZE, 
                       n_generations=DEFAULT_N_GENERATIONS, 
                       mutation_probability=DEFAULT_MUTATION_PROBABILITY,
                       critical_indices_str="",
                       priority_penalty=0):
    
    # Using att48 benchmark
    WIDTH, HEIGHT = 1500, 800
    PLOT_X_OFFSET = 450
    NODE_RADIUS = 10
    
    att_cities_locations = np.array(att_48_cities_locations)
    max_x = max(point[0] for point in att_cities_locations)
    max_y = max(point[1] for point in att_cities_locations)
    scale_x = (WIDTH - PLOT_X_OFFSET - NODE_RADIUS) / max_x
    scale_y = HEIGHT / max_y
    cities_locations = [(int(point[0] * scale_x + PLOT_X_OFFSET),
                         int(point[1] * scale_y)) for point in att_cities_locations]

    # Process Priorities
    current_priorities = ['Normal'] * len(cities_locations)
    
    if critical_indices_str and critical_indices_str.strip():
        # User defined overrides
        try:
            # Parse "1, 5, 10" -> [1, 5, 10]
            indices = [int(x.strip()) for x in critical_indices_str.split(',') if x.strip().isdigit()]
            for idx in indices:
                if 0 <= idx < len(current_priorities):
                    current_priorities[idx] = 'Critical'
        except Exception:
            print("Error parsing critical indices, using defaults.")
            pass # Fallback to Normal if error
    else:
        # Use Benchmark Defaults if nothing provided? Or default to None?
        # Let's use Benchmark defaults to match previous behavior if empty
        current_priorities = att_48_cities_priorities

    # Generate Distance Matrix
    distance_matrix = generate_distance_matrix(cities_locations)

    target_solution = [i-1 for i in att_48_cities_order[:-1]]
    fitness_target_solution = calculate_fitness(target_solution, distance_matrix, att_48_cities_weights, truck_capacity, current_priorities, priority_penalty)
    print(f"Best Solution: {fitness_target_solution}")
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSP Solver using Pygame")
    clock = pygame.time.Clock()
    generation_counter = itertools.count(start=1)  # Start the counter at 1
    FPS = 30

    # Create Initial Population
    population = generate_random_population(len(cities_locations), population_size)
    best_fitness_values = []
    best_solutions = []

    # Generate Random Baseline
    random_baseline = random.sample(range(len(cities_locations)), len(cities_locations))
    random_baseline_fitness = calculate_fitness(random_baseline, distance_matrix, att_48_cities_weights, truck_capacity, current_priorities, priority_penalty)
    print(f"Random Baseline Fitness: {random_baseline_fitness}")

    # Main game loop
    running = True
    paused = False 
    finished = False
    current_best_fitness = float('inf')
    generation = 0 
    
    # Track start time for performance stats
    # start_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not finished:
                        paused = not paused
                elif event.key == pygame.K_c:
                     if finished:
                         # Navigate to Chat
                         import subprocess
                         subprocess.Popen(["python", "chat-ia.py"])

        # Update Generation (if active)
        if not paused and not finished:
            generation = next(generation_counter)
            if n_generations and generation >= n_generations:
                finished = True
                print("Simulation Complete!")
        
        screen.fill(WHITE)

        # Evolution Step (Only calculate if we are running or just finished to show final state)
        # We always draw the current state, but only update population if active.
        
        # NOTE: To save performance, we could skip re-calculating fitness every frame if paused/finished,
        # but for simplicity we keep the draw logic consistent.
        
        if not finished and not paused:
             population_fitness = [calculate_fitness(individual, distance_matrix, att_48_cities_weights, truck_capacity, current_priorities, priority_penalty) for individual in population]
             population, population_fitness = sort_population(population,  population_fitness)
             
             best_fitness = calculate_fitness(population[0], distance_matrix, att_48_cities_weights, truck_capacity, current_priorities, priority_penalty)
             best_solution = population[0]
             
             if best_fitness < current_best_fitness:
                 current_best_fitness = best_fitness
             
             best_fitness_values.append(best_fitness)
             best_solutions.append(best_solution)

             # Evolution Logic
             new_population = [population[0]] 
             while len(new_population) < population_size:
                 probability = 1 / np.array(population_fitness)
                 parent1, parent2 = random.choices(population, weights=probability, k=2)
                 child1 = order_crossover(parent1, parent1)
                 child1 = mutate(child1, mutation_probability)
                 new_population.append(child1)
             population = new_population

        else:
             # Just retrieve current best for drawing
             best_fitness = calculate_fitness(population[0], distance_matrix, att_48_cities_weights, truck_capacity, current_priorities, priority_penalty)
             best_solution = population[0]


        draw_plot(screen, list(range(len(best_fitness_values))),
                  best_fitness_values, y_label="Fitness - Distance (pxls)")

        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        ORANGE = (255, 165, 0)

        # Process Cities Metadata
        city_colors = []
        city_radii = []
        critical_count = 0
        normal_count = 0

        for i in range(len(cities_locations)):
            prio = current_priorities[i]
            if prio == 'Critical':
                city_colors.append(RED)
                critical_count += 1
            else:
                city_colors.append(GREEN)
                normal_count += 1
            
            weight = att_48_cities_weights[i]
            radius = 5 + weight 
            city_radii.append(radius)
        
        # Calculate routes based on capacity
        capacity_routes = get_routes_with_capacity(best_solution, att_48_cities_weights, truck_capacity)

        # Highlight Start City (Depot) - Depot is start of all routes
        if len(best_solution) > 0:
            # Fixed Depot is always 0
            depot_idx = 0
            current_frame_colors = city_colors.copy()
            current_frame_colors[depot_idx] = ORANGE
        else:
            current_frame_colors = city_colors

        stats_text = f"Total Cities: {len(cities_locations)}\nCritical (Red): {critical_count}\nNormal (Green): {normal_count}\n"
        stats_text += f"Generation: {generation}/{n_generations}\nBest Fitness: {round(best_fitness, 2)}\n"
        stats_text += f"Truck Capacity: {truck_capacity}\nTrips: {len(capacity_routes)}\n"
        
        # Calculate improvement
        if random_baseline_fitness > 0:
             improvement_pct = 100 * (random_baseline_fitness - best_fitness) / random_baseline_fitness
        else:
             improvement_pct = 0
             
        stats_text += f"Baseline (Random): {round(random_baseline_fitness, 2)}\n"
        stats_text += f"Improvement: {round(improvement_pct, 2)}%\n"
        stats_text += f"Priorities: {'Custom' if critical_indices_str else 'Default'}\n"
        
        if finished:
            stats_text += "SIMULATION COMPLETE"
        else:
            stats_text += "Press SPACE to Pause" if not paused else "PAUSED"
        
        draw_text(screen, stats_text, BLACK, (10, 10))

        draw_cities(screen, cities_locations, current_frame_colors, city_radii)
        
        # Draw logic for capacity routes
        for i, route_indices in enumerate(capacity_routes):
            subset_coords = [cities_locations[idx] for idx in route_indices]
            color = ROUTE_COLORS[i % len(ROUTE_COLORS)]
            draw_paths(screen, subset_coords, color, width=3)
        
        # Overlay for Finished State
        if finished:
            # Create a semi-transparent surface
            s = pygame.Surface((WIDTH, HEIGHT))  # the size of your rect
            s.set_alpha(128)                # alpha level
            s.fill((0,0,0))           # black
            screen.blit(s, (0,0))
            
            # Centered Text
            font_large = pygame.font.SysFont('Arial', 64, bold=True)
            font_small = pygame.font.SysFont('Arial', 32)
            
            text_surf = font_large.render("SIMULATION FINISHED", True, WHITE)
            text_rect = text_surf.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
            screen.blit(text_surf, text_rect)
            
            res_text = f"Final Improvement: {round(improvement_pct, 2)}% | Fitness: {round(best_fitness, 2)}"
            res_surf = font_small.render(res_text, True, YELLOW)
            res_rect = res_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 20))
            screen.blit(res_surf, res_rect)
            
            close_text = "Press Q to Close | Press C to Chat with IA"
            close_surf = font_small.render(close_text, True, WHITE)
            close_rect = close_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 70))
            screen.blit(close_surf, close_rect)
            
            # Generate LLM Report (Once)
            # using a static variable attribute on the function or a global to avoid spamming
            if not hasattr(run_tsp_simulation, "report_generated"):
                run_tsp_simulation.report_generated = True
                print("Generating Driver Report with Llama...")
                
                try:
                    from llm_service import gerar_relatorio_motorista
                    
                    # Prepare data
                    route_indices = best_solution
                    truck_data = f"Capacity: {truck_capacity} | Trips: {len(capacity_routes)}"
                    
                    relatorio = gerar_relatorio_motorista(route_indices, truck_data)
                    
                    # 'a' mode creates the file if it doesn't exist, and appends if it does.
                    with open("relatorio_viagem.txt", "a", encoding="utf-8") as f:
                        f.write("\n\n--- NOVO RELATÓRIO ---\n")
                        f.write(relatorio)
                        
                    print("Report saved to 'relatorio_viagem.txt'!")
                    
                    # Optional: Show on screen that report is saved
                    rep_text = "Relatório salvo em relatorio_viagem.txt"
                    rep_surf = font_small.render(rep_text, True, GREEN)
                    rep_rect = rep_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 120))
                    screen.blit(rep_surf, rep_rect)
                    
                except Exception as e:
                    print(f"Failed to generate report: {e}")
            else:
                 # Draw the 'report saved' text if already generated
                 rep_text = "Relatório salvo em relatorio_viagem.txt"
                 rep_surf = font_small.render(rep_text, True, GREEN)
                 rep_rect = rep_surf.get_rect(center=(WIDTH/2, HEIGHT/2 + 120))
                 screen.blit(rep_surf, rep_rect)
        
        # second_solution_coords = [cities_locations[i] for i in population[1]]
        # draw_paths(screen, second_solution_coords, rgb_color=(128, 128, 128), width=1)

        if not finished and generation % 10 == 0:
            print(f"Generation {generation}: Best fitness = {round(best_fitness, 2)}")

        pygame.display.flip()
        clock.tick(FPS)
        

    # exit software
    pygame.quit()
    # sys.exit() # Dont exit sys, just return

if __name__ == "__main__":
    run_tsp_simulation()
