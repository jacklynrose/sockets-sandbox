from PiicoDev_SSD1306 import *

   
def plot_image(coordinates, desired_x, desired_y, display):
    # Find the maximum x and y values in the coordinates
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    for x, y in coordinates:
        # Calculate the relative coordinates by subtracting from the maximum values
        relative_x = x + desired_x
        relative_y = y + desired_y
        
        # Plot the final coordinates using your pixel method
        display.pixel(relative_x, relative_y, 1)
    
    display.show()
    
def remove_image(coordinates, desired_x, desired_y, display):
    # Find the maximum x and y values in the coordinates
    max_x = max(coord[0] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    for x, y in coordinates:
        # Calculate the relative coordinates by subtracting from the maximum values
        relative_x = x + desired_x
        relative_y = y + desired_y
        
        # Plot the final coordinates using your pixel method
        display.pixel(relative_x, relative_y, 0)
    
    display.show()
