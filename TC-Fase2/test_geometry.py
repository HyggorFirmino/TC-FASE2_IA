import math

def distance_point_segment(px, py, x1, y1, x2, y2):
    # Vector from p1 to p2
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

def test():
    # Radius
    R = 10
    
    # Case 1: Direct hit
    # A(0,0) -> B(100,0) passing through C(50,0)
    d = distance_point_segment(50, 0, 0, 0, 100, 0)
    print(f"Case 1 (Direct hit): Dist={d}, Hit={d < R}")

    # Case 2: Near miss
    # A(0,0) -> B(100,0) passing near C(50, 9)
    d = distance_point_segment(50, 9, 0, 0, 100, 0)
    print(f"Case 2 (Near miss): Dist={d}, Hit={d < R}")

    # Case 3: Safe
    # A(0,0) -> B(100,0) passing safely C(50, 11)
    d = distance_point_segment(50, 11, 0, 0, 100, 0)
    print(f"Case 3 (Safe): Dist={d}, Hit={d < R}")
    
    # Case 4: Behind start
    # A(0,0) -> B(100,0), C(-20, 0)
    d = distance_point_segment(-20, 0, 0, 0, 100, 0)
    print(f"Case 4 (Behind): Dist={d}, Hit={d < R}") # Should be 20, False

if __name__ == "__main__":
    test()
