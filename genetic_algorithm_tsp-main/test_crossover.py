
import random
from genetic_algorithm import order_crossover

def test_crossover():
    parent1 = list(range(10))
    parent2 = list(reversed(range(10)))
    
    print(f"Parent1: {parent1}")
    print(f"Parent2: {parent2}")
    
    for i in range(5):
        try:
            child = order_crossover(parent1, parent2)
            print(f"Child {i}: {child}")
            
            if len(child) != 10:
                print("FAILURE: Child length incorrect")
            if len(set(child)) != 10:
                print("FAILURE: Duplicates found in child")
                from collections import Counter
                print(f"Counts: {Counter(child)}")
                
        except Exception as e:
            print(f"FAILURE: Exception {e}")

if __name__ == "__main__":
    try:
        test_crossover()
    except Exception as e:
        print(e)
