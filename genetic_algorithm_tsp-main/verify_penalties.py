from genetic_algorithm import generate_distance_matrix
import math

def test_penalties():
    # Define 3 cities in a line: A(0,0) -> C(50,0) -> B(100,0)
    # A path from A to B should pass through C.
    cities = [
        (0.0, 0.0),    # Index 0
        (100.0, 0.0),  # Index 1
        (50.0, 0.0)    # Index 2 (The city in the middle)
    ]
    
    matrix = generate_distance_matrix(cities)
    
    # Distance 0->1 should be 100 + penalty
    dist_0_1 = matrix[0][1]
    expected_base = 100.0
    
    print(f"Distance 0->1: {dist_0_1}")
    
    if dist_0_1 > 1000 + expected_base:
        print("SUCCESS: Penalty applied for 0->1 passing through 2")
    else:
        print("FAILURE: No penalty applied for 0->1 passing through 2")
        
    # Distance 0->2 should be 50 (no penalty)
    dist_0_2 = matrix[0][2]
    print(f"Distance 0->2: {dist_0_2}")
    if dist_0_2 == 50.0:
        print("SUCCESS: No penalty for 0->2")
    else:
         print(f"FAILURE: Unexpected distance for 0->2: {dist_0_2}")

if __name__ == "__main__":
    test_penalties()
