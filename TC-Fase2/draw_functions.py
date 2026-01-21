# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:03:11 2023

@author: SérgioPolimante
"""
import pylab
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib
import pygame
from typing import List, Tuple

matplotlib.use("Agg")


def draw_plot(screen: pygame.Surface, x: list, y: list, x_label: str = 'Generation', y_label: str = 'Fitness') -> None:
    """
    Draw a plot on a Pygame screen using Matplotlib.

    Parameters:
    - screen (pygame.Surface): The Pygame surface to draw the plot on.
    - x (list): The x-axis values.
    - y (list): The y-axis values.
    - x_label (str): Label for the x-axis (default is 'Generation').
    - y_label (str): Label for the y-axis (default is 'Fitness').
    """
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    try:
        plt.tight_layout()
    except Exception:
        pass

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))
    
    # Close the figure to free memory
    plt.close(fig)
    
def draw_cities(screen: pygame.Surface, cities_locations: List[Tuple[int, int]], colors: List[Tuple[int, int, int]], radii: List[int]) -> None:
    """
    Draws circles representing cities on the given Pygame screen.

    Parameters:
    - screen (pygame.Surface): The Pygame surface on which to draw the cities.
    - cities_locations (List[Tuple[int, int]]): List of (x, y) coordinates representing the locations of cities.
    - colors (List[Tuple[int, int, int]]): List of RGB tuples representing the color of each city.
    - radii (List[int]): List of radii for each city.

    Returns:
    None
    """
    for i, city_location in enumerate(cities_locations):
        # Use the specific color and radius for each city
        color = colors[i] if i < len(colors) else (0, 0, 0) # Fallback to black
        radius = radii[i] if i < len(radii) else 5 # Fallback to 5
        pygame.draw.circle(screen, color, city_location, radius)



def draw_paths(screen: pygame.Surface, path: List[Tuple[int, int]], rgb_color: Tuple[int, int, int], width: int = 1):
    """
    Draw a path on a Pygame screen with direction arrows.

    Parameters:
    - screen (pygame.Surface): The Pygame surface to draw the path on.
    - path (List[Tuple[int, int]]): List of tuples representing the coordinates of the path.
    - rgb_color (Tuple[int, int, int]): RGB values for the color of the path.
    - width (int): Width of the path lines (default is 1).
    """
    pygame.draw.lines(screen, rgb_color, True, path, width=width)
    
    # Draw arrows
    import math
    for i in range(len(path)):
        start_pos = path[i]
        end_pos = path[(i + 1) % len(path)]
        
        # Calculate angle
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        
        # Arrow position (midpoint)
        mid_x = (start_pos[0] + end_pos[0]) / 2
        mid_y = (start_pos[1] + end_pos[1]) / 2
        
        # Arrow geometry
        arrow_len = 10
        arrow_angle = 0.5 # radians
        
        # Calculate arrow points
        x1 = mid_x - arrow_len * math.cos(angle - arrow_angle)
        y1 = mid_y - arrow_len * math.sin(angle - arrow_angle)
        
        x2 = mid_x - arrow_len * math.cos(angle + arrow_angle)
        y2 = mid_y - arrow_len * math.sin(angle + arrow_angle)
        
        # Draw arrow head
        pygame.draw.polygon(screen, rgb_color, [(mid_x, mid_y), (x1, y1), (x2, y2)])


def draw_text(screen: pygame.Surface, text: str, color: pygame.Color, position: Tuple[int, int] = (10, 10)) -> None:
    """
    Draw text on a Pygame screen.

    Parameters:
    - screen (pygame.Surface): The Pygame surface to draw the text on.
    - text (str): The text to be displayed.
    - color (pygame.Color): The color of the text.
    - position (Tuple[int, int]): Position to draw the text (x, y).
    """
    if not pygame.font.get_init():
        pygame.font.init()

    font_size = 20
    my_font = pygame.font.SysFont('Arial', font_size)
    
    # Handle multi-line text
    lines = text.split('\n')
    x, y = position
    for line in lines:
        text_surface = my_font.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += font_size + 5

