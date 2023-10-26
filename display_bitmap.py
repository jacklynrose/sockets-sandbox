from PiicoDev_SSD1306 import *

def convert_to_coordinates(filename):
    # Initialize an array to store coordinates and color values
    coordinates = []

    with open(filename, 'r') as file:
        for line in file:
            # Split the line into x, y, and value
            x, y, value = map(int, line.strip().split(', '))
            
            # Assuming values of 0 and 1 represent colors (adjust as needed)
            color = value

            coordinates.append((x, y, color))

    return coordinates

    
def plot_image(image, desired_x, desired_y, display):
    
    coordinates = convert_to_coordinates(image)
    # Find the maximum x and y values in the coordinates
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    for x, y, color in coordinates:
        # Calculate the relative coordinates by subtracting from the maximum values
        relative_x = x + desired_x
        relative_y = y + desired_y
        
        # Plot the final coordinates using your pixel method
        display.pixel(relative_x, relative_y, color)
    
    display.show()
